# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\GUI-PyQt\Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import random
import numpy as np
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(866, 605)
        self.gridMainWindow = QtWidgets.QGridLayout(Dialog)
        self.gridMainWindow.setObjectName("gridMainWindow")
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
        self.gridDataView = QtWidgets.QGridLayout(self.tabDataView)
        self.gridDataView.setObjectName("gridDataView")
        self.f22 = QtWidgets.QFrame(self.tabDataView)
        self.f22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f22.setObjectName("f22")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.f22)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridDataView.addWidget(self.f22, 1, 1, 1, 1)
        self.f21 = QtWidgets.QFrame(self.tabDataView)
        self.f21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f21.setObjectName("f21")
        self.gridDataView.addWidget(self.f21, 1, 0, 1, 1)
        self.f11 = QtWidgets.QFrame(self.tabDataView)
        self.f11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f11.setObjectName("f11")
        self.gridDataView.addWidget(self.f11, 0, 0, 1, 1)
        self.f12 = QtWidgets.QFrame(self.tabDataView)
        self.f12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f12.setObjectName("f12")
        self.gridDeapthChart = QtWidgets.QGridLayout(self.f12)
        self.gridDeapthChart.setObjectName("gridDeapthChart")
        self.bDeapthMinus = QtWidgets.QPushButton(self.f12)
        self.bDeapthMinus.setObjectName("bDeapthMinus")
        self.gridDeapthChart.addWidget(self.bDeapthMinus, 0, 0, 1, 1)
        self.lDeapthPrice = QtWidgets.QLabel(self.f12)
        self.lDeapthPrice.setTextFormat(QtCore.Qt.AutoText)
        self.lDeapthPrice.setAlignment(QtCore.Qt.AlignCenter)
        self.lDeapthPrice.setObjectName("lDeapthPrice")
        self.gridDeapthChart.addWidget(self.lDeapthPrice, 0, 1, 1, 1)
        self.bDeapthPlus = QtWidgets.QPushButton(self.f12)
        self.bDeapthPlus.setDefault(False)
        self.bDeapthPlus.setFlat(False)
        self.bDeapthPlus.setObjectName("bDeapthPlus")
        self.bDeapthPlus.clicked.connect(self.update_graph)
        self.gridDeapthChart.addWidget(self.bDeapthPlus, 0, 2, 1, 1)
        self.mplDeapthChart = MplWidget(self.f12)
        self.mplDeapthChart.setObjectName("mplDeapthChart")
        self.gridDeapthChart.addWidget(self.mplDeapthChart, 1, 0, 1, 3)
        self.gridDataView.addWidget(self.f12, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tabDataView, "")
        self.tabConfig = QtWidgets.QWidget()
        self.tabConfig.setObjectName("tabConfig")
        self.tabWidget.addTab(self.tabConfig, "")
        self.gridMainWindow.addWidget(self.tabWidget, 0, 0, 1, 1)

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

    def update_graph(self):

        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)
        
        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.mplDeapthChart.canvas.axes.clear()
        self.mplDeapthChart.canvas.axes.plot(t, cosinus_signal)
        self.mplDeapthChart.canvas.axes.plot(t, sinus_signal)
        self.mplDeapthChart.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        self.mplDeapthChart.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.mplDeapthChart.canvas.draw()
from mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
