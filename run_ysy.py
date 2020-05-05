import UIWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UIWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    
    sys.exit(app.exec_())

