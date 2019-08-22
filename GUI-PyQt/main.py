import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import random
import numpy as np
from mplwidget import MplWidget

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        
        QtWidgets.QDialog.__init__(self)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        loadUi(os.path.join(ui_path,"ui/Main.ui"),self)
        self.bDeapthPlus.clicked.connect(self.update_graph)


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


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = Dialog()
    window.show()
    sys.exit(app.exec_())
