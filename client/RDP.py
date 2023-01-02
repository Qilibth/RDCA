import socket

from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv
from NProtocol.networkprotocol import *
import threading
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        MainWindow.resize(240, 252)
        MainWindow.setFixedSize(MainWindow.size())

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.your_id_label = QtWidgets.QLabel(self.centralwidget)
        self.your_id_label.setGeometry(QtCore.QRect(20, 10, 91, 20))
        self.your_id_label.setAlignment(QtCore.Qt.AlignCenter)
        self.your_id_label.setObjectName("label")

        self.id_display_label = QtWidgets.QLabel(self.centralwidget)
        self.id_display_label.setGeometry(QtCore.QRect(20, 30, 91, 21))
        self.id_display_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.id_display_label.setObjectName("label_2")

        self.remote_id_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.remote_id_entry.setGeometry(QtCore.QRect(130, 30, 91, 20))
        self.remote_id_entry.setObjectName("lineEdit")

        self.remote_id_label = QtWidgets.QLabel(self.centralwidget)
        self.remote_id_label.setGeometry(QtCore.QRect(130, 10, 91, 20))
        self.remote_id_label.setAlignment(QtCore.Qt.AlignCenter)
        self.remote_id_label.setObjectName("label_3")

        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setGeometry(QtCore.QRect(20, 60, 201, 41))
        self.connect_button.setObjectName("pushButton")
        self.connect_button.clicked.connect(self.connect)

        self.info_panel = QtWidgets.QLabel(self.centralwidget)
        self.info_panel.setGeometry(QtCore.QRect(20, 119, 201, 111))
        self.info_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.info_panel.setAlignment(QtCore.Qt.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RDCA"))
        self.your_id_label.setText(_translate("MainWindow", "Your ID"))
        self.remote_id_label.setText(_translate("MainWindow", "Remote ID"))
        self.connect_button.setText(_translate("MainWindow", "Connect"))

    def connect(self):
        print(self.remote_id_entry.text())

class RDP_GUI:
    def __init__(self):
        app = QtWidgets.QApplication(argv)
        MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        MainWindow.show()

        self.connected = True

        # everything must be between this line and os._exit()



        os._exit(app.exec_())

    def socket_start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while not self.connected:
            try:
                self.server.connect(ADDR)
                self.send("Test")
                break
            except ConnectionRefusedError:
                pass

    def send(self, msg):
        if self.connected:
            msg_length = len(msg)
            send_msg_length = str(msg_length).encode(FORMAT)
            send_msg_length += b" " * (HEADER - msg_length)

            self.server.send(send_msg_length)
            self.server.send(msg.encode(FORMAT))
        else:
            return None

rdp = RDP_GUI()