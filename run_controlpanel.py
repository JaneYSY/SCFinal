import ControlPanel
import sys
from PyQt5 import QtWidgets
import socket

class Transmission:
    def __init__(self,ui):
        self.ui = ui
        self.host = 'localhost'
        self.port = 6589
        self.addr = (self.host, self.port)

    def send(self, command, value=None):
        tcp_client_socket = socket.socket(AF_INET, SOCK_STREAM)
        tcp_client_socket.connect(self.addr)
        if value is None:
            value = 0
        data = command + ':' + str(value)
        tcp_client_socket.send(('&s\r\n' % data).encode(encoding='utf-8'))
        data = tcp_client_socket.recv(1024)
        result = data.decode('utf-8').strip()
        tcp_client_socket.close()
        return result

    def setup(self):
        self.ui.BedUpdate.clicked.connect(self.update_Bed)
        self.ui.TransUpdate.clicked.connect(self.update_Trans)
        self.ui.DistUpdate.clicked.connect(self.update_Dist)
        self.ui.ExitGame.clicked.connect(self.close)

    def update_Bed(self):
        self.send('add_iso_beds', self.ui.BedBox.value())


    def update_Trans(self):
        self.send('set_trans_prob', self.ui.TransBox.value())

    def update_Dist(self):
        self.send('set_travel_mean', self.ui.DistBox.value())

    def close(self):
        self.send('close')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = ControlPanel.Ui_MainWindow()
    ui.setupUi(mainWindow)
    transmission = Transmission(ui)
    transmission.setup()
    mainWindow.show()
    sys.exit(app.exec_())
