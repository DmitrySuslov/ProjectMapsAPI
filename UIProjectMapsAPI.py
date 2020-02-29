# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIProjectMapsAPI.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProjectMapsAPI(object):
    def setupUi(self, ProjectMapsAPI):
        ProjectMapsAPI.setObjectName("ProjectMapsAPI")
        ProjectMapsAPI.resize(750, 600)
        self.centralwidget = QtWidgets.QWidget(ProjectMapsAPI)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(610, 130, 131, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(610, 100, 121, 20))
        self.label.setObjectName("label")
        ProjectMapsAPI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ProjectMapsAPI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 21))
        self.menubar.setObjectName("menubar")
        ProjectMapsAPI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ProjectMapsAPI)
        self.statusbar.setObjectName("statusbar")
        ProjectMapsAPI.setStatusBar(self.statusbar)

        self.retranslateUi(ProjectMapsAPI)
        QtCore.QMetaObject.connectSlotsByName(ProjectMapsAPI)

    def retranslateUi(self, ProjectMapsAPI):
        _translate = QtCore.QCoreApplication.translate
        ProjectMapsAPI.setWindowTitle(_translate("ProjectMapsAPI", "ProjectMapsAPI"))
        self.comboBox.setItemText(0, _translate("ProjectMapsAPI", "Схема"))
        self.comboBox.setItemText(1, _translate("ProjectMapsAPI", "Спутник"))
        self.comboBox.setItemText(2, _translate("ProjectMapsAPI", "Гибрид"))
        self.label.setText(_translate("ProjectMapsAPI", "Тип карты:"))
