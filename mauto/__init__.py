import sys

from mauto import gui
from mauto.api import library


def show():
    gui.show()


def select_repo():
    gui.select_repo()


def list_macros():
    return library.macros.keys()


def new_macro(*arg, **kwds):
    return library.new_macro(*arg, **kwds)


def get_macro(name):
    return library.get(name)


def remove_macro(name):
    if library.get(name):
        library.remove_macro(name)


def save_macro(name):
    return library.save_macro(name)


def get_filepath(name):
    return library.get_filepath(name)


def __main__():
    app = gui.QtGui.QApplication(sys.argv)
    w = gui.Layout()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    __main__()
