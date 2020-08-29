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

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import rlcompleter


class ECompleter(rlcompleter.Completer):

    def global_matches(self, text):
        """Compute matches when text is a simple name.

        Return a list of all keywords, built-in functions and names currently
        defined in self.namespace that match.

        """
# lines commented out make tab completion match keywords and builtins,
# which we don't want
#        import keyword
        matches = []
        n = len(text)
        for list in [
                     # keyword.kwlist,
                     # __builtin__.__dict__,
                     self.namespace]:
            for word in list:
                if word[:n] == text and word != "__builtins__":
                    matches.append(word)
        return matches
