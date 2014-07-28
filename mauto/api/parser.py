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
import importlib

EXCLUDE = ("marking", "mode")
PARSING_RULES = dict()

rules_path = os.path.join(os.path.dirname(__file__), "rules")
rules = list()
for name in os.listdir(rules_path):
    full_name = os.path.join(rules_path, name)
    if os.path.isfile(full_name) and "__init__" not in name:
        rules.append(name.split(".")[0])
for r in rules:
    m = importlib.import_module("mauto.api.rules.%s" % r)
    PARSING_RULES[r] = getattr(m, "rule")
PARSING_RULES["null"] = lambda x: (None, list(), dict(), list())
PARSING_RULES["createlocator"] = PARSING_RULES["null"]


def parse(log):
    macro = list()
    # cleanup
    log = "\n".join([l.replace(" ;", ";")[:-1] for l in log.split("\n")
                     if not any([x in l.lower() for x in EXCLUDE])])
    # parsing
    for sloc in log.split("\n"):
        if sloc.startswith("//"):  # comments
            if "// Result: " not in sloc:
                continue
            # command filtering, regex seemed overkill
            out = sloc.replace("// Result: ", "")[:-2]
            # set as the output of the previous command
            previous = list(macro[-1])
            previous[-1] = [x for x in out.split(" ") if len(x)]
            macro[-1] = tuple(previous)
        else:
            macro.append(parse_sloc(sloc))
    return macro


def parse_sloc(sloc):
    split_space = [x for x in sloc.split(" ") if len(x) and x != ";"]
    cmd_name = split_space[0] if len(split_space) else ""
    default = PARSING_RULES.get("base")
    return PARSING_RULES.get(cmd_name.lower(), default)(sloc)
