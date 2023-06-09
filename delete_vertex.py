# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete_vertex.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from graph import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_delete_vertex(object):
    def setupUi(self, delete_vertex):
        delete_vertex.setObjectName("delete_vertex")
        delete_vertex.resize(349, 110)
        self.verticalLayout = QtWidgets.QVBoxLayout(delete_vertex)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(delete_vertex)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(delete_vertex)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(G.nodes)
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(delete_vertex)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(delete_vertex)
        self.buttonBox.accepted.connect(delete_vertex.accept) # type: ignore
        self.buttonBox.rejected.connect(delete_vertex.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(delete_vertex)

    def retranslateUi(self, delete_vertex):
        _translate = QtCore.QCoreApplication.translate
        delete_vertex.setWindowTitle(_translate("delete_vertex", "Удаление вершины"))
        self.label.setText(_translate("delete_vertex", "Выберите вершину для удаления:"))

    def show_data(self):
        return (self.comboBox.currentText())


def delete_vertex_dialog():
    global delete_vertex
    delete_vertex = QtWidgets.QDialog()
    ui = Ui_delete_vertex()
    ui.setupUi(delete_vertex)
    delete_vertex.show()

    if delete_vertex.exec():
        try:
            G.remove_node(ui.show_data())
            text_output.append("Вершина " + ui.show_data() + " удалена.")
        except:
            text_output.append("Неккоректный ввод.")