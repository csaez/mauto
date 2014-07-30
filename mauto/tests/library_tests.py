import os
from nose import with_setup
from ..api import library as l


def setup():
    return l.new_macro("testsuite")


def teardown():
    n = "testsuite"
    if l.get(n):
        l.remove_macro(n)


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
    l.remove_macro("testsuite")
    assert l.get("testsuite") is None


@with_setup(setup, teardown)
def test_remove_macro2():
    fp = l.get("testsuite").filepath
    l.remove_macro("testsuite")
    assert os.path.exists(fp) is False


@with_setup(setup, teardown)
def test_save_macro():
    assert l.save_macro("testsuite")


@with_setup(setup, teardown)
def test_reload():
    lenA = len(l)
    l.clear()
    l.reload()
    assert len(l) == lenA
