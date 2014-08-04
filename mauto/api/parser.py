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

REGEX = {
    # command -flag value REFERENCE;
    "general": r'-[a-zA-Z]+\s[a-zA-Z0-9]*\s([a-zA-Z][a-zA-Z0-9\s\.]+)\s?;',
    # command "REFERENCE.attr" value;
    "attr": r'.*\s\"([a-zA-Z][a-zA-Z0-9]*).*;',
    # select -flag value REFERENCE(s);
    "select": r'select\s\-\w*\s([a-zA-Z][a-zA-Z0-9\s\.]+)\s?;'
}  # <---- add extra regex here!

OUTPUT = r'//\s([a-zA-Z0-9\s]*)\s//'  # // REFERENCE(s) //


def parse(MEL):
    actions = list()
    for i, sloc in enumerate(MEL.split("\n")):
        if not len(sloc) or sloc[0].isupper():
            continue
        if sloc.startswith("//"):
            if i and not actions[-1]["sloc"].startswith("parent"):
                for x in re.compile(OUTPUT).findall(sloc):
                    actions[-1]["out"] = str_to_list(x)
        else:
            actions.append({"sloc": sloc, "out": list()})
    return actions


def get_deps(MEL):
    deps = set()
    for expr in REGEX.values():
        for x in re.compile(expr).findall(MEL):
            deps = deps.union(set(str_to_list(x)))
    return list(deps)


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
