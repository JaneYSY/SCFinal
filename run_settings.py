from PyQt5 import QtWidgets
import ControlPanel
import sys
from run_main import Transmission
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = ControlPanel.Ui_MainWindow()
    ui.setupUi(mainWindow)
    transmission = Transmission(ui)
    transmission.setup()
    mainWindow.show()
    sys.exit(app.exec_())
