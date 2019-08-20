# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\GUI-PyQt\Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(866, 605)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tabHome = QtWidgets.QWidget()
        self.tabHome.setObjectName("tabHome")
        self.tabWidget.addTab(self.tabHome, "")
        self.tabDataView = QtWidgets.QWidget()
        self.tabDataView.setObjectName("tabDataView")
        self.gridLayout = QtWidgets.QGridLayout(self.tabDataView)
        self.gridLayout.setObjectName("gridLayout")
        self.f11 = QtWidgets.QFrame(self.tabDataView)
        self.f11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f11.setObjectName("f11")
        self.gridLayout.addWidget(self.f11, 0, 0, 1, 1)
        self.f22 = QtWidgets.QFrame(self.tabDataView)
        self.f22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f22.setObjectName("f22")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.f22)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 245, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.f22, 1, 1, 1, 1)
        self.f21 = QtWidgets.QFrame(self.tabDataView)
        self.f21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f21.setObjectName("f21")
        self.gridLayout.addWidget(self.f21, 1, 0, 1, 1)
        self.f12 = QtWidgets.QFrame(self.tabDataView)
        self.f12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f12.setObjectName("f12")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.f12)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.bDeapthMinus = QtWidgets.QPushButton(self.f12)
        self.bDeapthMinus.setObjectName("bDeapthMinus")
        self.gridLayout_4.addWidget(self.bDeapthMinus, 0, 0, 1, 1)
        self.lDeapthPrice = QtWidgets.QLabel(self.f12)
        self.lDeapthPrice.setTextFormat(QtCore.Qt.AutoText)
        self.lDeapthPrice.setAlignment(QtCore.Qt.AlignCenter)
        self.lDeapthPrice.setObjectName("lDeapthPrice")
        self.gridLayout_4.addWidget(self.lDeapthPrice, 0, 1, 1, 1)
        self.bDeapthPlus = QtWidgets.QPushButton(self.f12)
        self.bDeapthPlus.setObjectName("bDeapthPlus")
        self.gridLayout_4.addWidget(self.bDeapthPlus, 0, 2, 1, 1)
        self.gVDeapthChart = QtWidgets.QGraphicsView(self.f12)
        self.gVDeapthChart.setObjectName("gVDeapthChart")
        self.gridLayout_4.addWidget(self.gVDeapthChart, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.f12, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tabDataView, "")
        self.tabConfig = QtWidgets.QWidget()
        self.tabConfig.setObjectName("tabConfig")
        self.tabWidget.addTab(self.tabConfig, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Bitpanda GE Data Viewer"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabHome), _translate("Dialog", "Home"))
        self.bDeapthMinus.setText(_translate("Dialog", "-"))
        self.lDeapthPrice.setText(_translate("Dialog", "10€"))
        self.bDeapthPlus.setText(_translate("Dialog", "+"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDataView), _translate("Dialog", "DataView"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabConfig), _translate("Dialog", "Config"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
