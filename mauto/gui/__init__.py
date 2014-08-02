import os
import sys
import pkg_resources

from mauto.api.lib import library

try:
    from maya import OpenMayaUI
    from PySide import QtGui
    from shiboken import wrapInstance
    from mauto.gui.designer import Ui_MainWindow
except ImportError:
    class QtGui():
        QMainWindow = object  # placeholder


class Layout(QtGui.QMainWindow):
    # MODES[0]:Recorder, MODES[1]:Library
    MODES = ({"list": True, "rec_group": True, "filter": False,
              "actionClipboard": True, "actionRecord": True,
              "actionPause": True, "actionSave": True,
              "actionShowLibrary": True, "actionPlay": False,
              "actionRemove": False, "actionShowRecorder": False, },
             {"list": True, "rec_group": False, "filter": True,
              "actionClipboard": False, "actionRecord": False,
              "actionPause": False, "actionSave": False,
              "actionShowLibrary": False, "actionPlay": True,
              "actionRemove": True, "actionShowRecorder": True, })

    IMAGES = {"record": "iconmonstr-microphone-3-icon-256.png",
              "pause": "pause-2-icon-256.png", }

    def __init__(self, *args, **kwds):
        super(Layout, self).__init__(*args, **kwds)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # update window title
        try:
            _version = pkg_resources.get_distribution("mauto").version
            self.setWindowTitle("mauto v%s" % _version)
        except:
            pass
        # icons
        self.IMAGES = dict([(k, os.path.join(os.path.dirname(__file__), "images", v))
                           for k, v in self.IMAGES.iteritems()])
        self.ICONS = dict([(k, QtGui.QIcon(v))
                          for k, v in self.IMAGES.iteritems()])
        # connect signals
        self.ui.filter.textChanged.connect(self.filter_list)
        self.ui.button.clicked.connect(self.btn_clicked)
        # menues signals
        self.ui.actionRecord.triggered.connect(self.record)
        self.ui.actionPause.triggered.connect(self.pause)
        self.ui.actionRemove.triggered.connect(self.remove_macro)
        self.ui.actionShowRecorder.triggered.connect(
            lambda x=0: self.set_mode(x))
        self.ui.actionShowLibrary.triggered.connect(
            lambda x=1: self.set_mode(x))
        self.ui.button.setIcon(self.ICONS.get("record"))
        # fill list
        self.ui.list.addItems(library.keys())
        # init mode
        self.set_mode(0)

    def set_mode(self, index):
        self._mode = index
        for k, v in self.MODES[index].iteritems():
            getattr(self.ui, k).setVisible(v)

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

    def record(self):
        if not hasattr(self, "_recording"):
            self.new()
        self.ui.button.setIcon(self.ICONS.get("pause"))
        stylesheet = "border: 2px solid; border-color: rgb(255, 0, 0);"
        self.ui.list.setStyleSheet(stylesheet)
        self._recording = not self._recording

    def new(self):
        self._recording = True
        # start a new macro


def get_parent():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Layout()
    w.show()
    sys.exit(app.exec_())
