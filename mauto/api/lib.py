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
from PySide.QtCore import QSettings
from . import Macro


class Lib(object):

    def __init__(self):
        super(Lib, self).__init__()
        self.macros = dict()  # {name: (macro, filepath), ...}
        self.reload()

    @property
    def repository(self):
        if not hasattr(self, "_repo"):
            settings = QSettings("csaez", "mauto")
            self._repo = settings.value("repo")
            if not self._repo:
                self._repo = os.path.normpath(
                    os.path.join(
                        os.path.expanduser("~"),
                        "mauto"))
        if not os.path.exists(self._repo):
            os.makedirs(self._repo)
        return self._repo

    @repository.setter
    def repository(self, value):
        settings = QSettings("csaez", "mauto")
        settings.setValue("repo", value)
        if not os.path.exists(value):
            os.makedirs(value)
        self._repo = value
        self.reload()

    def reload(self):
        for f in os.listdir(self.repository):
            filepath = os.path.join(self.repository, f)
            if os.path.isfile(filepath) and filepath.endswith(".json"):
                with open(filepath) as fp:
                    data = json.load(fp)
                if Macro.is_valid(data):
                    m = Macro.from_data(data)
                    self.macros[m.name] = (m, filepath)

    def get(self, name):
        d = self.macros.get(name)
        return d[0] if d else None

    def get_filepath(self, name):
        d = self.macros.get(name)
        return d[1] if d else None

    def new_macro(self, name, log=None, save=True):
        if not self.get(name):
            m = Macro.from_log(name, log) if log else Macro(name)
            self.macros[name] = (m, None)
            if save:
                self.save_macro(name)
            return self.macros.get(name)[0]
        return None

    def save_macro(self, name, filename=None):
        macro = self.get(name)
        if not macro:
            return False

        filename = filename if filename is not None else os.path.join(
            self.repository, "{}.json".format(name))
        self.macros[name] = (macro, filename)
        with open(filename, "w") as fp:
            json.dump(macro.serialize(), fp)
        return os.path.exists(filename)

    def remove_macro(self, name):
        if not self.get(name):
            return
        fp = self.macros.get(name)[1]
        del self.macros[name]
        if fp and os.path.exists(fp):
            os.remove(fp)

library = Lib()
