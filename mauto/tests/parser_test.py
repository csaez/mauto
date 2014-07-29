from ..api import parser as p


def test_rules1():
    assert isinstance(p.PARSING_RULES, dict)


def test_rules2():
    assert len(p.PARSING_RULES) >= 4


def test_rules3():
    r = ['base', 'setattr', 'select', 'createlocator']
    assert all([x in r for x in p.PARSING_RULES.keys()])


def test_cleanup1():
    l = 'selectMode -component ;'
    r = [('', [], {}, [])]  # null
    assert p.parse(l) == r


def test_cleanup2():
    l = 'MarkingMenuPopDown;'
    r = [('', [], {}, [])]  # null
    assert p.parse(l) == r


def test_base1():
    l = 'polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0.6151959098 -pvy 0.3039012501 -pvz -1.076895647 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 ;'
    r = [('polyExtrudeFacet', [],
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
    assert p.parse(l) == r


def test_select1():
    l = 'select -add locator1;'
    assert p.parse(l) == [('select', ['locator1'], {'add': 1}, [])]


def test_select2():
    l = 'select -add 0 locator1 locator2;'
    r = [('select', ['locator1', 'locator2'], {'add': 0}, [])]
    assert p.parse(l) == r


def test_select3():
    l = 'select -add 0 -tgl 0 locator1 locator2;'
    r = [('select', ['locator1', 'locator2'], {'add': 0, 'tgl': 0}, [])]
    assert p.parse(l) == r


def test_select4():
    l = 'select -r 0 -cl locator1 locator2;'
    r = [('select', ['locator1', 'locator2'], {'r': 0, 'cl': 1}, [])]
    assert p.parse(l) == r


def test_setattr1():
    l = 'setAttr "locator1.rotateY" 0;'
    r = [('setAttr', ['locator1.rotateY', 0], {}, [])]
    assert p.parse(l) == r

def test_comment1():
    l = """spaceLocator -p 0 0 0;
// Result: locator1 //;"""
    assert p.parse(l) == [('spaceLocator', [], {'p': [0, 0, 0]}, ['locator1'])]

def test_comment():
    l = "// any kind of comment here"
    assert p.parse(l) == []
