from ..api import parser as p


def test_remove_banned_commands():
    p1 = p.Parse("CreateLocator;").actions
    p2 = p.Parse("MarkingMenuPopDown;").actions
    assert p1 == p2 == list()


def test_select_clear_command():
    log = "select -cl ;"
    assert p.Parse(log).actions == [{"sloc": "select -cl ;", "out": []}]


def test_select_add_single():
    log = 'select -add locator1;'
    assert p.Parse(log).inputs == ['locator1']


def test_select_add_multi():
    log = 'select -add 0 locator1 locator2;'
    result = ['locator1', 'locator2']
    assert all(x in p.Parse(log).inputs for x in result)


def test_multi_flag_command():
    log = 'polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0.6151959098 -pvy 0.3039012501 -pvz -1.076895647 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 ;'
    assert not len(p.Parse(log).references)  # no references


def test_setattr_command_single():
    log = 'setAttr "locator1.rotateY" 0;'
    assert "locator1" in p.Parse(log).references


def test_setattr_command_vector3():
    log = 'setAttr "locator1.vector3" 0 0 0;'
    assert "locator1" in p.Parse(log).references


def test_outputs():
    log = 'spaceLocator -p 0 0 0;\n// locator1 //'
    assert p.Parse(log).actions[0]["out"] == ['locator1']


def test_ignore_comments():
    log = "// any kind of comment here"
    assert p.Parse(log).actions == []


def test_str_to_list():
    assert p.str_to_list("foo") == ["foo"]
    assert p.str_to_list(" foo") == ["foo"]
    assert p.str_to_list("foo ") == ["foo"]
    assert p.str_to_list(" foo ") == ["foo"]
    assert p.str_to_list("foo bar") == ["foo", "bar"]
    assert p.str_to_list("foo bar") == ["foo", "bar"]
    assert p.str_to_list("foo bar") == ["foo", "bar"]
    assert p.str_to_list("foo bar") == ["foo", "bar"]


def setup_simplelog():
    return """CreateLocator;
spaceLocator -p 0 0 0;
// locator1 //
// locatorShape1 //
CreateLocator;
spaceLocator -p 0 0 0;
// locator2 locatorShape2 //
TranslateToolWithSnapMarkingMenu;
MarkingMenuPopDown;
move -r 1.780128 3.387885 -4.321042 ;
select -cl  ;
select -r locator1 ;
select -r locatorShape1 ;
select -r locatorShape2 ;
select -r locatorShape1 ;
nodeOutliner -e -replace locatorShape1 connectWindowModal|tl|cwForm|connectWindowPane|rightSideCW;
// connectWindowModal|tl|cwForm|connectWindowPane|rightSideCW //
select -r locatorShape2 ;
connectAttr -force locatorShape1.localPosition locatorShape2.localScale;
// Connected locatorShape1.localPosition to locatorShape2.localScale. //
select -r pCube1 ;"""


def test_multi_outputs():
    r = set([x for a in p.Parse(setup_simplelog()).actions for x in a.get("out")])
    assert r == set(("locator1", "locatorShape1", "locator2", "locatorShape2"))


def test_banned_cmds():
    for x in p.Parse(setup_simplelog()).actions:
        assert not x["sloc"].startswith("nodeOutliner")


def test_global_input():
    print p.Parse(setup_simplelog()).inputs
    assert p.Parse(setup_simplelog()).inputs == ["pCube1"]


def test_connect_attr():
    logs = (
        "connectAttr -force locatorShape1.localPosition locatorShape2.localScale;",
        "connectAttr locatorShape1.localPosition locatorShape2.localScale;",
        "connectAttr locatorShape1 locatorShape2;",
    )
    for log in logs:
        deps = p.Parse(log).references
        for x in ("locatorShape1", "locatorShape2"):
            assert x in deps


def test_references():
    parsed = p.Parse(setup_simplelog())
    expected_results = ("locator1", "locatorShape1",
                        "locator2", "locatorShape2", "pCube1")
    for x in expected_results:
        assert x in parsed.references
