from PyQt5 import QtCore, QtGui, QtWidgets
from networkprotocol import *
from sys import argv
from os import _exit
import socket
import time
import threading


class SignUp(object):
    def __init__(self):
        self.connected = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(196, 212)
        MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        MainWindow.setFixedSize(MainWindow.size())

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.id_label = QtWidgets.QLabel(self.centralwidget)
        self.id_label.setGeometry(QtCore.QRect(40, 10, 111, 20))
        self.id_label.setAlignment(QtCore.Qt.AlignCenter)
        self.id_label.setObjectName("id_label")

        self.id_input = QtWidgets.QLineEdit(self.centralwidget)
        self.id_input.setGeometry(QtCore.QRect(30, 30, 131, 31))
        self.id_input.setObjectName("id_input")

        self.sign_up_button = QtWidgets.QPushButton(self.centralwidget)
        self.sign_up_button.setGeometry(QtCore.QRect(60, 70, 75, 23))
        self.sign_up_button.setObjectName("sign_up_button")
        self.sign_up_button.clicked.connect(self.sign_up_clicked)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 112, 111, 71))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sign Up Window"))
        self.id_label.setText(_translate("MainWindow", "ID"))
        self.sign_up_button.setText(_translate("MainWindow", "Sign In"))
        self.label.setText(_translate("MainWindow", "Connection Status :"))

    def sign_up_clicked(self):
        id_input = self.id_input.text()
        if id_input == "" or " " in id_input:
            self.label.setText("Invalid input")
        elif not self.connected:
            self.label.setText("Not Connected\nTo Server")
        else:
            self.send(f"{SIGNUP}//{id_input}")
            data = self.recv()
            self.server_msg_chcecK(data[0], data[1])

    def server_msg_chcecK(self, command, value):
        # msg sent from server checking
        if command == SIGNUP_RESULT:
            if eval(value):
                self.label.setText("ID Set Successfully.\nClose And Reopen\nApplication.")
                self.sign_up_button.setEnabled(False)

                with open("client_data.json", "r") as client_data_file:
                    data = json.load(client_data_file)
                    data["HasID"] = True
                    data["ID"] = self.id_input.text()

                with open("client_data.json", "w") as client_data_file:
                    json.dump(data, client_data_file, indent=4)
                    print(data)

            elif not eval(value):
                self.label.setText("ID Invalid")
        print(value)


    def socket_start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not self.connected:
            try:
                self.server.connect(ADDR)
                self.label.setText("Connection Status:\nConnected")
                self.connected = True
                break
            except ConnectionRefusedError:
                self.label.setText("Connection Status:\nAttempting...")

    def send(self, msg):
        if self.connected:
            msg_length = len(msg)
            send_msg_length = str(msg_length).encode(FORMAT)
            send_msg_length += b" " * (HEADER - msg_length)

            self.server.send(send_msg_length)
            time.sleep(0.2)  # this is required otherwise the sent messages will interfere with each other
            self.server.send(msg.encode(FORMAT))
        else:
            pass

    def recv(self):
        msg_length = self.server.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = self.server.recv(msg_length).decode(FORMAT)

            try:
                command, value = msg.split("//")
            except Exception:
                command, value = None, None

            return (command, value)



# socket begin
def main():
    app = QtWidgets.QApplication(argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = SignUp()
    ui.setupUi(MainWindow)

    MainWindow.show()

    # everything must be between this line and os._exit()
    socket_thread = threading.Thread(target=ui.socket_start)
    socket_thread.start()

    if app.exec_() == 0:
        ui.send(f"{DISCONNECT}//0")
        _exit(0)
