import os
import mock
from nose import with_setup
from ..api import macro
from ..api.lib import library


def setup_empty():
    library.new_macro("testsuite")


def setup_fromlog():
    log = """select -r joint1.rotatePivot ;
select -add joint3.rotatePivot ;
ikHandle -sol ikRPsolver ;
// Result: ikHandle1 effector1 //
select -r locator1 ;
select -add joint1 ;
parent;
// Result: locator1 //
setAttr "locator1.rotateZ" 0;
setAttr "locator1.translateX" 0;
setAttr "locator1.translateY" 0;
setAttr "locator1.translateZ" 0;
setAttr "locator1.rotateX" 0;
setAttr "locator1.rotateY" 0;
select -r locator1 ;
parent -w;
// Result: locator1 //
TranslateToolWithSnapMarkingMenu;
MarkingMenuPopDown;
move -r -os -wd 0 0 9.927413 ;
select -tgl ikHandle1 ;
poleVectorConstraint -weight 1;
// Result: ikHandle1_poleVectorConstraint1 // """
    library.new_macro("testsuite", log)


def teardown():
    n = "testsuite"
    if library.get(n):
        library.remove_macro(n)


def test_valid():
    assert macro.Macro.is_valid("invalid_data") == False


def test_valid1():
    assert macro.Macro.is_valid({"filetype": "mauto_macro"}) == False


@with_setup(setup_empty, teardown)
def test_valid2():
    d = library.get("testsuite").serialize()
    assert macro.Macro.is_valid(d) == True


@with_setup(setup_empty, teardown)
def test_fromfile():
    d = library.get("testsuite").serialize()
    assert macro.Macro.from_data(d) is not None


@with_setup(setup_empty, teardown)
def test_record():
    with mock.patch("mauto.api.macro.mc", create=True):
        m = library.get("testsuite")
        m.record()
        assert m.recording == True


@with_setup(setup_fromlog, teardown)
def test_fromlog():
    assert library.get("testsuite") is not None


@with_setup(setup_fromlog, teardown)
def test_inputs():
    m = library.get("testsuite")
    assert m.inputs.keys() == ['joint3.rotatePivot', 'joint1', 'locator1']


@with_setup(setup_fromlog, teardown)
def test_play():
    with mock.patch("mauto.api.macro.mc", create=True) as mc:
        # mock all the things!
        mc.ikHandle.return_value = ["ikHandle1", "effector1"]
        mc.poleVectorConstraint.return_value = "ikHandle1_poleVectorConstraint1"
        # test
        m = library.get("testsuite")
        assert m.play() == True


def setup_logfile():
    setup_empty()
    # setup
    m = library.get("testsuite")
    filepath = m.filepath.replace("testsuite.json", "temp.txt")
    with open(filepath, "w") as fp:
        fp.write("select -r locator1 ;")


def teardown_logfile():
    m = library.get("testsuite")
    filepath = m.filepath.replace("testsuite.json", "temp.txt")
    os.remove(filepath)
    teardown()


@with_setup(setup_logfile, teardown_logfile)
def test_stop():
    m = library.get("testsuite")
    filepath = m.filepath.replace("testsuite.json", "temp.txt")
    with mock.patch("mauto.api.macro.mc", create=True) as mc:
        mc.scriptEditorInfo.return_value = filepath
        m.record()
        m.stop()
        assert m.actions == [('select', ['locator1'], {'r': 1}, [])]


@with_setup(setup_logfile, teardown_logfile)
def test_pause1():
    m = library.get("testsuite")
    filepath = m.filepath.replace("testsuite.json", "temp.txt")
    with mock.patch("mauto.api.macro.mc", create=True) as mc:
        mc.scriptEditorInfo.return_value = filepath
        m = library.get("testsuite")
        m.record()
        m.pause()
        assert m.recording == False


@with_setup(setup_empty, teardown)
def test_pause2():
    m = library.get("testsuite")
    m.pause()
    assert m.recording == False
