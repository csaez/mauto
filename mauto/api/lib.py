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
import json
from . import Macro


class Lib(dict):
    EXTRA_DIR = os.environ.get("MAUTO_PATH")

    def __init__(self, repo):
        super(Lib, self).__init__()
        self.repo = repo
        if not os.path.exists(self.repo):
            os.makedirs(self.repo)
        self.reload()

    def reload(self):
        self.clear()
        for d in (self.repo, self.EXTRA_DIR):
            if not d:
                continue
            for f in os.listdir(d):
                filepath = os.path.join(d, f)
                if os.path.isfile(filepath) and filepath.endswith(".json"):
                    with open(filepath) as fp:
                        data = json.load(fp)
                    if Macro.is_valid(data):
                        m = Macro.from_data(data)
                        self.__setitem__(m.name, m)

    def new_macro(self, name, log=None, filename=None):
        if self.get(name):
            print "Warning: name collision"
            return None
        m = Macro(name) if not log else Macro.from_log(name, log)
        self.__setitem__(name, m)
        self.save_macro(name, filename)
        return self.get(name)

    def save_macro(self, name, filename=None):
        m = self.__getitem__(name)
        _filename = filename if filename else name + ".json"
        m.filepath = os.path.join(self.repo, _filename)
        with open(m.filepath, "w") as fp:
            json.dump(m.serialize(), fp)
        return os.path.exists(m.filepath)

    def remove_macro(self, name):
        fp = self.__getitem__(name).filepath if self.get(name) else None
        self.__delitem__(name)
        if fp and os.path.exists(fp):
            os.remove(fp)

library = Lib(os.path.normpath(os.path.join(os.path.expanduser("~"), "mauto")))
