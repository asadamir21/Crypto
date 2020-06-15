from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

from PIL import Image

#import pandas as pd
#import numpy as np

import os, sys, datetime

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Crypto"

        self.width = QDesktopWidget().screenGeometry(0).width()/2
        self.height = QDesktopWidget().screenGeometry(0).height()*0.8

        self.settings = QSettings('Crypto', 'Crypto')
        # Comic List for keeping checks on no of comics
        #self.ComicList = []

        self.initWindows()

    # Initiate Windows
    def initWindows(self):
        self.setWindowIcon(QIcon('Images/Logo.png'))
        self.setWindowTitle(self.title)
        self.setFixedHeight(self.height)
        self.setFixedWidth(self.width)


        self.CentralWidget = QWidget(self)

        self.setCentralWidget(self.CentralWidget)


        self.loginID = self.settings.value('loginID', '')

        if self.loginID == '':
            self.LoginLayout()

    def LoginLayout(self):
        try:
            if self.CentralWidget.layout() is not None:
                CentralWidgetLayout = self.CentralWidget.layout()
                for i in reversed(range(CentralWidgetLayout.count())):
                    CentralWidgetLayout.itemAt(i).widget().setParent(None)
            else:
                CentralWidgetLayout = QVBoxLayout(self.CentralWidget)
                CentralWidgetLayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                CentralWidgetLayout.setContentsMargins(self.width * 0.25, 0, self.width * 0.25, 0)

            # Login Title
            LoginTitleLabel = QLabel()
            LoginTitleLabel.setText("Login")
            LoginTitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            CentralWidgetLayout.addWidget(LoginTitleLabel)

            # Login ID Label
            LoginIDLabel = QLabel()
            LoginIDLabel.setText("LoginID")
            LoginIDLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(LoginIDLabel)

            # Login ID Line Edit
            LoginIDLineEdit = QLineEdit()
            LoginIDLineEdit.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(LoginIDLineEdit)

            # Login Password
            LoginPasswordLabel = QLabel()
            LoginPasswordLabel.setText("Password")
            LoginPasswordLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(LoginPasswordLabel)

            # Login Password Line Edit
            LoginPasswordLineEdit = QLineEdit()
            LoginPasswordLineEdit.setAlignment(Qt.AlignVCenter)
            LoginPasswordLineEdit.setEchoMode(QLineEdit.Password)
            CentralWidgetLayout.addWidget(LoginPasswordLineEdit)

            # Button Widget
            ButtonWidget = QWidget()

            # Button Layout
            ButtonLayout = QHBoxLayout(ButtonWidget)

            # Register Button
            RegisterButton = QPushButton()
            RegisterButton.setText("Register")
            RegisterButton.clicked.connect(lambda: self.RegisterLayout())
            ButtonLayout.addWidget(RegisterButton)

            # Login Button
            LoginButton = QPushButton()
            LoginButton.setText("Login")
            ButtonLayout.addWidget(LoginButton)

            CentralWidgetLayout.addWidget(ButtonWidget)


        except Exception as e:
            print(str(e))

    def RegisterLayout(self):
        try:
            if self.CentralWidget.layout() is not None:
                CentralWidgetLayout = self.CentralWidget.layout()
                for i in reversed(range(CentralWidgetLayout.count())):
                    CentralWidgetLayout.itemAt(i).widget().setParent(None)
            else:
                CentralWidgetLayout = QVBoxLayout(self.CentralWidget)
                CentralWidgetLayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                CentralWidgetLayout.setContentsMargins(self.width * 0.25, 0, self.width * 0.25, 0)

            # Register Title
            RegisterTitleLabel = QLabel()
            RegisterTitleLabel.setText("Register")
            RegisterTitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            CentralWidgetLayout.addWidget(RegisterTitleLabel)

            # Register Name Label
            NameLabel = QLabel()
            NameLabel.setText("Name")
            NameLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(NameLabel)

            # Register Name Line Edit
            NameLineEdit = QLineEdit()
            NameLineEdit.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(NameLineEdit)

            # Register email Label
            emailLabel = QLabel()
            emailLabel.setText("E-mail")
            emailLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(emailLabel)

            # Register Name Line Edit
            emailLineEdit = QLineEdit()
            emailLineEdit.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(emailLineEdit)
            emailLineEdit.setValidator(QRegularExpressionValidator(
                                            QRegularExpression(
                                                "\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b",
                                                QRegularExpression.CaseInsensitiveOption), self
                                            )
                                      )

            # Age Label
            AgeLabel = QLabel()
            AgeLabel.setText("Age:")
            AgeLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(AgeLabel)

            # Register Age Line Edit
            AgeLineEdit = QLineEdit()
            AgeLineEdit.setAlignment(Qt.AlignVCenter)
            AgeLineEdit.setValidator(QIntValidator(0, 10, self))
            CentralWidgetLayout.addWidget(AgeLineEdit)

            # Birth Date Label
            BirthDateLabel = QLabel()
            BirthDateLabel.setText("Birth Date:")
            BirthDateLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(BirthDateLabel)

            # Birth Date Calendar
            BirthDateCalendar = QDateEdit()
            BirthDateCalendar.setCalendarPopup(True)
            BirthDateCalendar.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
            BirthDateCalendar.setMaximumDate(datetime.datetime.now() - datetime.timedelta(days=5840))
            BirthDateCalendar.setMinimumDate(QDate(1903, 2, 2))
            BirthDateCalendar.setDate(datetime.datetime.now() - datetime.timedelta(days=5840))
            CentralWidgetLayout.addWidget(BirthDateCalendar)

            # Enter Password Label
            EnterPasswordLabel = QLabel()
            EnterPasswordLabel.setText("Enter Password")
            EnterPasswordLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(EnterPasswordLabel)

            # Enter Password Line Edit
            EnterPasswordLineEdit = QLineEdit()
            EnterPasswordLineEdit.setAlignment(Qt.AlignVCenter)
            EnterPasswordLineEdit.setEchoMode(QLineEdit.Password)
            CentralWidgetLayout.addWidget(EnterPasswordLineEdit)

            # Retype Password Label
            RetypePasswordLabel = QLabel()
            RetypePasswordLabel.setText("Re-type Password")
            RetypePasswordLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(RetypePasswordLabel)

            # Retype Password Line Edit
            RetypePasswordLineEdit = QLineEdit()
            RetypePasswordLineEdit.setAlignment(Qt.AlignVCenter)
            RetypePasswordLineEdit.setEchoMode(QLineEdit.Password)
            CentralWidgetLayout.addWidget(RetypePasswordLineEdit)

            # Button Widget
            ButtonWidget = QWidget()

            # Button Layout
            ButtonLayout = QHBoxLayout(ButtonWidget)

            # Login Button
            LoginButton = QPushButton()
            LoginButton.setText("Login")
            LoginButton.clicked.connect(lambda: self.LoginLayout())
            ButtonLayout.addWidget(LoginButton)

            # Register Button
            RegisterButton = QPushButton()
            RegisterButton.setText("Register")
            #RegisterButton.clicked.connect(lambda: self.RegisterLayout())
            ButtonLayout.addWidget(RegisterButton)

            CentralWidgetLayout.addWidget(ButtonWidget)

        except Exception as e:
            print(str(e))


    # Close Application / Exit
    def closeEvent(self, event):
        ExitWindowChoice = QMessageBox.question(self, 'Exit',
                                                "Are you sure you want to exit?",
                                                QMessageBox.Yes | QMessageBox.No)
        # If user chooses Yes
        if ExitWindowChoice == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    App = QApplication(sys.argv)

    Crypto = Window()
    Crypto.show()

    sys.exit(App.exec())