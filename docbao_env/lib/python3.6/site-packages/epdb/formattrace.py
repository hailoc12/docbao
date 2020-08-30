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
Methods for formatting "extended" tracebacks with locals.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import sys
import types
import inspect
import itertools
import linecache
from six.moves import xmlrpc_client
from six.moves.reprlib import Repr

if (sys.version_info > (3, 0)):
    # Python 3 code in this block

    # Types for which calling __safe_str__ has side effects
    UNSAFE_TYPES = (
        xmlrpc_client.ServerProxy,
        xmlrpc_client._Method,
      )

    # Types that should not appear in the output at all
    IGNORED_TYPES = (
        types.FunctionType,
        types.ModuleType,
      )
else:
    # Python 2 code in this block

    # Types for which calling __safe_str__ has side effects
    UNSAFE_TYPES = (
        xmlrpc_client.ServerProxy,
        xmlrpc_client.MethodType,
      )

    # Types that should not appear in the output at all
    IGNORED_TYPES = (
        types.ClassType,
        types.FunctionType,
        types.ModuleType,
        types.TypeType,
        )


# Set for consumers to hook into for black listing their own classes.
UNSAFE_TYPE_NAMES = set()


class TraceRepr(Repr):
    def __init__(self, subsequentIndent=""):
        Repr.__init__(self)
        self.maxtuple = 20
        self.maxset = 160
        self.maxlist = 20
        self.maxdict = 20
        self.maxstring = 1600
        self.maxother = 160

        self.maxLineLen = 160

        self.subsequentIndent = subsequentIndent
        # Pretty-print?
        self._pretty = True

    def _pretty_repr(self, pieces, iterLen, level):
        ret = ', '.join(pieces)
        if not self._pretty or len(ret) < self.maxLineLen:
            return ret
        padding = self.subsequentIndent + "  " * (self.maxlevel - level)
        sep = ',\n' + padding
        return '\n' + padding + sep.join(pieces)

    def _repr_iterable(self, obj, level, left, right, maxiter, trail=''):
        n = len(obj)
        if level <= 0 and n:
            out = '...len=%d...' % n
        else:
            newlevel = level - 1
            repr1 = self.repr1
            pieces = [repr1(elem, newlevel)
                      for elem in itertools.islice(obj, maxiter)]
            if n > maxiter:
                pieces.append('...len=%d...' % n)
            out = self._pretty_repr(pieces, n, level)
            if n == 1 and trail:
                right = trail + right
        return '%s%s%s' % (left, out, right)

    def repr_dict(self, obj, level):
        n = len(obj)
        if n == 0:
            return '{}'
        if level <= 0:
            return '{...len=%d...}' % n
        newlevel = level - 1
        repr1 = self.repr1
        pieces = []
        for key in itertools.islice(sorted(obj), self.maxdict):
            oldPretty = self._pretty
            self._pretty = False
            keyrepr = repr1(key, newlevel)
            self._pretty = oldPretty

            oldSubsequentIndent = self.subsequentIndent
            self.subsequentIndent += ' ' * 4
            valrepr = repr1(obj[key], newlevel)
            self.subsequentIndent = oldSubsequentIndent

            pieces.append('%s: %s' % (keyrepr, valrepr))
        if n > self.maxdict:
            pieces.append('...len=%d...' % n)
        out = self._pretty_repr(pieces, n, level)
        return '{%s}' % (out,)


def shouldSafeStr(obj):
    if hasattr(types, 'InstanceType') and isinstance(obj, types.InstanceType):
        # Old-style instances
        cls = obj.__class__
    else:
        # New-style instances and non-instances
        cls = type(obj)

    if isinstance(obj, UNSAFE_TYPES):
        return False
    if cls.__name__ in UNSAFE_TYPE_NAMES:
        return False

    if not hasattr(obj, '__safe_str__'):
        return False
    if not callable(obj.__safe_str__):
        return False

    return True


def formatCode(frame, stream):
    _updatecache = linecache.updatecache

    def updatecache(*args):
        # linecache.updatecache looks in the module search path for
        # files that match the module name. This is a problem if you
        # have a file without source with the same name as a python
        # standard library module. We'll just check to see if the file
        # exists first and require exact path matches.
        if not os.access(args[0], os.R_OK):
            return []
        return _updatecache(*args)
    linecache.updatecache = updatecache
    try:
        try:
            frameInfo = inspect.getframeinfo(frame, context=1)
        except:
            frameInfo = inspect.getframeinfo(frame, context=0)
        fileName, lineNo, funcName, text, idx = frameInfo

        stream.write('  File "%s", line %d, in %s\n' %
                     (fileName, lineNo, funcName))
        if text is not None and len(text) > idx:
            # If the source file is not available, we may not be able to get
            # the line
            stream.write('    %s\n' % text[idx].strip())
    finally:
        linecache.updatecache = _updatecache


def formatLocals(frame, stream):
    prettyRepr = TraceRepr(subsequentIndent=" " * 27).repr
    for name, obj in sorted(frame.f_locals.items()):
        if name.startswith('__') and name.endswith('__'):
            # Presumably internal data
            continue
        if isinstance(obj, IGNORED_TYPES):
            # Uninteresting things like functions
            continue
        try:
            if shouldSafeStr(obj):
                vstr = obj.__safe_str__()
            else:
                vstr = prettyRepr(obj)
        except Exception as error:
            # Failed to get a representation, but at least display what
            # type it was and what exception was raised.
            if hasattr(types, 'InstanceType') \
                    and isinstance(obj, types.InstanceType):
                typeName = obj.__class__.__name__
            else:
                typeName = type(obj).__name__
            vstr = '** unrepresentable object of type %r (error: %s) **' % (
                typeName, error.__class__.__name__)

        stream.write("        %15s : %s\n" % (name, vstr))


def stackToList(stack):
    """
    Convert a chain of traceback or frame objects into a list of frames.
    """
    if isinstance(stack, types.TracebackType):
        while stack.tb_next:
            stack = stack.tb_next
        stack = stack.tb_frame

    out = []
    while stack:
        out.append(stack)
        stack = stack.f_back
    return out


def formatTrace(excType, excValue, excTB, stream=sys.stderr, withLocals=True):
    stream.write(str(excType))
    stream.write(": ")
    stream.write(str(excValue))
    stream.write("\n\n")

    tbStack = stackToList(excTB)
    if withLocals:
        stream.write("Traceback (most recent call first):\n")
    else:
        stream.write("Traceback (most recent call last):\n")
        tbStack.reverse()

    for frame in tbStack:
        formatCode(frame, stream)

        if withLocals:
            formatLocals(frame, stream)
            stream.write("  %s\n\n" % ("*" * 70))
