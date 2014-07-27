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


def rule(sloc):  # parsing rule, fallback
    split_space = [x for x in sloc.split(" ") if len(x) and x != ";"]
    command = split_space[0] if len(split_space) else ""
    args, kwds, out = list(), dict(), list()
    if len(split_space) > 1:
        tokens = list()
        for x in " ".join(split_space[1:]).split("-")[1:]:
            if x[0].isdigit():
                tokens[-1] += "-" + x
            else:
                tokens.append(x)
        for t in tokens:
            k = t.split(" ")[0]
            v = remove_headtail(t[len(k):])
            v = [eval_data(v)
                 for v in v.split(" ")] if " " in v else eval_data(v)
            kwds[k] = v if v is not None else 1
    return command, args, kwds, out


def remove_headtail(string):
    s = str(string)  # force type
    while s.startswith(" "):
        s = s[1:]
    while s.endswith(" "):
        s = s[:-1]
    return s


def eval_data(string):
    s = str(string)  # force type
    if not len(s):
        return None  # this way 'is not None' works
    try:
        s = eval(s)  # int, float
    except:
        pass  # fallback to string
    return s
