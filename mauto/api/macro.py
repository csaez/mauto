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

from . import parser

try:
    from maya import cmds as mc
    from maya import mel
except ImportError:
    pass


class Macro(object):

    def __init__(self, name):
        super(Macro, self).__init__()
        self.name = name
        self.actions = list()

        self.filepath = None
        self._tempfile = "mauto_tempHistoryLog.txt"
        self._recording = False

    @classmethod
    def from_data(cls, data):
        """
        De-serialize an instance from data dict.
        """
        if cls.is_valid(data):
            m = cls(data["name"])
            m.deserialize(data)
            return m

    @classmethod
    def from_log(cls, name, log):
        m = cls(name)
        m.actions.extend(parser.parse(log))
        return m

    @staticmethod
    def is_valid(data):
        """
        Returns a bool validating data dict.
        """
        try:
            validate = {"filetype": "mauto_macro", "version": 0.1}
            return all([data.get(k) == v for k, v in validate.iteritems()])
        except AttributeError:
            return False

    @property
    def inputs(self):
        """
        Returns a dict of the macro's external references.
        This dict is usually used as a template for the custom inputs
        passed to play().
        """
        return dict([(k, v) for k, v in self._template().iteritems() if v is None])

    @property
    def recording(self):
        """
        Returns a bool indicating wether the macro is recording or not.
        """
        return self._recording

    def _template(self):
        t = dict()
        for a in self.actions:
            for o in a["out"]:
                t[o] = -1  # set un-initiated
            for ref in parser.get_deps(a["sloc"]):
                t[ref] = t.get(ref)
        return t

    def record(self):
        """
        Start recording a log with the actions done in the Maya GUI.
        """
        mc.scriptEditorInfo(historyFilename=self._tempfile, writeHistory=True)
        self._recording = True

    def play(self, inputs=None):
        """
        Run the macro.
        If inputs is passed, it replaces the external references by the
        ones on the incoming dict. Otherwise it look for the same references
        as the ones used when the macro was recorded."""
        # default value
        if inputs is None:
            inputs = dict([(k, k) for k in self.inputs.keys()])
        # merge input with internal refs
        ref = self._template()
        ref.update(inputs)
        # run
        mc.undoInfo(openChunk=True)  # start grouping undo
        for a in self.actions:
            code = a["sloc"]
            for k, v in ref.iteritems():
                if k in code and k != v:
                    code = code.replace(k, v)
            out = mel.eval(code)
            if isinstance(out, (list, tuple)):
                for i, x in enumerate(out):
                    ref[a["out"][i]] = x
            else:
                if a.get("out"):
                    ref[a["out"]] = out
        mc.undoInfo(closeChunk=True)  # end grouping undo
        return True

    def stop(self):
        """
        Same as self.pause().
        """
        self.pause()

    def pause(self):
        """
        Pauses the recording.
        """
        if not self.recording:
            return
        mc.scriptEditorInfo(writeHistory=False)
        _tempfile = mc.scriptEditorInfo(query=True, historyFilename=True)
        with open(_tempfile) as fp:
            log = fp.read()
        self.actions.extend(parser.parse(log))  # parse log
        with open(_tempfile, "w") as fp:  # clear temp file
            fp.write("")
        self._recording = False

    def serialize(self):
        """Returns a dict with macro's data."""
        return {"name": self.name,
                "actions": self.actions,
                "filetype": "mauto_macro",
                "version": 0.1,
                "filepath": self.filepath}

    def deserialize(self, data):
        """Fills up the macro using the incoming data dict."""
        if self.is_valid(data):
            for k, v in data.iteritems():
                setattr(self, k, v)
        return self.is_valid(data)
