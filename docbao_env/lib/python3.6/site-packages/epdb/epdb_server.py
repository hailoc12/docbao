#!/usr/bin/env python
#
# Copyright (c) SAS Institute, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


"""
Telnet Server implementation.

Based on telnetlib telnet client - reads in and parses telnet protocol
from the socket, understands window change requests and interrupt requests.
(IP and NAWS).

This server does _NOT_ do LINEMODE, instead it is character based.  This means
to talk to this server using the standard telnet client, you'll need to first
type "CTRL-] mode char\n"
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from six.moves.socketserver import TCPServer, BaseRequestHandler
import fcntl
import os
import pty
import select
import signal
import six
import socket
import struct
import sys
import telnetlib
import termios
from telnetlib import IAC, IP, SB, SE, DO, DONT, WILL, TM, NAWS

IPRESP = b'\x03'  # chr(ord('C') & 0x1F)


class TelnetServerProtocolHandler(telnetlib.Telnet):
    """
        Code that actually understands telnet protocol.
        Accepts telnet-coded input from the socket and passes on that
        information to local, which should be the master for a pty controlled
        process.
    """
    def __init__(self, socket, local):
        telnetlib.Telnet.__init__(self)
        self.sock = socket
        self.remote = self.sock.fileno()
        self.local = local
        self.set_option_negotiation_callback(self.process_IAC)

    def process_IAC(self, sock, cmd, option):
        """
            Read in and parse IAC commands as passed by telnetlib.

            SB/SE commands are stored in sbdataq, and passed in w/ a command
            of SE.
        """
        if cmd == DO:
            if option == TM:
                # timing mark - send WILL into outgoing stream
                os.write(self.remote, IAC + WILL + TM)
            else:
                pass
        elif cmd == IP:
            # interrupt process
            os.write(self.local, IPRESP)
        elif cmd == SB:
            pass
        elif cmd == SE:
            option = self.sbdataq[0]
            if option == NAWS[0]:
                # negotiate window size.
                cols = six.indexbytes(self.sbdataq, 1)
                rows = six.indexbytes(self.sbdataq, 2)
                s = struct.pack('HHHH', rows, cols, 0, 0)
                fcntl.ioctl(self.local, termios.TIOCSWINSZ, s)
        elif cmd == DONT:
            pass
        else:
            pass

    def handle(self):
        """
            Performs endless processing of socket input/output, passing
            cooked information onto the local process.
        """
        while True:
            toRead = select.select([self.local, self.remote], [], [], 0.1)[0]
            if self.local in toRead:
                data = os.read(self.local, 4096)
                self.sock.sendall(data)
                continue
            if self.remote in toRead or self.rawq:
                buf = self.read_eager()
                os.write(self.local, buf)
                continue


class TelnetRequestHandler(BaseRequestHandler):
    """
        Request handler that serves up a shell for users who connect.
        Derive from this class to change the execute() method to change how
        what command the request serves to the client.
    """
    command = '/bin/sh'
    args = ['/bin/sh']

    def setup(self):
        pass

    def handle(self):
        """
            Creates a child process that is fully controlled by this
            request handler, and serves data to and from it via the
            protocol handler.
        """
        pid, fd = pty.fork()
        if pid:
            protocol = TelnetServerProtocolHandler(self.request, fd)
            protocol.handle()
        else:
            self.execute()

    def execute(self):
        try:
            os.execv(self.command, self.args)
        finally:
            os._exit(1)

    def finish(self):
        pass


class TelnetServer(TCPServer):

    allow_reuse_address = True

    def __init__(self, server_address=None,
                 requestHandlerClass=TelnetRequestHandler):
        if not server_address:
            server_address = ('', 23)
        TCPServer.__init__(self, server_address, requestHandlerClass)


class TelnetServerForCommand(TelnetServer):
    def __init__(self, server_address=None,
                 requestHandlerClass=TelnetRequestHandler,
                 command=['/bin/sh']):
        class RequestHandler(requestHandlerClass):
            pass
        RequestHandler.command = command[0]
        RequestHandler.args = command
        TelnetServer.__init__(self, server_address, RequestHandler)


class InvertedTelnetRequestHandler(TelnetRequestHandler):
    def handle(self):
        masterFd, slaveFd = pty.openpty()

        try:
            # if we're not in the main thread, this will not work.
            signal.signal(signal.SIGTTOU, signal.SIG_IGN)
        except:
            pass
        pid = os.fork()
        if pid:
            os.close(masterFd)
            raise SocketConnected(slaveFd, pid)
            # make parent process the pty slave - the opposite of
            # pty.fork().  In this setup, the parent process continues
            # to act normally, while the child process performs the
            # logging.  This makes it simple to kill the logging process
            # when we are done with it and restore the parent process to
            # normal, unlogged operation.
        else:
            os.close(slaveFd)
            try:
                protocol = TelnetServerProtocolHandler(self.request, masterFd)
                protocol.handle()
            finally:
                os.close(masterFd)
                os._exit(1)


class InvertedTelnetServer(TelnetServer):
    """
        Creates a telnet server that controls the stdin and stdout
        of the current process, instead of serving a subprocess.

        The telnet server can be closed at any time, and when it is
        input and output for the current process will be restored.
    """
    def __init__(self, server_address=None,
                 requestHandlerClass=InvertedTelnetRequestHandler):
        TelnetServer.__init__(self, server_address, requestHandlerClass)
        self.closed = True
        self.oldStdin = self.oldStdout = self.oldStderr = None
        self.oldTermios = None

    def handle_request(self):
        """
            Handle one request - serve current process to one connection.

            Use close_request() to disconnect this process.
        """
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            try:
                # we only serve once, and we want to free up the port
                # for future serves.
                self.socket.close()
                self.process_request(request, client_address)
            except SocketConnected as err:
                self._serve_process(err.slaveFd, err.serverPid)
                return
            except Exception as err:
                self.handle_error(request, client_address)
                self.close_request()

    def _serve_process(self, slaveFd, serverPid):
        """
            Serves a process by connecting its outputs/inputs to the pty
            slaveFd.  serverPid is the process controlling the master fd
            that passes that output over the socket.
        """
        self.serverPid = serverPid
        if sys.stdin.isatty():
            self.oldTermios = termios.tcgetattr(sys.stdin.fileno())
        else:
            self.oldTermios = None
        self.oldStderr = SavedFile(2, sys, 'stderr')
        self.oldStdout = SavedFile(1, sys, 'stdout')
        self.oldStdin = SavedFile(0, sys, 'stdin')
        self.oldStderr.save(slaveFd, mode="w")
        self.oldStdout.save(slaveFd, mode="w")
        self.oldStdin.save(slaveFd, mode="r")
        os.close(slaveFd)
        self.closed = False

    def close_request(self):
        if self.closed:
            pass
        self.closed = True
        # restore old terminal settings before quitting
        self.oldStderr.restore()
        self.oldStdout.restore()
        self.oldStdin.restore()
        self.oldStderr = self.oldStdout = self.oldStdin = None
        if self.oldTermios is not None:
            termios.tcsetattr(0, termios.TCSADRAIN, self.oldTermios)
        os.waitpid(self.serverPid, 0)


class SocketConnected(Exception):
    """
        Control-Flow Exception raised when we have successfully connected
        a socket.

        Used for IntertedTelnetServer
    """
    def __init__(self, slaveFd, serverPid):
        self.slaveFd = slaveFd
        self.serverPid = serverPid


class SavedFile(object):

    def __init__(self, fileno, module, attribute):
        self.fileno = fileno
        self.module = module
        self.attribute = attribute
        self.fileno_saved = None
        self.fileobj_saved = None
        self.fileobj_new = None

    def save(self, newFileno, mode="r"):
        # Save the file object in any case, it may not even have a real
        # underlying descriptor.
        self.fileobj_saved = getattr(self.module, self.attribute)
        # Duplicate the descriptor if possible.
        try:
            self.fileno_saved = os.dup(self.fileno)
        except OSError:
            self.fileno_saved = None
        # Duplicate the new PTY into place and open it as a new object.
        os.dup2(newFileno, self.fileno)
        self.fileobj_new = os.fdopen(self.fileno, mode)
        setattr(self.module, self.attribute, self.fileobj_new)

    def restore(self):
        # First destroy the duplicated PTY object and descriptor
        self.fileobj_new.close()
        self.fileobj_new = None
        # Now restore the original file object
        setattr(self.module, self.attribute, self.fileobj_saved)
        self.fileobj_saved = None
        # And if the descriptor was successfully duplicated earlier, restore
        # it.
        if self.fileno_saved is not None:
            os.dup2(self.fileno_saved, self.fileno)
            try:
                os.close(self.fileno_saved)
            except OSError:
                pass
            self.fileno_saved = None


if __name__ == '__main__':
    print('serving on 8081....')
    t = TelnetServer(('', 8081))
    t.serve_forever()
