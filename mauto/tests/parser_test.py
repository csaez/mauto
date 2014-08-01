from ..api import parser as p


def test_rules1():
    assert isinstance(p.PARSING_RULES, dict)


def test_rules2():
    assert len(p.PARSING_RULES) >= 4


def test_rules3():
    result = ['base', 'setattr', 'select', 'createlocator']
    assert all([x in result for x in p.PARSING_RULES.keys()])


def test_cleanup1():
    log = 'selectMode -component ;'
    result = [('', [], {}, [])]  # null
    assert p.parse(log) == result


def test_cleanup2():
    log = 'MarkingMenuPopDown;'
    result = [('', [], {}, [])]  # null
    assert p.parse(log) == result


def test_base():
    log = "select -cl ;"
    assert p.parse(log) == [('select', [], {'cl': 1}, [])]


def test_base1():
    log = 'select -add locator1;'
    assert p.parse(log) == [('select', ['locator1'], {'add': 1}, [])]


def test_base2():
    log = 'select -add 0 locator1 locator2;'
    result = [('select', ['locator1', 'locator2'], {'add': 0}, [])]
    assert p.parse(log) == result


def test_base3():
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


def test_select3():
    log = 'select -add 0 -tgl 0 locator1 locator2;'
    result = [('select', ['locator1', 'locator2'], {'add': 0, 'tgl': 0}, [])]
    assert p.parse(log) == result


def test_select4():
    log = 'select -r 0 -cl locator1 locator2;'
    result = [('select', ['locator1', 'locator2'], {'r': 0, 'cl': 1}, [])]
    assert p.parse(log) == result


def test_setattr1():
    log = 'setAttr "locator1.rotateY" 0;'
    result = [('setAttr', ['locator1.rotateY', 0], {}, [])]
    assert p.parse(log) == result


def test_setattr2():
    log = 'setAttr "locator1.vector3" 0 0 0;'
    assert p.parse(log) == [
        ('setAttr', ['locator1.vector3', [0, 0, 0]], {}, [])]


def test_comment1():
    log = 'spaceLocator -p 0 0 0;\n// Result: locator1 //;'
    assert p.parse(log) == [
        ('spaceLocator', [], {'p': [0, 0, 0]}, ['locator1'])]


def test_comment():
    log = "// any kind of comment here"
    assert p.parse(log) == []
