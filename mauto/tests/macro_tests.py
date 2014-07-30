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
    assert Macro.is_valid("invalid_data") == False


def test_valid1():
    assert Macro.is_valid({"filetype": "mauto_macro"}) == False


@with_setup(setup, teardown)
def test_fromfile():
    d = mauto.get_macro("testsuite").serialize()
    assert Macro.from_data(d) is not None


@with_setup(setup, teardown)
def test_valid2():
    d = mauto.get_macro("testsuite").serialize()
    assert Macro.is_valid(d) == True


def test_pause1():
    m = Macro("testsuite")
    m.record()
    m.pause()
    assert m.recording == False


def test_pause2():
    m = Macro("testsuite")
    m.pause()
    assert m.recording == False
