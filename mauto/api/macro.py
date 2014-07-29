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

import json
from . import parser


class Macro(object):

    def __init__(self, name):
        super(Macro, self).__init__()
        self.name = name
        self.actions = list()

        self.filepath = None
        self._tempfile = "mauto_tempHistoryLog.txt"
        self._recording = False

    @classmethod
    def from_file(cls, filepath):
        if cls.is_valid(filepath):
            with open(filepath) as fp:
                data = json.load(fp)
            m = cls(data["name"])
            m.actions = data["actions"]
            m.filepath = filepath
            return m

    @classmethod
    def from_log(cls, name, log):
        m = cls(name)
        m.actions = parser.parse(log)
        return m

    @staticmethod
    def is_valid(json_file):
        with open(json_file) as fp:
            try:
                data = json.load(fp)
            except ValueError:
                return False
        validate = {"filetype": "mauto_macro", "version": 0.1}
        return all([data.get(k) == v for k, v in validate.iteritems()])

    @property
    def inputs(self):
        t = dict()
        for k, v in self._template(self.actions).iteritems():
            if v is None:
                t[k] = v
        return t

    @property
    def recording(self):
        return self._recording

    def _template(self):
        t = dict()
        for command, args, kwds, outputs in self.actions:
            for o in outputs:
                t[o] = -1  # set unitialized
            if command:
                for a in args:
                    if isinstance(a, basestring):
                        t[a] = t.get(a)
        for k, v in t.iteritems():
            for key in t.keys():
                if key + "." in k and key != k:
                    t[k] = lambda x=key, y=k.replace(key, ""): str(t[x]) + y
        return t

    def record(self):
        if len(self.actions):
            print "WARNING: %s actions are going to be overriden" % self.name
        from maya import cmds as mc
        mc.scriptEditorInfo(historyFilename=self._tempfile, writeHistory=True)
        self._recording = True

    def play(self, inputs=None):
        from maya import cmds as mc
        # default value
        if not inputs:
            inputs = dict()
        # merge input with internal refs
        ref = self._template()
        ref.update(inputs)
        # run
        for command, args, kwds, outputs in self.actions:
            if not command:
                continue
            args = [ref[a]() for a in args]  # solve runtime args
            r = getattr(mc, command)(*args, **kwds)
            for i, o in outputs:
                ref[o] = lambda x=r[i]: x  # update outputs

    def stop(self, clear_file=True):
        if not self.recording:
            return
        from maya import cmds as mc
        mc.scriptEditorInfo(writeHistory=False)
        self._recording = False
        _tempfile = mc.scriptEditorInfo(query=True, historyFilename=True)
        with open(_tempfile, "w") as f:
            log = f.read()
            if clear_file:
                f.write("")  # clear temp file
        self.actions = parser.parse(log)

    def pause(self):
        self.stop(clear_file=False)

    def save(self):
        if self.filepath:
            return self.export(self.filepath)
        return False

    def export(self, filepath):
        data = {"name": self.name,
                "actions": self.actions,
                "filetype": "mauto_macro",
                "version": 0.1}
        with open(filepath, "w") as fp:
            json.dump(data, fp, indent=2, separators=[",", ":"])
        return True
