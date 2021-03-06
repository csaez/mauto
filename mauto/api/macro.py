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
from . import cache  # dumb module used to monkeypatch/share states

try:
    from maya import cmds, mel
except ImportError:
    pass


def mauto_job():
    curr_dag = set(cmds.ls(dag=True))
    new = curr_dag - cache.dag
    if len(new):
        print "// %s //" % " ".join(new)
        cache.dag = curr_dag
    return new


class Macro(object):

    def __init__(self, name):
        self.name = name
        self.log = ""
        self.actions = None
        self.references = None
        self.inputs = None
        self.recording = False
        self._logfile = "mauto_tempHistoryLog.txt"

        # init global scene cache
        # used to subtract nodes on a scriptjob
        cache.dag = set()

    @classmethod
    def from_data(cls, data):
        if cls.is_valid(data):
            m = cls(data["name"])
            m.deserialize(data)
            return m

    @classmethod
    def from_log(cls, name, log):
        m = cls(name)
        m.log = log
        m.stop()  # parse the log
        return m

    @staticmethod
    def is_valid(data):
        try:
            validate = {"filetype": "mauto_macro", "version": 0.1}
            return all([data.get(k) == v for k, v in validate.iteritems()])
        except AttributeError:
            return False

    def serialize(self):
        data = {"filetype": "mauto_macro",
                "version": 0.1, }
        for k, v in self.__dict__.iteritems():
            if not k.startswith("_"):
                data[k] = v
        return data

    def deserialize(self, data):
        if self.is_valid(data):
            for k, v in data.iteritems():
                setattr(self, k, v)
        return self.is_valid(data)

    def record(self):
        cmds.scriptEditorInfo(historyFilename=self._logfile, writeHistory=True)
        self.recording = True
        # set scriptjob
        if not len(cache.dag):
            cache.dag = set(cmds.ls(dag=True))
        job_number = cmds.scriptJob(event=("DagObjectCreated", mauto_job))
        cache.job_number = job_number

    def pause(self):
        # kill scriptjob
        for j in cmds.scriptJob(listJobs=True):
            if j.startswith("{}:".format(cache.job_number)):
                cmds.scriptJob(kill=cache.job_number, force=True)
        # record
        if self.recording:
            cmds.scriptEditorInfo(writeHistory=False)
            _logfile = cmds.scriptEditorInfo(query=True, historyFilename=True)
            with open(_logfile) as fp:
                _log = fp.read()
            self.log += _log
            # clear temp file
            with open(_logfile, "w") as fp:
                fp.write("")
            self.recording = False
        p = parser.Parse(self.log)
        for k in ("actions", "references", "inputs"):
            setattr(self, k, getattr(p, k))

    def stop(self):
        self.pause()

    def play(self, **options):
        if not self.references:
            return False
        # re-parse the log, fresh start
        p = parser.Parse(self.log)
        for k in ("actions", "references", "inputs"):
            setattr(self, k, getattr(p, k))
        # update ref dict
        self.references.update(options)
        cmds.undoInfo(openChunk=True)  # group undo
        try:
            for j, a in enumerate(self.actions):
                code = a["sloc"]
                # replace dependencies from reference table
                for x in parser.get_deps(code):
                    r = self.references.get(x)
                    if isinstance(r, basestring):
                        code = code.replace(x, r)
                # eval code
                out = mel.eval(code)
                # init outputs into reference table
                if isinstance(out, (list, tuple)):
                    for i, x in enumerate(out):
                        self.references[a["out"][i]] = x
                else:
                    if a.get("out"):
                        self.references[a["out"][0]] = out
        except Exception as err:
            raise err
        finally:
            cmds.undoInfo(closeChunk=True)
        return True
