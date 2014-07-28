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
from .macro import Macro

HOME_DIR = os.path.normpath(os.path.join(os.path.expanduser("~"), "mauto"))
EXTRA_DIR = os.environ.get("MAUTO_PATH")

if not os.path.exists(HOME_DIR):
    os.makedirs(HOME_DIR)


def macros():
    macros = set()
    for d in (HOME_DIR, EXTRA_DIR):
        if not d:
            continue
        for f in os.listdir(d):
            filepath = os.path.join(d, f)
            if os.path.isfile(filepath) and filepath.endswith(".json"):
                macros.add(Macro.from_file(filepath))
    return macros


def list_macros():
    return [m.name for m in macros()]


def get_macro(name):
    for m in macros():
        if m.name == name:
            return m
    return None


def new_macro(name):
    if name in list_macros():
        print "Warning: name collision"
        return None
    m = Macro(name)
    m.export(os.path.join(HOME_DIR, "%s.json" % name))
    return m


def remove_macro(name):
    m = get_macro(name)
    if not m:
        print "Macro not found"
        return
    m.destroy()
