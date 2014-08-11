import os
import sys
import pkg_resources

from mauto.api.lib import library

try:
    from mauto.gui.mainwindow import Ui_MainWindow
    from PySide import QtGui, QtCore
    from shiboken import wrapInstance
except ImportError:
    class QtGui():
        QMainWindow = object
try:
    from maya import OpenMayaUI
except ImportError:
    pass


class Layout(QtGui.QMainWindow):
    IMAGES = {"play": "iconmonstr-video-play-icon-256.png",
              "stop": "iconmonstr-stop-2-icon-256.png",
              "record": "iconmonstr-microphone-3-icon-256.png",
              "add": "iconmonstr-plus-4-icon-256.png"}

    def __init__(self, *args, **kwds):
        super(Layout, self).__init__(*args, **kwds)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        # args
        self.IMAGES = dict([(k, os.path.join(os.path.dirname(__file__), "images", v))
                           for k, v in self.IMAGES.iteritems()])
        self.ICONS = dict([(k, QtGui.QIcon(v))
                          for k, v in self.IMAGES.iteritems()])
        self._state = 2  # 0: record, 1: stop, 2:play
        # connect signals
        self.ui.filter.textChanged.connect(self.filter_changed)
        self.ui.filter.returnPressed.connect(self.filter_entered)
        self.ui.action.clicked.connect(self.action_clicked)
        self.ui.macros.itemSelectionChanged.connect(self.macros_changed)
        self.ui.macros.itemClicked.connect(self.macros_changed)
        self.ui.macros.itemDoubleClicked.connect(self.play)
        QtGui.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Delete), self, self.remove_macro)
        # init ui
        try:
            _version = pkg_resources.get_distribution("mauto").version
            self.setWindowTitle("mauto v%s" % _version)
        except:
            pass
        self.list_macros()
        self.filter_changed("")

    @property
    def state(self):
        if hasattr(self, "_state"):
            return self._state

    @state.setter
    def state(self, value):
        self._state = value
        _icon = self.ICONS.get(("add", "stop", "play")[self._state])
        self.ui.action.setIcon(_icon)
        css = "#MainWindow{border: 2px solid;border-color:rgb(255,0,0);}" if self._state == 1 else ""
        self.setStyleSheet(css)

    def list_macros(self):
        self.ui.macros.setRowCount(len(library))
        for i, m in enumerate(library.values()):
            item = QtGui.QTableWidgetItem()
            item.setText(m.name)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.ui.macros.setItem(i, 0, item)

    def list_inputs(self):
        if not self.curr_macro:
            return
        self.ui.inputs.setRowCount(len(self.curr_macro.inputs))
        for row, items in enumerate(self.curr_macro.inputs.iteritems()):
            for column, value in enumerate(items):
                item = QtGui.QTableWidgetItem()
                item.setText(value)
                if column == 0:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.ui.inputs.setItem(row, column, item)

    def filter_changed(self, text):
        match = False
        for i in range(self.ui.macros.rowCount()):
            item = self.ui.macros.item(i, 0)
            match = True if text == item.text() else match
            self.ui.macros.setRowHidden(i, text not in item.text())
        self.state = 2 if match else 0

    def filter_entered(self):
        name = self.ui.filter.text()
        if not len(name):
            return
        for i in range(self.ui.macros.rowCount()):
            item = self.ui.macros.item(i, 0)
            if item and item.text() == name:
                self.macros_changed(item)
                return
        self.action_clicked()

    def macros_changed(self):
        if not self.curr_macro:
            return
        self.list_inputs()
        self.state = 2

    def remove_macro(self):
        if not self.curr_macro:
            return
        n = self.curr_macro.name
        for i in range(self.ui.macros.rowCount()):
            curr_item = self.ui.macros.item(i, 0)
            if curr_item and curr_item.text() == n:
                self.ui.macros.removeRow(i)
                library.remove_macro(n)
                self.list_inputs()

    def action_clicked(self):
        if len(self.ui.filter.text()):
            (self.record, self.stop, self.play)[self.state]()
            return
        # fallback
        if self.curr_macro:
            self.play()

    def stop(self):
        self.state = 2
        self.list_inputs()
        if self.curr_macro:
            self.curr_macro.pause()
            library.save_macro(self.curr_macro.name)

    def record(self):
        name = self.ui.filter.text()
        # update ui
        self.state = 1
        item = QtGui.QTableWidgetItem(name)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.ui.macros.insertRow(0)
        self.ui.macros.setItem(0, 0, item)
        self.ui.macros.setCurrentItem(item)
        # macro stuff
        if library.get(name):
            library.remove_macro(name)
        m = library.new_macro(name)
        m.record()

    def play(self):
        if not self.curr_macro:
            return
        d = dict()
        for i in range(self.ui.inputs.rowCount()):
            k = self.ui.inputs.item(i, 0).text()
            v = self.ui.inputs.item(i, 1).text()
            if not len(v):
                v = k
            d[k] = v
        self.curr_macro.play(d)

    @property
    def curr_macro(self):
        curr_item = self.ui.macros.currentItem()
        return library.get(curr_item.text()) if curr_item else None


def get_parent():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Layout()
    w.show()
    sys.exit(app.exec_())
