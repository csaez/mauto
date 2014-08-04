from ..api import parser as p


def test_regex_type():
    assert isinstance(p.REGEX, dict)


def test_number_of_regex():
    assert len(p.REGEX) >= 3


def test_regex_exists():
    result = ['general', 'attr', 'select']
    assert all([x in result for x in p.REGEX.keys()])


def test_remove_banned_commands():
    assert p.parse("CreateLocator;") == p.parse("MarkingMenuPopDown;") == []


def test_select_clear_command():
    log = "select -cl ;"
    assert p.parse(log) == [{"sloc": "select -cl ;",
                             "out": []}]


def test_select_add_single():
    log = 'select -add locator1;'
    assert p.get_deps(log) == ['locator1']


def test_select_add_multi():
    log = 'select -add 0 locator1 locator2;'
    result = ['locator1', 'locator2']
    assert all(x in p.get_deps(log) for x in result)


def test_multi_flag_command():
    log = 'polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0.6151959098 -pvy 0.3039012501 -pvz -1.076895647 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 ;'
    assert p.get_deps(log) == []


def test_setattr_command_single():
    log = 'setAttr "locator1.rotateY" 0;'
    assert p.get_deps(log) == ["locator1"]


def test_setattr_command_vector3():
    log = 'setAttr "locator1.vector3" 0 0 0;'
    assert p.get_deps(log) == ["locator1"]


def test_outputs():
    log = 'spaceLocator -p 0 0 0;\n// locator1 //'
    assert p.parse(log)[0]["out"] == ['locator1']


def test_ignore_comments():
    log = "// any kind of comment here"
    assert p.parse(log) == []

def test_str_to_list():
    assert p.str_to_list("foo") == ["foo"]
    assert p.str_to_list(" foo") == ["foo"]
    assert p.str_to_list("foo ") == ["foo"]
    assert p.str_to_list(" foo ") == ["foo"]
    assert p.str_to_list("foo bar") == ["foo", "bar"]
    assert p.str_to_list( "foo bar") == ["foo", "bar"]
    assert p.str_to_list("foo bar" ) == ["foo", "bar"]
    assert p.str_to_list( "foo bar" ) == ["foo", "bar"]
