from ..api import library as lib


def test_macros():
    assert isinstance(lib.macros(), set)


def test_list_macros():
    assert len(lib.list_macros()) == len(lib.macros())


def test_get_macro1():
    n = "macro_testsuite"
    assert lib.get_macro(n) is None


def test_get_macro2():
    n = "macro_testsuite"
    lib.new_macro(n)
    r = lib.get_macro(n) is not None
    lib.remove_macro(n)
    assert r


def test_get_macro3():
    n = "macro_testsuite"
    lib.new_macro(n)
    r = lib.get_macro(n).name == n
    lib.remove_macro(n)
    assert r


def test_new_macro():
    n = "macro_testsuite"
    m = lib.new_macro(n)
    r = type(m).__name__ == "Macro"
    lib.remove_macro(n)
    assert r


def test_remove_macro():
    n = "macro_testsuite"
    lib.new_macro(n)
    lib.remove_macro(n)
    assert n not in lib.list_macros()
