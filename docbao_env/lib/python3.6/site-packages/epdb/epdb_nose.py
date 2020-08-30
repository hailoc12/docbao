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
This plugin provides ``--epdb`` and ``--epdb-failures`` options. The ``--epdb``
option will drop the test runner into epdb when it encounters an error. To
drop into epdb on failure, use ``--epdb-failures``.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import epdb
import sys

from nose.plugins.base import Plugin

import traceback


class Epdb(Plugin):
    """
    Provides --epdb and --epdb-failures options that cause the test runner to
    drop into epdb if it encounters an error or failure, respectively.
    """
    def options(self, parser, env):
        """Register commandline options.
        """
        parser.add_option(
            "--epdb", action="store_true", dest="epdb_debugErrors",
            default=env.get('NOSE_EPDB', False),
            help="Drop into extended debugger on errors")
        parser.add_option(
            "--epdb-failures", action="store_true",
            dest="epdb_debugFailures",
            default=env.get('NOSE_EPDB_FAILURES', False),
            help="Drop into extended debugger on failures")

    def configure(self, options, conf):
        """Configure which kinds of exceptions trigger plugin.
        """
        self.conf = conf
        self.enabled = options.epdb_debugErrors or options.epdb_debugFailures
        self.enabled_for_errors = options.epdb_debugErrors
        self.enabled_for_failures = options.epdb_debugFailures

    def addError(self, test, err):
        """Enter pdb if configured to debug errors.
        """
        if not self.enabled_for_errors:
            return
        self.debug(err)

    def addFailure(self, test, err):
        """Enter pdb if configured to debug failures.
        """
        if not self.enabled_for_failures:
            return
        self.debug(err)

    def debug(self, err):
        ec, ev, tb = err
        stdout = sys.stdout
        sys.stdout = sys.__stdout__
        try:
            traceback.print_exc()
        except Exception:
            print(*sys.exc_info())
        try:
            epdb.post_mortem(tb)
        finally:
            sys.stdout = stdout
