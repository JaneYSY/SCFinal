import GameControlPanel
import sys
from PyQt5.QtWidgets import *

# Transmission 和Run放一起了

class Transmission:
    def __init__(self,ui):
        self.ui = ui
        self.hostIP = 'localhost'
        self.port = 49289
        self.addr = (self.hostIP ,self.port)

    def send_command(self,command,value=None):
        tcp_client_socket = socket(AF_INET,SOCK_STREAM)
        tcp_client_socket.connect(self.addr)

        if value == None:
            value = 0

        data = command + ':' + str(value)
        tcp_client_socket.send(('%s\r\n' % data).encode(encoding='utf-8'))
        data = tcp_client_socket.recv(1024)
        result = data.decode('utf-8').strip()
        tcp_client_socket.close()
        return result
        """

        URL: https://pythonspot.com/python-network-sockets-programming-tutorial/

        """
    def setting(self):

        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = GameControlPanel.Ui_MainWindow()

    ui.setupUi(mainWindow)
    # transmission = Transmission(ui)
    Transmission.setting(ui)
    mainWindow.show()
    sys.exit(app.exec_())