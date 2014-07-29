import os
from nose import with_setup
from ..api import library as l


def setup():
    return l.new_macro("testsuite")


def teardown():
    n = "testsuite"
    if l.get(n):
        del l[n]

def test_get_macro():
    n = "unexistent_macro"
    assert l.get(n) is None


@with_setup(setup, teardown)
def test_get_macro2():
    assert l.get("testsuite") is not None


@with_setup(setup, teardown)
def test_get_macro3():
    assert l.get("testsuite").name == "testsuite"


@with_setup(setup, teardown)
def test_new_macro():
    assert type(l.get("testsuite")).__name__ == "Macro"


@with_setup(setup, teardown)
def test_remove_macro1():
    del l["testsuite"]
    assert l.get("testsuite") is None


@with_setup(setup, teardown)
def test_remove_macro2():
    fp = l.get("testsuite").filepath
    del l["testsuite"]
    assert os.path.exists(fp) is False
