# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ControlPanel.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(822, 327)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 40, 741, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.BedBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BedBox.sizePolicy().hasHeightForWidth())
        self.BedBox.setSizePolicy(sizePolicy)
        self.BedBox.setSuffix("")
        self.BedBox.setMinimum(50)
        self.BedBox.setMaximum(900)
        self.BedBox.setProperty("value", 200)
        self.BedBox.setDisplayIntegerBase(10)
        self.BedBox.setObjectName("BedBox")
        self.gridLayout_2.addWidget(self.BedBox, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.TransUpdate = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.TransUpdate.setFont(font)
        self.TransUpdate.setObjectName("TransUpdate")
        self.gridLayout_2.addWidget(self.TransUpdate, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 1, 1, 1)
        self.TransBox = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TransBox.sizePolicy().hasHeightForWidth())
        self.TransBox.setSizePolicy(sizePolicy)
        self.TransBox.setMaximum(1.0)
        self.TransBox.setSingleStep(0.01)
        self.TransBox.setProperty("value", 0.75)
        self.TransBox.setObjectName("TransBox")
        self.gridLayout_2.addWidget(self.TransBox, 2, 2, 1, 1)
        self.DistUpdate = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DistUpdate.setFont(font)
        self.DistUpdate.setObjectName("DistUpdate")
        self.gridLayout_2.addWidget(self.DistUpdate, 1, 0, 1, 1)
        self.BedUpdate = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.BedUpdate.setFont(font)
        self.BedUpdate.setObjectName("BedUpdate")
        self.gridLayout_2.addWidget(self.BedUpdate, 0, 0, 1, 1)
        self.DistBox = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
<<<<<<< HEAD:ControlPanel.py
        sizePolicy.setHeightForWidth(self.DistBox.sizePolicy().hasHeightForWidth())
        self.DistBox.setSizePolicy(sizePolicy)
        self.DistBox.setDecimals(1)
        self.DistBox.setMinimum(0.0)
        self.DistBox.setMaximum(100.0)
        self.DistBox.setSingleStep(0.5)
        self.DistBox.setProperty("value", 50.0)
        self.DistBox.setObjectName("DistBox")
        self.gridLayout_2.addWidget(self.DistBox, 1, 2, 1, 1)
        self.ExitGame = QtWidgets.QPushButton(self.centralwidget)
        self.ExitGame.setGeometry(QtCore.QRect(230, 330, 311, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ExitGame.setFont(font)
        self.ExitGame.setObjectName("ExitGame")
=======
        sizePolicy.setHeightForWidth(self.FlowIntentionBox.sizePolicy().hasHeightForWidth())
        self.FlowIntentionBox.setSizePolicy(sizePolicy)
        self.FlowIntentionBox.setDecimals(1)
        self.FlowIntentionBox.setMinimum(1.0)
        self.FlowIntentionBox.setMaximum(5.0)
        self.FlowIntentionBox.setSingleStep(0.5)
        self.FlowIntentionBox.setProperty("value", 5.0)
        self.FlowIntentionBox.setObjectName("FlowIntentionBox")
        self.gridLayout_2.addWidget(self.FlowIntentionBox, 1, 2, 1, 1)
>>>>>>> d32ab672b49d4ab5ae7e817c17769c740c0de9fe:GameControlPanel.py
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 822, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
<<<<<<< HEAD:ControlPanel.py
        self.label.setText(_translate("MainWindow", "Add Isolation Beds"))
        self.label_2.setText(_translate("MainWindow", " Update Mean Travel Dist"))
        self.TransUpdate.setText(_translate("MainWindow", "Update"))
        self.label_3.setText(_translate("MainWindow", "Update Trans Prob"))
        self.DistUpdate.setText(_translate("MainWindow", "Update"))
        self.BedUpdate.setText(_translate("MainWindow", "Update"))
        self.ExitGame.setText(_translate("MainWindow", "Exit Game"))
=======
        self.label.setText(_translate("MainWindow", "Isolation Beds"))
        self.label_2.setText(_translate("MainWindow", "Flow Intention"))
        self.InfectionRateUpdateButton.setText(_translate("MainWindow", "Update"))
        self.label_3.setText(_translate("MainWindow", "Infection Rate"))
        self.FlowIntentionUpdateButton.setText(_translate("MainWindow", "Update"))
        self.BedUpdateButton.setText(_translate("MainWindow", "Update"))
>>>>>>> d32ab672b49d4ab5ae7e817c17769c740c0de9fe:GameControlPanel.py


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

