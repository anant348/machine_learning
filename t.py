# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 't.ui'
#
# Created: Thu Oct 20 06:27:44 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(416, 148)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(17, 50, 391, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Fetching Results From Server...", None, QtGui.QApplication.UnicodeUTF8))

