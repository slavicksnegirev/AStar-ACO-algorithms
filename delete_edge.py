# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete_edge.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from graph import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_delete_edge(object):
    def setupUi(self, delete_edge):
        delete_edge.setObjectName("delete_edge")
        delete_edge.resize(505, 110)
        self.verticalLayout = QtWidgets.QVBoxLayout(delete_edge)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(delete_edge)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(delete_edge)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(G.nodes)
        self.horizontalLayout.addWidget(self.comboBox)
        self.label_2 = QtWidgets.QLabel(delete_edge)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(delete_edge)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(G.nodes)
        self.horizontalLayout.addWidget(self.comboBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(delete_edge)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(delete_edge)
        self.buttonBox.accepted.connect(delete_edge.accept) # type: ignore
        self.buttonBox.rejected.connect(delete_edge.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(delete_edge)

    def retranslateUi(self, delete_edge):
        _translate = QtCore.QCoreApplication.translate
        delete_edge.setWindowTitle(_translate("delete_edge", "Разъединить вершины"))
        self.label.setText(_translate("delete_edge", "Начальная вершина:"))
        self.label_2.setText(_translate("delete_edge", "Конечная вершина:"))

    def show_data(self):
        return (self.comboBox.currentText(), self.comboBox_2.currentText())


def delete_edge_dialog():
    global delete_edge
    delete_edge = QtWidgets.QDialog()
    ui = Ui_delete_edge()
    ui.setupUi(delete_edge)
    delete_edge.show()

    if delete_edge.exec():
        try:
            G.remove_edge(ui.show_data()[0], ui.show_data()[1])
        except:
            text_output.append("Некорректный ввод.")
            return
        text_output.append("Вершина " + ui.show_data()[0] + " разъединена с вершиной " + ui.show_data()[1] + ".")