# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputs.ui'
#
# Created: Sat Aug 02 18:24:40 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(258, 239)
        Dialog.setWindowTitle("")
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name = QtGui.QLineEdit(Dialog)
        self.name.setObjectName("name")
        self.verticalLayout_2.addWidget(self.name)
        self.inputs = QtGui.QTableWidget(Dialog)
        self.inputs.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.inputs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.inputs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.inputs.setCornerButtonEnabled(False)
        self.inputs.setObjectName("inputs")
        self.inputs.setColumnCount(2)
        self.inputs.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.inputs.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.inputs.setHorizontalHeaderItem(1, item)
        self.inputs.horizontalHeader().setStretchLastSection(True)
        self.inputs.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.inputs)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.buttonBox, self.name)
        Dialog.setTabOrder(self.name, self.inputs)

    def retranslateUi(self, Dialog):
        self.inputs.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.inputs.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "Value", None, QtGui.QApplication.UnicodeUTF8))

