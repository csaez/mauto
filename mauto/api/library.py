# The MIT License (MIT)

# Copyright (c) 2014 Cesar Saez

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys


class PseudoModule(object):
    import os
    from .macro import Macro

    HOME_DIR = os.path.normpath(os.path.join(os.path.expanduser("~"), "mauto"))
    EXTRA_DIR = os.environ.get("MAUTO_PATH")

    def __init__(self):
        super(PseudoModule, self).__init__()
        if not self.os.path.exists(self.HOME_DIR):
            self.os.makedirs(self.HOME_DIR)

    @property
    def macros(self):
        if hasattr(self, "_macros"):
            return self._macros
        self._macros = self.get_macros()
        return self._macros

    def get_macros(self):
        macros = set()
        for d in (self.HOME_DIR, self.EXTRA_DIR):
            if not d:
                continue
            for f in self.os.listdir(d):
                filepath = self.os.path.join(d, f)
                if self.os.path.isfile(filepath) and filepath.endswith(".json"):
                    macros.add(self.Macro.from_file(filepath))
        return macros

    def list_macros(self):
        return [m.name for m in self.macros]

    def get_macro(self, name):
        for m in self.macros:
            if m.name == name:
                return m
        return None

    def new_macro(self, name):
        if name in self.list_macros():
            print "Warning: name collision"
            return None
        m = self.Macro(name)
        m.export(self.os.path.join(self.HOME_DIR, "%s.json" % name))
        self.add_macro(m)
        return m

    def add_macro(self, macro):
        self._macros.add(macro)

    def remove_macro(self, name):
        m = self.get_macro(name)
        if not m:
            print "Macro not found"
            return
        self._macros.discard(m)
        del m


# this is a hack to use classes' magic methods on modules,
# does the trick overriding the modules cache with a class instance
sys.modules[__name__] = PseudoModule()
