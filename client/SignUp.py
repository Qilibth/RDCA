
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(201, 212)
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
        print(self.id_input.text())


class SignUpGUI:
    @classmethod
    def run(cls):
        from sys import argv
        import os

        app = QtWidgets.QApplication(argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        os._exit(app.exec_())
