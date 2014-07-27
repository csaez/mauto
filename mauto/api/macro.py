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
from mauto.api import parser


class Macro(object):

    def __init__(self, name):
        super(Macro, self).__init__()
        self.name = name
        self.actions = list()

    @classmethod
    def from_file(cls, file_path):
        with open(file_path) as fp:
            data = json.load(fp)
        validate = {"filetype": "mauto_macro", "version": 0.1}
        if all([data.get(k) == v for k, v in validate.iteritems()]):
            m = cls(data["name"])
            m.actions = data["actions"]
            return m

    @classmethod
    def from_log(cls, name, log):
        m = cls(name)
        m.actions = parser.parse(log)
        return m

    @property
    def inputs(self):
        t = dict()
        for k, v in self._template(self.actions).iteritems():
            if v is None:
                t[k] = v
        return t

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
        pass

    def is_recording(self):
        pass

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

    def stop(self):
        pass

    def save(self, file_path):
        data = {"name": self.name,
                "actions": self.actions,
                "filetype": "mauto_macro",
                "version": 0.1}
        with open(file_path, "w") as fp:
            json.dump(data, fp, indent=2, separators=[":", ","])
