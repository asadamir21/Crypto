from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PIL import Image

import os, sys, datetime, mysql.connector, re, hashlib

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

        self.ButtonCSS = """
                            QPushButton{
                                background-color: white;
                                border-width: 1px;
                                border-color: #1e1e1e;
                                border-style: solid;
                                border-radius: 10;
                                padding: 3px;
                                font-weight: 700;
                                font-size: 15px;
                                padding-left: 5px;
                                padding-right: 5px;
                                min-width: 40px;
                            }
                            QPushButton:hover{
                                border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #32CD32, stop: 1 #d4e8f2);
                            }                                    
                        """

        if self.loginID == '':
            self.LoginLayout()
        else:
            self.MainWindow()

        #self.MainWindow()

    # Login Layout
    def LoginLayout(self):
        try:
            if self.CentralWidget.layout() is not None:
                CentralWidgetLayout = self.CentralWidget.layout()
                for i in reversed(range(CentralWidgetLayout.count())):
                    CentralWidgetLayout.itemAt(i).widget().setParent(None)
                CentralWidgetLayout.setContentsMargins(self.width * 0.25, self.height * 0.25, self.width * 0.25, self.height * 0.25)
            else:
                CentralWidgetLayout = QVBoxLayout(self.CentralWidget)
                CentralWidgetLayout.setAlignment(Qt.AlignHCenter)
                CentralWidgetLayout.setContentsMargins(self.width * 0.25, self.height * 0.25, self.width * 0.25,self.height * 0.25)

            # Logo Pixmap
            LogoPixmap = QLabel()
            LogoPixmap.setPixmap(QPixmap('Images/Logo.png').scaled(self.width/4, self.height, Qt.KeepAspectRatio))
            LogoPixmap.setAlignment(Qt.AlignHCenter)
            CentralWidgetLayout.addWidget(LogoPixmap)

            # Login Title
            LoginTitleLabel = QLabel()
            LoginTitleLabel.setText("Login")
            LoginTitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            font = LoginTitleLabel.font()
            font.setPointSize(20)
            font.setBold(True)
            LoginTitleLabel.setFont(font);

            LoginTitleLabel.setStyleSheet(
                """
                    QLabel{
                        background-color: rgba(0,0,0,0%);
                    }      
                """
            )
            CentralWidgetLayout.addWidget(LoginTitleLabel)

            # Login ID Label
            LoginIDLabel = QLabel()
            LoginIDLabel.setText("LoginID")
            LoginIDLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(LoginIDLabel)

            # Login ID Line Edit
            LoginIDLineEdit = QLineEdit()
            LoginIDLineEdit.setAlignment(Qt.AlignVCenter)
            LoginIDLineEdit.setStyleSheet(
                """
                    QLineEdit{
                        padding: 1px;
                        border-style: solid;
                        border: 1px solid  # 1e1e1e;
                        border-radius: 5;            
                    }
                """
            )
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
            RegisterButton.setStyleSheet(self.ButtonCSS)
            ButtonLayout.addWidget(RegisterButton)

            # Login Button
            LoginButton = QPushButton()
            LoginButton.setText("Login")
            LoginButton.setStyleSheet(self.ButtonCSS)
            ButtonLayout.addWidget(LoginButton)
            CentralWidgetLayout.addWidget(ButtonWidget)


        except Exception as e:
            print(str(e))

    # Login
    def Login(self):
        pass

    # Register Layout
    def RegisterLayout(self):
        try:
            if self.CentralWidget.layout() is not None:
                CentralWidgetLayout = self.CentralWidget.layout()
                for i in reversed(range(CentralWidgetLayout.count())):
                    CentralWidgetLayout.itemAt(i).widget().setParent(None)
                CentralWidgetLayout.setContentsMargins(self.width * 0.25, self.height * 0.125, self.width * 0.25, self.height * 0.125)
            else:
                CentralWidgetLayout = QVBoxLayout(self.CentralWidget)
                CentralWidgetLayout.setAlignment(Qt.AlignHCenter)
                CentralWidgetLayout.setContentsMargins(self.width * 0.25, self.height * 0.125, self.width * 0.25, self.height * 0.125)
                CentralWidgetLayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # Back Button Widget
            BackButtonWidget = QWidget()

            # Back Button Layout
            BackButtonLayout = QHBoxLayout(BackButtonWidget)
            BackButtonLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            # Back Button
            BackButton = QPushButton()
            BackButton.setIcon(QIcon("Images/Back.png"))
            BackButton.setIconSize(QSize(50,50))
            BackButton.setStyleSheet("border: 0px")
            BackButton.clicked.connect(lambda: self.LoginLayout())
            BackButtonLayout.addWidget(BackButton)

            CentralWidgetLayout.addWidget(BackButtonWidget)

            # Logo Pixmap
            LogoPixmap = QLabel()
            LogoPixmap.setPixmap(QPixmap('Images/Logo.png').scaled(self.width / 4, self.height, Qt.KeepAspectRatio))
            LogoPixmap.setAlignment(Qt.AlignHCenter)
            CentralWidgetLayout.addWidget(LogoPixmap)

            # Register Title
            RegisterTitleLabel = QLabel()
            RegisterTitleLabel.setText("Register")
            RegisterTitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            font = RegisterTitleLabel.font()
            font.setPointSize(20)
            font.setBold(True)
            RegisterTitleLabel.setFont(font);
            CentralWidgetLayout.addWidget(RegisterTitleLabel)

            # Register First Name Label
            FirstNameLabel = QLabel()
            FirstNameLabel.setText("First Name")
            FirstNameLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(FirstNameLabel)

            # Register First Name Line Edit
            FirstNameLineEdit = QLineEdit()
            FirstNameLineEdit.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(FirstNameLineEdit)

            # Register Last Name Label
            LastNameLabel = QLabel()
            LastNameLabel.setText("Last Name")
            LastNameLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(LastNameLabel)

            # Register Last Name Line Edit
            LastNameLineEdit = QLineEdit()
            LastNameLineEdit.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(LastNameLineEdit)

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

            # Register Gender Label
            GenderLabel = QLabel()
            GenderLabel.setText("Gender")
            GenderLabel.setAlignment(Qt.AlignVCenter)
            CentralWidgetLayout.addWidget(GenderLabel)

            # Gender GroupBox
            GenderGroupBox = QComboBox()
            GenderGroupBox.addItem("Male")
            GenderGroupBox.addItem("Female")
            CentralWidgetLayout.addWidget(GenderGroupBox)

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

            # Register Button
            RegisterButton = QPushButton()
            RegisterButton.setText("Register")
            RegisterButton.setDisabled(True)
            RegisterButton.setStyleSheet(self.ButtonCSS)
            CentralWidgetLayout.addWidget(RegisterButton)

            FirstNameLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, AgeLineEdit,BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
            LastNameLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, AgeLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
            emailLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, AgeLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
            AgeLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, AgeLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
            BirthDateCalendar.dateChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, AgeLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
            EnterPasswordLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, AgeLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
            RetypePasswordLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, AgeLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))

            RegisterButton.clicked.connect(lambda: self.RegisterValidate(FirstNameLineEdit.text(), LastNameLineEdit.text(), emailLineEdit.text(), AgeLineEdit.text(), BirthDateCalendar.text(), GenderGroupBox.currentText(), EnterPasswordLineEdit.text()))


        except Exception as e:
            print(str(e))

    # Register Button Toggle
    def RegisterButtonToggle(self, FirstNameLineEdit, LastNameLineEdit, emailLineEdit, AgeLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton):
        # Empty Fields
        if len(FirstNameLineEdit.text()) == 0 or len(LastNameLineEdit.text()) == 0 or len(emailLineEdit.text()) == 0 or len(AgeLineEdit.text()) == 0 or len(BirthDateCalendar.text()) == 0 or len(EnterPasswordLineEdit.text()) == 0 or len(RetypePasswordLineEdit.text()) == 0:
            emailLineEdit.setStyleSheet("border: 1px solid black;")
            EnterPasswordLineEdit.setStyleSheet("border: 1px solid black;")
            RetypePasswordLineEdit.setStyleSheet("border: 1px solid black;")
            RegisterButton.setDisabled(True)

        # Email
        elif not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', emailLineEdit.text()):
            emailLineEdit.setStyleSheet("border: 1px solid red;")
            RegisterButton.setDisabled(True)

        # Password Mismatch
        elif not EnterPasswordLineEdit.text() == RetypePasswordLineEdit.text():
            EnterPasswordLineEdit.setStyleSheet("border: 1px solid red;")
            RetypePasswordLineEdit.setStyleSheet("border: 1px solid red;")
            RegisterButton.setDisabled(True)

        else:
            emailLineEdit.setStyleSheet("border: 1px solid black;")
            EnterPasswordLineEdit.setStyleSheet("border: 1px solid black;")
            RetypePasswordLineEdit.setStyleSheet("border: 1px solid black;")
            RegisterButton.setDisabled(False)

    # Register Form Validate
    def RegisterValidate(self, FirstName, LastName, email, Age, BirthDate, Gender, EnterPassword):
        RegistrationError = False

        try:
            mycursor = mydb.cursor()
            PasswordHash = hashlib.md5(EnterPassword.encode('utf-8')).digest()

            sql = "INSERT INTO users (email, password, first_name, last_name, dob, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (email, PasswordHash, FirstName, LastName, datetime.datetime.strptime(BirthDate, '%m/%d/%Y').date(), Age, Gender)
            mycursor.execute(sql, val)

            mydb.commit()

        except Exception as e:
            RegistrationError = True

        if not RegistrationError:
            QMessageBox.information(self, "Registration Success",
                                    "User Registration Successful",
                                    QMessageBox.Ok)
            self.LoginLayout()
        else:
            QMessageBox.critical(self, "Registration Failed",
                                    "User Registration Failed",
                                    QMessageBox.Ok)

    # Register
    def Register(self):
        pass

    #  Main Window
    def MainWindow(self):
        pass

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


    mydb = mysql.connector.connect(
        host="sql12.freemysqlhosting.net",
        user="sql12348621",
        password="nvcWV8lYIj",
        database= "sql12348621"
    )

    Crypto = Window()
    Crypto.setStyleSheet(
        """
            QToolTip
            {
                 border: 1px solid black;
                 padding: 1px;
                 border-radius: 3px;
                 opacity: 100;
            }
            
            
            QTreeView, QListView
            {
                margin-left: 5px;
            }
            
            QMenuBar::item
            {
                background: transparent;
            }
            
            
            QMenu
            {
                border: 1px solid #cae6ef;
            }
            
            QMenuBar::item:selected
            {
                background: #cae6ef;
                border: 1px solid #cae6ef;
            }
            QMenuBar::item:pressed
            {
                background: #444;
                border: 1px solid #cae6ef;
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:1 #cae6ef,
                    stop:0.4 #cae6ef/*,
                    stop:0.2 #343434,
                    stop:0.1 #ffaa00*/
                );
                margin-bottom:-1px;
                padding-bottom:1px;
            }
            
            QMenu::item
            {
                padding: 2px 20px 2px 20px;
            }
            
            QMenu::item:selected
            {
                background: #cae6ef;
                color: #000000;
            }
            
            
            QWidget:focus, QMessageBox:focus
            {
                border: 1px solid darkgray;
            }
            
            QLineEdit
            {
                padding: 1px;
                border-style: solid;
                border: 1px solid #1e1e1e;
                border-radius: 5;
            }
            
            QPushButton
            {
                border-width: 1px;
                border-color: #1e1e1e;
                border-style: solid;
                border-radius: 6;
                padding: 3px;
                font-size: 12px;
                padding-left: 5px;
                padding-right: 5px;
                min-width: 40px;
            }
            
            
            QComboBox
            {
                border-style: solid;
                border: 1px solid #1e1e1e;
                border-radius: 5;
            }
            
            QComboBox:hover,QPushButton:hover
            {
                border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #86beda, stop: 1 #d4e8f2);
            }
            
            
            QComboBox:on
            {
                padding-top: 3px;
                padding-left: 4px;
            }
            
            QComboBox QAbstractItemView
            {
                border: 2px solid darkgray;
            }
            
            QComboBox::drop-down
            {
                 subcontrol-origin: padding;
                 subcontrol-position: top right;
                 width: 15px;
            
                 border-left-width: 0px;
                 border-left-color: darkgray;
                 border-left-style: solid; /* just a single line */
                 border-top-right-radius: 3px; /* same radius as the QComboBox */
                 border-bottom-right-radius: 3px;
             }
            
            QComboBox::down-arrow
            {
                 image: url(:/dark_orange/img/down_arrow.png);
            }
            
            QGroupBox
            {
                border: 1px solid darkgray;
                margin-top: 10px;
            }
            
            QGroupBox:focus
            {
                border: 1px solid darkgray;
            }
            
            QTextEdit:focus
            {
                border: 1px solid darkgray;
            }
            
            QScrollBar:horizontal {
                 border: 1px solid #222222;
                 background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #ffffff, stop: 0.2 #ffffff, stop: 1 #ffffff);
                 height: 7px;
                 margin: 0px 16px 0 16px;
            }
            
            QScrollBar::handle:horizontal
            {
                  background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #D3D3D3, stop: 0.5 #a9a9a9, stop: 1 #D3D3D3);
                  min-height: 20px;
                  border-radius: 2px;
            }
            
            QScrollBar::add-line:horizontal {
                  border: 1px solid #1b1b19;
                  border-radius: 2px;
                  background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #D3D3D3, stop: 1 #a9a9a9);
                  width: 14px;
                  subcontrol-position: right;
                  subcontrol-origin: margin;
            }
            
            QScrollBar::sub-line:horizontal {
                  border: 1px solid #1b1b19;
                  border-radius: 2px;
                  background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #D3D3D3, stop: 1 #a9a9a9);
                  width: 14px;
                 subcontrol-position: left;
                 subcontrol-origin: margin;
            }
            
            QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal
            {
                  border: 1px solid black;
                  width: 1px;
                  height: 1px;
                  background: white;
            }
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
            {
                  background: none;
            }
            
            QScrollBar:vertical
            {
                  background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #ffffff, stop: 0.2 #ffffff, stop: 1 #ffffff);
                  width: 7px;
                  margin: 16px 0 16px 0;
                  border: 1px solid #222222;
            }
            
            QScrollBar::handle:vertical
            {
                  background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D3D3D3, stop: 0.5 #a9a9a9, stop: 1 #D3D3D3);
                  min-height: 20px;
                  border-radius: 2px;
            }
            
            QScrollBar::add-line:vertical
            {
                  border: 1px solid #1b1b19;
                  border-radius: 2px;
                  background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D3D3D3, stop: 1 #a9a9a9);
                  height: 14px;
                  subcontrol-position: bottom;
                  subcontrol-origin: margin;
            }
            
            QScrollBar::sub-line:vertical
            {
                  border: 1px solid #1b1b19;
                  border-radius: 2px;
                  background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #a9a9a9, stop: 1 #D3D3D3);
                  height: 14px;
                  subcontrol-position: top;
                  subcontrol-origin: margin;
            }
            
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
            {
                  border: 1px solid black;
                  width: 1px;
                  height: 1px;
                  background: white;
            }
            
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {
                  background: none;
            }
            
            QHeaderView::section
            {
                padding-left: 4px;
                border: 1px solid #6c6c6c;
            }
            
            QDockWidget::title
            {
                text-align: center;
                spacing: 3px; /* spacing between items in the tool bar */
            }
            
            QDockWidget::close-button, QDockWidget::float-button
            {
                text-align: center;
                spacing: 1px; /* spacing between items in the tool bar */
            }
            
            QDockWidget::close-button:pressed, QDockWidget::float-button:pressed
            {
                padding: 1px -1px -1px 1px;
            }
            
            QMainWindow::separator
            {
                padding-left: 4px;
                border: 1px solid #4c4c4c;
                spacing: 3px; /* spacing between items in the tool bar */
            }
            
            QMainWindow::separator:hover
            {
                padding-left: 4px;
                border: 1px solid #6c6c6c;
                spacing: 3px; /* spacing between items in the tool bar */
            }
            
            QToolBar::handle
            {
                 spacing: 3px; /* spacing between items in the tool bar */
                 background: url(:/dark_orange/img/handle.png);
            }
            
            QMenu::separator
            {
                height: 2px;
                padding-left: 4px;
                margin-left: 10px;
                margin-right: 5px;
            }
            
            QProgressBar
            {
                border: 2px solid grey;
                border-radius:8px;
                padding:1px
            }
            
            QTabBar::tab {
                border: 1px solid #444;
                border-bottom-style: none;
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 3px;
                padding-bottom: 2px;
                margin-right: -1px;
            }
            
            QTabWidget::pane {
                border: 1px solid #444;
                top: 1px;
            }
            
            QTabBar::tab:last
            {
                margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
                border-top-right-radius: 3px;
            }
            
            QTabBar::tab:first:!selected{
                margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */
                border-top-left-radius: 3px;
            }
            
            QTabBar::tab:!selected
            {
                border-bottom-style: solid;
                margin-top: 3px;
            }
            
            QTabBar::tab:selected
            {
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                margin-bottom: 0px;
            }
            
            QTabBar::tab:!selected:hover
            {
                /*border-top: 2px solid #ffaa00;
                padding-bottom: 3px;*/
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
            }
            
            QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{
                color: #b1b1b1;
                background-color: #ffffff;
                border: 1px solid #b1b1b1;
                border-radius: 6px;
            }
            
            QRadioButton::indicator:checked
            {
                background-color: qradialgradient(
                    cx: 0.5, cy: 0.5,
                    fx: 0.5, fy: 0.5,
                    radius: 1.0,
                    stop: 0.25 #323232,
                    stop: 0.3 #ffffff
                );
            }
            
            QRadioButton::indicator
            {
                border-radius: 6px;
            }
            
            /*
            QCheckBox::indicator{
                border: 1px solid #b1b1b1;
                width: 9px;
                height: 9px;
            }
            
            QRadioButton::indicator:hover, QCheckBox::indicator:hover
            {
                border: 1px solid #121212;
            }
            
            QCheckBox::indicator:checked
            {
                image:url(:/dark_orange/img/checkbox.png);
            }
            
            
            QCheckBox::indicator:disabled, QRadioButton::indicator:disabled
            {
                border: 1px solid #444;
            }
            */
            QSlider::groove:horizontal {
                border: 1px solid #3A3939;
                height: 8px;
                margin: 2px 0;
                border-radius: 2px;
            }
            
            QSlider::handle:horizontal {
                border: 1px solid #3A3939;
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 2px;
            }
            
            QSlider::groove:vertical {
                border: 1px solid #3A3939;
                width: 8px;
                margin: 0 0px;
                border-radius: 2px;
            }
            
            QSlider::handle:vertical {
                border: 1px solid #3A3939;
                width: 14px;
                height: 14px;
                margin: 0 -4px;
                border-radius: 2px;
            }
            
            QAbstractSpinBox {
                padding-top: 2px;
                padding-bottom: 2px;
                border: 1px solid darkgray;
            
                border-radius: 2px;
                min-width: 50px;
            }
            
        """
    )
    Crypto.show()

    sys.exit(App.exec())