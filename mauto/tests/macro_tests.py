import os
import mock
import mauto
from nose import with_setup
from ..api import macro


Macro = macro.Macro
macro.mc = mock.Mock()
macro.mc.scriptEditorInfo = mock.Mock()


def setup():
    mauto.new_macro("testsuite")


def teardown():
    mauto.remove_macro("testsuite")


def test_record():
    m = Macro("testsuite")
    m.record()
    assert m.recording == True


def test_valid():
    assert Macro.is_valid("invalid/file/path") == False


def test_valid1():
    fp = os.path.normpath(os.path.join(os.path.expanduser("~"), "temp.json"))
    with open(fp, "w") as f:
        f.write("invalid file contents")
    r = Macro.is_valid(fp) == False  # test
    os.remove(fp)
    assert r


@with_setup(setup, teardown)
def test_valid2():
    fp = mauto.get_macro("testsuite").filepath
    assert Macro.is_valid(fp) == True


# def test_pause():
#     m = Macro("testsuite")
#     m.record()
#     m.pause()
#     assert m.recording == False
