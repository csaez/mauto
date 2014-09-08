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

import re


BANNED_CMDS = ("nodeOutliner", "doCreatePointConstraintArgList")

REGEX = {
    # command -flag value REFERENCE;
    "general": r'-[a-zA-Z]+\s[a-zA-Z0-9]*\s([a-zA-Z][a-zA-Z0-9\s\.]+)\s?;',
    # command "REFERENCE.attr" value;
    "attr": r'.*\s\"([a-zA-Z][a-zA-Z0-9]*).*;',
    # select -flag value REFERENCE(s);
    "select": r'select\s\-\w*\s([a-zA-Z][a-zA-Z0-9\s\.]+)\s?;',
    # connectAttr -flag REF1.attr REF2.Attr;
    "connectAttr": r'^connectAttr.*?(\w*)[\w\.]*\s(\w*)[\w\.]*\s?;$',
}  # <---- add extra regex here!

OUTPUT = r'//\s([a-zA-Z0-9_\s]*)\s?//.*'  # // REFERENCE(s) //


def str_to_list(text):
    result = list()
    _split = [_ for _ in text.split(" ") if len(_)]
    if len(_split) > 1:
        result.extend(_split)
    else:
        result.append(text)
    # cleanup
    result = list(set(result))
    for i, x in enumerate(result):
        while x.startswith(" "):
            x = x[1:]
        while x.endswith(" "):
            x = x[:-1]
        if "." in x:
            x = x.split(".")[0]
        result[i] = x
    return result


def get_deps(code):
    deps = set()
    for expr in REGEX.values():
        for x in re.compile(expr).findall(code):
            _add = str_to_list(x) if isinstance(x, basestring) else x
            deps = deps.union(set(_add))
    return list(deps)


class Parse(object):

    def __init__(self, code):
        self.actions = self.get_actions(code)
        self.references = self.get_references()
        self.inputs = self.get_inputs()

    def get_actions(self, code):
        actions = list()
        for i, sloc in enumerate(code.splitlines()):
            v = (not len(sloc),
                 sloc[0].isupper(),
                 sloc.split(" ")[0] in BANNED_CMDS)
            if any(v):
                continue
            if sloc.startswith("//"):
                if i and not actions[-1]["sloc"].startswith("parent"):
                    for x in re.compile(OUTPUT).findall(sloc):
                        actions[-1]["out"].extend(str_to_list(x))
            else:
                actions.append({"sloc": sloc, "out": list()})
        return actions

    def get_references(self):
        t = dict()
        for a in self.actions:
            for o in a["out"]:
                t[o] = -1  # set un-initiated
            for ref in get_deps(a["sloc"]):
                t[ref] = t.get(ref)
        return t

    def get_inputs(self):
        return [k for k, v in self.references.iteritems()
                if v is None]
