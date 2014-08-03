from ..api import parser as p


def test_parsing_rules_type():
    assert isinstance(p.PARSING_RULES, dict)


def test_number_of_rules():
    assert len(p.PARSING_RULES) >= 4


def test_rules_exists():
    result = ['base', 'setattr', 'select', 'createlocator']
    assert all([x in result for x in p.PARSING_RULES.keys()])


def test_remove_banned_commands():
    assert p.parse("selectMode -component;") == p.parse(
        "MarkingMenuPopDown") == []


def test_select_clear_command():
    log = "select -cl ;"
    assert p.parse(log) == [('select', [], {'cl': 1}, [])]


def test_select_add_single():
    log = 'select -add locator1;'
    assert p.parse(log) == [('select', ['locator1'], {'add': 1}, [])]


def test_select_add_multi():
    log = 'select -add 0 locator1 locator2;'
    result = [('select', ['locator1', 'locator2'], {'add': 0}, [])]
    assert p.parse(log) == result


def test_multi_flag_command():
    log = 'polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0.6151959098 -pvy 0.3039012501 -pvz -1.076895647 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 ;'
    result = [('polyExtrudeFacet', [],
               {'divisions': 1,
                'off': 0,
                'taper': 1,
                'pvy': 0.3039012501,
                'pvx': 0.6151959098,
                'pvz': -1.076895647,
                'thickness': 0,
                'twist': 0,
                'smoothingAngle': 30,
                'keepFacesTogether': 1,
                'constructionHistory': 1},
             [])]
    assert p.parse(log) == result


def test_base_trailing_space():
    without_space = p.parse("parent;")
    with_space = p.parse("parent ;")
    print without_space, with_space
    assert with_space == without_space == [('parent', [], {}, [])]


def test_select_explicit_flag_values():
    log = 'select -add 0 -tgl 0 locator1 locator2;'
    result = [('select', ['locator1', 'locator2'], {'add': 0, 'tgl': 0}, [])]
    assert p.parse(log) == result


def test_select_implicit_flag_values():
    log = 'select -r 0 -cl locator1 locator2;'
    result = [('select', ['locator1', 'locator2'], {'r': 0, 'cl': 1}, [])]
    assert p.parse(log) == result


def test_setattr_command_single():
    log = 'setAttr "locator1.rotateY" 0;'
    result = [('setAttr', ['locator1.rotateY', 0], {}, [])]
    assert p.parse(log) == result


def test_setattr_command_vector3():
    log = 'setAttr "locator1.vector3" 0 0 0;'
    assert p.parse(log) == [
        ('setAttr', ['locator1.vector3', [0, 0, 0]], {}, [])]


def test_outputs():
    log = 'spaceLocator -p 0 0 0;\n// Result: locator1 //;'
    assert p.parse(log) == [
        ('spaceLocator', [], {'p': [0, 0, 0]}, ['locator1'])]


def test_ignore_comments():
    log = "// any kind of comment here"
    assert p.parse(log) == []
