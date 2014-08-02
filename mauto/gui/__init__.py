import os
import sys
import time
import pkg_resources

from mauto.api.lib import library

try:
    from maya import OpenMayaUI
    from PySide import QtGui, QtCore
    from shiboken import wrapInstance
    from mauto.gui.main import Ui_MainWindow
    from mauto.gui.inputs import Ui_Dialog
except ImportError:
    # stabs
    class QtGui():
        QMainWindow = QDialog = object


class Layout(QtGui.QMainWindow):
    # MODES[0]:Recorder, MODES[1]:Library
    MODES = ({"list": True, "button": True, "filter": False,
              "actionClipboard": True, "actionRecord": True,
              "actionPause": True, "actionSave": True,
              "actionShowLibrary": True, "actionPlay": False,
              "actionRemove": False, "actionShowRecorder": False, },
             {"list": True, "button": False, "filter": True,
              "actionClipboard": False, "actionRecord": False,
              "actionPause": False, "actionSave": False,
              "actionShowLibrary": False, "actionPlay": True,
              "actionRemove": True, "actionShowRecorder": True, })

    IMAGES = {"record": "iconmonstr-microphone-3-icon-256.png",
              "pause": "pause-2-icon-256.png",
              "window": "iconmonstr-script-8-icon-256.png"}

    def __init__(self, *args, **kwds):
        super(Layout, self).__init__(*args, **kwds)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        # args
        self.current_macro = None
        self.IMAGES = dict([(k, os.path.join(os.path.dirname(__file__), "images", v))
                           for k, v in self.IMAGES.iteritems()])
        self.ICONS = dict([(k, QtGui.QIcon(v))
                          for k, v in self.IMAGES.iteritems()])
        # update window title
        try:
            _version = pkg_resources.get_distribution("mauto").version
            self.setWindowTitle("mauto v%s" % _version)
        except:
            pass
        self.setWindowIcon(self.ICONS.get("window"))
        # connect signals
        self.ui.filter.textChanged.connect(self.filter_list)
        self.ui.button.clicked.connect(self.btn_clicked)
        # menues signals
        self.ui.actionRecord.triggered.connect(self.record)
        self.ui.actionPause.triggered.connect(self.pause)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionRemove.triggered.connect(self.remove_macro)
        self.ui.actionShowRecorder.triggered.connect(
            lambda x=0: self.set_mode(x))
        self.ui.actionShowLibrary.triggered.connect(
            lambda x=1: self.set_mode(x))
        self.ui.button.setIcon(self.ICONS.get("record"))
        # init mode
        self.set_mode(0)

    def show_macros(self):
        self.ui.list.clear()
        self.ui.list.addItems(library.keys())

    def show_actions(self):
        self.ui.list.clear()
        if self.current_macro:
            _items = [unicode(x) for x in self.current_macro.actions]
            self.ui.list.addItems(_items)

    def set_mode(self, index):
        # index == 0: Recorder, index==1: Library
        self._mode = index
        for k, v in self.MODES[index].iteritems():
            getattr(self.ui, k).setVisible(v)
        if self._mode:
            self.close_recorder()
            self.show_macros()
        else:
            self.show_actions()

    def close_recorder(self):
        if hasattr(self, "_recording"):
            del self._recording
        if self.current_macro:
            library.remove_macro(self.current_macro.name)
            self.current_macro = None

    def filter_list(self, text):
        for i in range(self.ui.list.count()):
            item = self.ui.list.item(i)
            item.setHidden(text not in item.text())

    def remove_macro(self):
        item = self.ui.list.currentItem()
        if not item:
            return
        i = self.ui.list.row(item)
        n = item.text()
        self.ui.list.takeItem(i)
        library.remove_macro(n)

    def btn_clicked(self):
        if not hasattr(self, "_recording"):
            self.new()
        (self.record, self.pause)[int(not self._recording)]()

    def pause(self):
        if not hasattr(self, "_recording"):
            return
        self.ui.button.setIcon(self.ICONS.get("record"))
        self.ui.list.setStyleSheet("")
        self._recording = not self._recording
        # macro stuff
        self.current_macro.pause()
        library.save_macro(self.current_macro.name)
        self.show_actions()

    def save(self):
        if self.current_macro:
            if Inputs.save(self.current_macro, parent=self):
                self.set_mode(1)

    def record(self):
        if not hasattr(self, "_recording"):
            self.new()
        self.ui.button.setIcon(self.ICONS.get("pause"))
        stylesheet = "border: 2px solid; border-color: rgb(255, 0, 0);"
        self.ui.list.setStyleSheet(stylesheet)
        self._recording = not self._recording
        # macro stuff
        self.current_macro.record()

    def new(self):
        self._recording = True
        # start a new macro
        self.current_macro = library.new_macro(str(int(time.time())))

    def closeEvent(self, event):
        self.close_recorder()
        super(Layout, self).closeEvent(event)


class Inputs(QtGui.QDialog):

    def __init__(self, macro, *args, **kwds):
        super(Inputs, self).__init__(*args, **kwds)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # args
        self.macro = macro
        # signals
        self.ui.name.textChanged.connect(self.validate_name)
        self.validate_name(self.ui.name.text())

    @classmethod
    def play(cls, macro, *args, **kwds):
        d = cls(macro, *args, **kwds)
        d.setWindowTitle("Inputs editor")
        d.ui.name.setVisible(False)
        result = d.exec_()
        if result:
            macro.play(d.refs)
        return result

    @classmethod
    def save(cls, macro, *args, **kwds):
        d = cls(macro, *args, **kwds)
        d.setWindowTitle("Save macro as...")
        d.ui.name.setFocus()
        result = d.exec_()
        if result:
            name = d.ui.name.text()
            m = library.new_macro(name)
            m.deserialize(macro.serialize())
            library.save_macro(name)
        del d  # release macro instance
        return result

    def validate_name(self, text):
        stylesheet = "border: 2px solid; border-color: rgb(255, 0, 0);"
        is_valid = library.get(text) is None and len(text)
        self.ui.name.setStyleSheet("" if is_valid else stylesheet)
        return is_valid

    def accept(self):
        if self.ui.name.isVisible():
            if self.validate_name(self.ui.name.text()):
                super(Inputs, self).accept()
        else:
            super(Inputs, self).accept()


def get_parent():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Layout()
    w.show()
    sys.exit(app.exec_())
