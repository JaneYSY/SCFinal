import GameControlPanel
import sys
from PyQt5.QtWidgets import *
from socket import *
# Transmission 和Run放一起了


class Transmission:
    def __init__(self, ui):
        self.ui = ui
        self.hostIP = '127.0.0.1'
        self.port = 49289
        self.addr = (self.hostIP, self.port)

    def send_command(self, command, value=None):
        tcp_s = socket(AF_INET, SOCK_STREAM)
        tcp_s.bind(self.addr)
        buffer_size = 1024

        if value == None:
            value = 0

        data = command + ':' + str(value)
        tcp_s.send(('%s\r\n' % data).encode(encoding='chonk'))
        data = tcp_s.recv(buffer_size)
        result = data.decode('chonk').strip()
        tcp_s.close()

        return result
        """Reference
        Python network sockets programming tutorial
        URL: https://pythonspot.com/python-network-sockets-programming-tutorial/
        
        UR Script: Commands via Socket connection
        Author: Zacobria Universal-Robots community
        URL: https://www.zacobria.com/universal-robots-zacobria-forum-hints-tips-how-to/script-via-socket-connection/
        """

    def setting(self):
        self.ui.BedUpdateButton.clicked.connect(self.update_bed_number)

        self.ui.FlowIntentionUpdateButton.clicked.connect(
            self.update_flow_intention)

        self.ui.InfectionRateUpdateButton.clicked.connect(
            self.update_infection_rate)

        self.ui.ExitGame.clicked.connect(self.close_controlpanel)

    def update_bed_number(self):
        print(self.ui.BedValueBox.value())
        result = self.send_command(
            'add_bed', self.ui.BedValueBox.value())
        if result == 'ok':
            QMessageBox.information(self.ui.centralwidget, 'Notification', 
                f'{self.ui.horizontalSliderBedCount.value()} beds have been added successfully',
                QMessageBox.Ok)

    def update_flow_intention(self):
        result = self.send_command(
            'change_flow_intention', self.ui.FlowIntentionBox.value())
        if result == 'ok':
            QMessageBox.information(self.ui.centralwidget, 'Notification',
                                    f'Flow rate changed to {self.ui.FlowIntentionBox.value()}', QMessageBox.Ok)

    def update_infection_rate(self):
        result = self.send_command(
            'change_infection_rate', self.ui.InfectionRateBox.value())
        if result == 'ok':
            QMessageBox.information(self.ui.centralwidget, 'Notification',
                                    f'Infection rate changed to {self.ui.InfectionRateBox.value()}, \
                                    because of preventive actions are taken', QMessageBox.Ok)

    def close_controlpanel(self):
        reply = QMessageBox.information(self.ui.centralwidget, "Please Confirm", "Are you sure you want to exit \
            the game contro panel?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            result = self.send_command('close')
            if result == 'ok':
                QMessageBox.information(
                    self.ui.centralwidget, 'Notification', 'You have exited the game', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = GameControlPanel.Ui_MainWindow()

    ui.setupUi(mainWindow)
    transmission = Transmission(ui)
    transmission.setting()
    mainWindow.show()
    sys.exit(app.exec_())