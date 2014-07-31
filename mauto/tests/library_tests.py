import os
from nose import with_setup
from ..api.lib import Lib, library


def setup():
    return library.new_macro("testsuite")


def teardown():
    n = "testsuite"
    if library.get(n):
        library.remove_macro(n)


def test_get_macro():
    n = "unexistent_macro"
    assert library.get(n) is None


@with_setup(setup, teardown)
def test_get_macro2():
    assert library.get("testsuite") is not None


@with_setup(setup, teardown)
def test_get_macro3():
    assert library.get("testsuite").name == "testsuite"


@with_setup(setup, teardown)
def test_new_macro():
    assert type(library.get("testsuite")).__name__ == "Macro"


@with_setup(setup, teardown)
def test_remove_macro1():
    library.remove_macro("testsuite")
    assert library.get("testsuite") is None


@with_setup(setup, teardown)
def test_remove_macro2():
    fp = library.get("testsuite").filepath
    library.remove_macro("testsuite")
    assert os.path.exists(fp) is False


@with_setup(setup, teardown)
def test_save_macro():
    assert library.save_macro("testsuite")


@with_setup(setup, teardown)
def test_reload():
    lenA = len(library)
    library.clear()
    library.reload()
    assert len(library) == lenA


def test_newrepo():
    new_repo = os.path.normpath(
        os.path.join(os.path.expanduser("~"), "temp_mauto"))
    if os.path.exists(new_repo):
        os.removedirs(new_repo)
    Lib(new_repo)
    r = os.path.exists(new_repo)
    os.removedirs(new_repo)
    assert r
