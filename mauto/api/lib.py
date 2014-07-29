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

import os
from . import Macro


class Lib(dict):

    HOME_DIR = os.path.normpath(os.path.join(os.path.expanduser("~"), "mauto"))
    EXTRA_DIR = os.environ.get("MAUTO_PATH")

    def __init__(self):
        super(Lib, self).__init__()
        if not os.path.exists(self.HOME_DIR):
            os.makedirs(self.HOME_DIR)
        self.reload()

    def reload(self):
        self.clear()
        for d in (self.HOME_DIR, self.EXTRA_DIR):
            if not d:
                continue
            for f in os.listdir(d):
                filepath = os.path.join(d, f)
                if os.path.isfile(filepath) and filepath.endswith(".json"):
                    m = Macro.from_file(filepath)
                    if m:
                        self.__setitem__(m.name, m)

    def new_macro(self, name):
        if self.get(name):
            print "Warning: name collision"
            return None
        m = Macro(name)
        m.filepath = os.path.join(self.HOME_DIR, "%s.json" % name)
        m.save()
        self.__setitem__(name, m)
        return m

    def __delitem__(self, name):
        fp = self.__getitem__(name).filepath if self.get(name) else None
        super(Lib, self).__delitem__(name)
        if fp and os.path.exists(fp):
            os.remove(fp)
