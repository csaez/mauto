import mock
from nose import with_setup
from ..api import macro
from ..api.lib import library

DEFAULT = mock.sentinel.DEFAULT
patcher = mock.patch.multiple("mauto.api.macro", create=True,
                              cmds=DEFAULT, mel=DEFAULT)


def setup_patch():
    patcher.start()


def teardown_patch():
    try:
        patcher.stop()
    except RuntimeError:
        pass


def setup_empty():
    setup_patch()
    library.new_macro("testsuite")


def setup_fromlog():
    setup_patch()
    log = """select -r joint1.rotatePivot ;
select -add joint3.rotatePivot ;
ikHandle -sol ikRPsolver ;
// ikHandle1 effector1 //
select -r locator1 ;
select -add joint1 ;
parent;
// locator1 //
setAttr "locator1.rotateZ" 0;
setAttr "locator1.translateX" 0;
setAttr "locator1.translateY" 0;
setAttr "locator1.translateZ" 0;
setAttr "locator1.rotateX" 0;
setAttr "locator1.rotateY" 0;
select -r locator1 ;
parent -w;
// locator1 //
move -r -os -wd 0 0 9.927413 ;
select -tgl ikHandle1 ;
poleVectorConstraint -weight 1;
// ikHandle1_poleVectorConstraint1 //"""
    library.new_macro("testsuite", log)


def teardown():
    n = "testsuite"
    if library.get(n):
        library.remove_macro(n)
    teardown_patch()


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
    macro.cmds.scriptJob.return_value = 0
    m = library.get("testsuite")
    m.record()
    assert m.recording == True


@with_setup(setup_fromlog, teardown)
def test_fromlog():
    print "lalala!!!!"
    macro.cmds.scriptJob.return_value = list()
    assert library.get("testsuite") is not None


@with_setup(setup_fromlog, teardown)
def test_inputs():
    macro.cmds.scriptJob.return_value = list()
    m = library.get("testsuite")
    print m.actions, m.inputs
    assert m.inputs == ['joint3', 'joint1', 'locator1']


@with_setup(setup_fromlog, teardown)
def test_play():
    # mock all the things!
    macro.cmds.scriptJob.return_value = list()
    macro.cmds.ikHandle.return_value = ["ikHandle1", "effector1"]
    macro.cmds.poleVectorConstraint.return_value = "ikHandle1_poleVectorConstraint1"
    return_values = {"ikHandle -sol ikRPsolver ;": ("ikHandle1", "effector1"),
                     "poleVectorConstraint -weight 1;": "ikHandle1_poleVectorConstraint1"}
    macro.mel.eval.side_effect = lambda x: return_values.get(x)
    # test
    m = library.get("testsuite")
    assert m.play() == True


@with_setup(setup_empty, teardown)
def test_pause():
    macro.cmds.scriptJob.return_value = list()
    macro.cmds.scriptEditorInfo.return_value = library.get_filepath(
        "testsuite")
    m = library.get("testsuite")
    m.recording = True
    m.pause()
    assert m.recording == False


@with_setup(setup_empty, teardown)
def test_pause2():
    macro.cmds.scriptJob.return_value = list()
    m = library.get("testsuite")
    m.pause()
    assert m.recording == False


@with_setup(setup_patch, teardown_patch)
def test_mauto_job():
    macro.cmds.ls.return_value = ("testsuite",)
    assert macro.mauto_job is not None
    assert "testsuite" in macro.mauto_job()
