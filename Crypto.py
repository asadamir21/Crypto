from PyQt5.QtCore import QHistoryState
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PIL import Image
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from stegano import lsb

import os, sys, datetime, mysql.connector, re, hashlib, io, base64, random

class CryptoSteganography(object):
    def __init__(self, key):
        self.block_size = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def hide(self, input_filename, data):
        iv = Random.new().read(AES.block_size)
        encryption_suite = AES.new(self.key, AES.MODE_CBC, iv)

        if isinstance(data, str):
            data = data.encode()

        cypher_data = encryption_suite.encrypt(iv + pad(data, self.block_size))

        cypher_data = base64.b64encode(cypher_data).decode()
        secret = lsb.hide(input_filename, cypher_data)
        return secret

    def retrieve(self, input_image_file):
        cypher_data = lsb.reveal(input_image_file)

        if not cypher_data:
            return None

        cypher_data = base64.b64decode(cypher_data)
        iv = cypher_data[:AES.block_size]
        cypher_data = cypher_data[AES.block_size:]

        try:
            decryption_suite = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = unpad(
                decryption_suite.decrypt(cypher_data),
                self.block_size
            )
            try:
                return decrypted_data.decode('utf-8')
            except UnicodeDecodeError:
                return decrypted_data
        except ValueError:
            return None

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "STD"

        self.width = QDesktopWidget().screenGeometry(0).width()
        self.height = QDesktopWidget().screenGeometry(0).height()

        self.settings = QSettings('STD', 'STD')
        self.initWindows()

    # Initiate Windows
    def initWindows(self):
        self.setWindowIcon(QIcon('Images/Logo.png'))
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.showMaximized()

        self.CentralWidget = QWidget(self)
        self.CentralWidget.setStyleSheet('background-color: #ffffff')
        self.setCentralWidget(self.CentralWidget)

        self.ButtonCSS = """
                            QPushButton{
                                background-color: #005072;
                                color: #ffffff;
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
                                border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #005b82, stop: 1 #d4e8f2);
                            }                                    
                        """

        self.email = self.settings.value('email', '')

    # Login Layout
    def LoginLayout(self):
        if self.CentralWidget.layout() is not None:
            CentralWidgetLayout = self.CentralWidget.layout()
            while CentralWidgetLayout.layout().count() > 0:
                try:
                    CentralWidgetLayout.itemAt(0).widget().setParent(None)
                except:
                    CentralWidgetLayout.removeItem(CentralWidgetLayout.itemAt(0))

            CentralWidgetLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            CentralWidgetLayout.setContentsMargins(self.width * 0.375, 0, self.width * 0.375, 0)

        else:
            CentralWidgetLayout = QVBoxLayout(self.CentralWidget)
            CentralWidgetLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            CentralWidgetLayout.setContentsMargins(self.width * 0.375, 0, self.width * 0.375, 0)

        font = QFont()
        font.setBold(True)
        font.setFamily('Ubuntu')

        # Logo Pixmap
        LogoPixmap = QLabel()
        LogoPixmap.setPixmap(QPixmap('Images/Logo.png').scaled(self.width * 0.125, self.height, Qt.KeepAspectRatio))
        LogoPixmap.setAlignment(Qt.AlignHCenter)
        CentralWidgetLayout.addWidget(LogoPixmap)

        # Application Title
        ApplicationTitleLabel = QLabel()
        ApplicationTitleLabel.setText("STD")
        ApplicationTitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        ApplicationTitleLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        font.setPointSize(20)
        ApplicationTitleLabel.setFont(font);
        CentralWidgetLayout.addWidget(ApplicationTitleLabel)

        # Login Title
        LoginTitleLabel = QLabel()
        LoginTitleLabel.setText("Login")
        LoginTitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        font.setPointSize(12)
        LoginTitleLabel.setFont(font)
        LoginTitleLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        CentralWidgetLayout.addWidget(LoginTitleLabel)

        font.setPointSize(8)

        # Login ID Label
        emailLabel = QLabel()
        emailLabel.setText("Email")
        emailLabel.setFont(font);
        emailLabel.setAlignment(Qt.AlignVCenter)
        emailLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        CentralWidgetLayout.addWidget(emailLabel)

        # Login ID Line Edit
        emailLineEdit = QLineEdit()
        emailLineEdit.setAlignment(Qt.AlignVCenter)
        emailLineEdit.setStyleSheet(
            """
                QLineEdit{
                    padding: 1px;
                    border-style: solid;
                    border: 1px solid  # 1e1e1e;
                    border-radius: 5;
                    color: #005072;            
                }
            """
        )
        CentralWidgetLayout.addWidget(emailLineEdit)

        # Login Password
        LoginPasswordLabel = QLabel()
        LoginPasswordLabel.setText("Password")
        LoginPasswordLabel.setAlignment(Qt.AlignVCenter)
        LoginPasswordLabel.setFont(font);
        LoginPasswordLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
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
        LoginButton.setDisabled(True)
        ButtonLayout.addWidget(LoginButton)
        CentralWidgetLayout.addWidget(ButtonWidget)

        emailLineEdit.textChanged.connect(lambda: self.LoginButtonToggle(emailLineEdit, LoginPasswordLineEdit, LoginButton))
        LoginPasswordLineEdit.textChanged.connect(lambda: self.LoginButtonToggle(emailLineEdit, LoginPasswordLineEdit, LoginButton))

        LoginButton.clicked.connect(lambda: self.Login(emailLineEdit.text(), LoginPasswordLineEdit.text()))

    # Login Button Toggle
    def LoginButtonToggle(self, Email, Password, LoginButton):
        # Empty Fields
        if len(Email.text()) == 0 or len(Password.text()) == 0:
            Email.setStyleSheet("border: 1px solid black;")
            Password.setStyleSheet("border: 1px solid black;")
            LoginButton.setDisabled(True)

        # Email
        elif not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', Email.text()):
            Email.setStyleSheet("border: 1px solid red;")
            LoginButton.setDisabled(True)

        else:
            Email.setStyleSheet("border: 1px solid black;")
            Password.setStyleSheet("border: 1px solid black;")
            LoginButton.setDisabled(False)

    # Login
    def Login(self, Email, Password):
        try:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM users where email = %s and password = %s", (Email, str(hashlib.md5(Password.encode('utf-8')).digest())))

            myresult = mycursor.fetchall()

            if not len(myresult):
                QMessageBox.critical(self, 'Login Error',
                                    'Invalid Credentials', QMessageBox.Ok)


            else:
                self.settings.setValue('email', myresult[0][1])
                self.email = self.settings.value('email', '')
                self.MainWindow()

        except mysql.connector.Error as error:
            QMessageBox.critical(self, 'Database Error',
                                'Connection to database failed', QMessageBox.Ok)

    # Register Layout
    def RegisterLayout(self):
        if self.CentralWidget.layout() is not None:
            CentralWidgetLayout = self.CentralWidget.layout()
            for i in reversed(range(CentralWidgetLayout.count())):
                CentralWidgetLayout.itemAt(i).widget().setParent(None)
            CentralWidgetLayout.setContentsMargins(self.width * 0.375, 0, self.width * 0.375, 0)
        else:
            CentralWidgetLayout = QVBoxLayout(self.CentralWidget)
            CentralWidgetLayout.setAlignment(Qt.AlignHCenter)
            CentralWidgetLayout.setContentsMargins(self.width * 0.375, 0, self.width * 0.375, 0)
            CentralWidgetLayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # Font
        font = QFont()
        font.setBold(True)
        font.setFamily('Ubuntu')

        # Logo Pixmap
        LogoPixmap = QLabel()
        LogoPixmap.setPixmap(QPixmap('Images/Logo.png').scaled(self.width*0.125, self.height, Qt.KeepAspectRatio))
        LogoPixmap.setAlignment(Qt.AlignHCenter)
        CentralWidgetLayout.addWidget(LogoPixmap)

        # Application Title
        ApplicationTitleLabel = QLabel()
        ApplicationTitleLabel.setText("STD")
        ApplicationTitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        ApplicationTitleLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        font.setPointSize(20)
        ApplicationTitleLabel.setFont(font);
        CentralWidgetLayout.addWidget(ApplicationTitleLabel)

        # Register Title
        RegisterTitleLabel = QLabel()
        RegisterTitleLabel.setText("Register")
        RegisterTitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        RegisterTitleLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        font.setPointSize(12)
        RegisterTitleLabel.setFont(font);
        CentralWidgetLayout.addWidget(RegisterTitleLabel)

        font.setPointSize(8)

        # Register First Name Label
        FirstNameLabel = QLabel()
        FirstNameLabel.setText("First Name")
        FirstNameLabel.setAlignment(Qt.AlignVCenter)
        FirstNameLabel.setFont(font);

        FirstNameLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        CentralWidgetLayout.addWidget(FirstNameLabel)

        # Register First Name Line Edit
        FirstNameLineEdit = QLineEdit()
        FirstNameLineEdit.setAlignment(Qt.AlignVCenter)
        CentralWidgetLayout.addWidget(FirstNameLineEdit)

        # Register Last Name Label
        LastNameLabel = QLabel()
        LastNameLabel.setText("Last Name")
        LastNameLabel.setAlignment(Qt.AlignVCenter)
        LastNameLabel.setFont(font);
        LastNameLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        CentralWidgetLayout.addWidget(LastNameLabel)

        # Register Last Name Line Edit
        LastNameLineEdit = QLineEdit()
        LastNameLineEdit.setAlignment(Qt.AlignVCenter)
        CentralWidgetLayout.addWidget(LastNameLineEdit)

        # Register email Label
        emailLabel = QLabel()
        emailLabel.setText("E-mail")
        emailLabel.setAlignment(Qt.AlignVCenter)
        emailLabel.setFont(font);
        emailLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
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

        # Birth Date Label
        BirthDateLabel = QLabel()
        BirthDateLabel.setText("Birth Date:")
        BirthDateLabel.setAlignment(Qt.AlignVCenter)
        BirthDateLabel.setFont(font);
        BirthDateLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        CentralWidgetLayout.addWidget(BirthDateLabel)

        # Birth Date Calendar
        BirthDateCalendar = QDateEdit()
        BirthDateCalendar.setCalendarPopup(True)
        BirthDateCalendar.setStyleSheet(
            """
                background-color: #ffffff;
                color: #005072;
                border-width: 1px;
                border-color: #005072;
                border-style: solid;
                border-radius: 10;                
            """
        )
        BirthDateCalendar.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        BirthDateCalendar.setMaximumDate(datetime.datetime.now() - datetime.timedelta(days=5840))
        BirthDateCalendar.setMinimumDate(QDate(1903, 2, 2))
        BirthDateCalendar.setDate(datetime.datetime.now() - datetime.timedelta(days=5840))
        CentralWidgetLayout.addWidget(BirthDateCalendar)

        # Register Gender Label
        GenderLabel = QLabel()
        GenderLabel.setText("Gender")
        GenderLabel.setAlignment(Qt.AlignVCenter)
        GenderLabel.setFont(font);
        GenderLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
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
        EnterPasswordLabel.setFont(font);
        EnterPasswordLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        CentralWidgetLayout.addWidget(EnterPasswordLabel)

        # Enter Password Line Edit
        EnterPasswordLineEdit = QLineEdit()
        EnterPasswordLineEdit.setAlignment(Qt.AlignVCenter)
        EnterPasswordLineEdit.setEchoMode(QLineEdit.Password)
        CentralWidgetLayout.addWidget(EnterPasswordLineEdit)

        # Min Character
        MinCharLabel = QLabel()
        MinCharLabel.setText('Minimum 8 characters')
        MinCharLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        MinCharLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        CentralWidgetLayout.addWidget(MinCharLabel)

        # Retype Password Label
        RetypePasswordLabel = QLabel()
        RetypePasswordLabel.setText("Re-type Password")
        RetypePasswordLabel.setAlignment(Qt.AlignVCenter)
        RetypePasswordLabel.setFont(font);
        RetypePasswordLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        CentralWidgetLayout.addWidget(RetypePasswordLabel)

        # Retype Password Line Edit
        RetypePasswordLineEdit = QLineEdit()
        RetypePasswordLineEdit.setAlignment(Qt.AlignVCenter)
        RetypePasswordLineEdit.setEchoMode(QLineEdit.Password)
        CentralWidgetLayout.addWidget(RetypePasswordLineEdit)

        CentralWidgetLayout.addSpacing(self.height/20)

        # ButtonWidget
        ButtonWidget = QWidget()
        ButtonWidgetLayout = QHBoxLayout(ButtonWidget)

        # Back Button
        BackButton = QPushButton()
        BackButton.setText("Back To Login")
        BackButton.setStyleSheet(self.ButtonCSS)
        ButtonWidgetLayout.addWidget(BackButton)

        # Register Button
        RegisterButton = QPushButton()
        RegisterButton.setText("Register")
        RegisterButton.setDisabled(True)
        RegisterButton.setStyleSheet(self.ButtonCSS)
        ButtonWidgetLayout.addWidget(RegisterButton)

        CentralWidgetLayout.addWidget(ButtonWidget)

        FirstNameLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        LastNameLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        emailLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        BirthDateCalendar.dateChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        EnterPasswordLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        RetypePasswordLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))

        BackButton.clicked.connect(lambda: self.LoginLayout())
        RegisterButton.clicked.connect(lambda: self.Register(FirstNameLineEdit.text(), LastNameLineEdit.text(), emailLineEdit.text(), BirthDateCalendar.text(), GenderGroupBox.currentText(), EnterPasswordLineEdit.text()))

    # Register Button Toggle
    def RegisterButtonToggle(self, FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton):
        # Empty Fields
        if len(FirstNameLineEdit.text()) == 0 or len(LastNameLineEdit.text()) == 0 or len(emailLineEdit.text()) == 0 or len(BirthDateCalendar.text()) == 0 or len(EnterPasswordLineEdit.text()) == 0 or len(RetypePasswordLineEdit.text()) == 0:
            emailLineEdit.setStyleSheet("border: 1px solid black;")
            EnterPasswordLineEdit.setStyleSheet("border: 1px solid black;")
            RetypePasswordLineEdit.setStyleSheet("border: 1px solid black;")
            RegisterButton.setDisabled(True)

        # Email
        elif not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', emailLineEdit.text()):
            emailLineEdit.setStyleSheet("border: 1px solid red;")
            RegisterButton.setDisabled(True)

        # Password Mismatch
        elif not EnterPasswordLineEdit.text() == RetypePasswordLineEdit.text() or not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', EnterPasswordLineEdit.text()):
            if not EnterPasswordLineEdit.text() == RetypePasswordLineEdit.text():
                EnterPasswordLineEdit.setStyleSheet("border: 1px solid red;")
                RetypePasswordLineEdit.setStyleSheet("border: 1px solid red;")
                RegisterButton.setDisabled(True)
            else:
                EnterPasswordLineEdit.setStyleSheet("border: 1px solid red;")
                RetypePasswordLineEdit.setStyleSheet("border: 1px solid black;")
                RegisterButton.setDisabled(True)
        else:
            emailLineEdit.setStyleSheet("border: 1px solid black;")
            EnterPasswordLineEdit.setStyleSheet("border: 1px solid black;")
            RetypePasswordLineEdit.setStyleSheet("border: 1px solid black;")
            RegisterButton.setDisabled(False)

    # Register
    def Register(self, FirstName, LastName, email, BirthDate, Gender, EnterPassword):
        RegistrationError = False

        try:
            mycursor = mydb.cursor()

            sql = "INSERT INTO users (email, password, first_name, last_name, dob, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (email,
                   str(hashlib.md5(EnterPassword.encode('utf-8')).digest()),
                   FirstName,
                   LastName,
                   datetime.datetime.strptime(BirthDate, '%m/%d/%Y').date(),
                   Gender)
            mycursor.execute(sql, val)

            mydb.commit()

        except mysql.connector.Error as error:
            RegistrationError = True
            QMessageBox.critical(self, 'Database Error',
                                'Connection to database failed', QMessageBox.Ok)

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

    #  Main Window
    def MainWindow(self):
        if self.CentralWidget.layout() is not None:
            CentralWidgetLayout = self.CentralWidget.layout()
            for i in reversed(range(CentralWidgetLayout.count())):
                CentralWidgetLayout.itemAt(i).widget().setParent(None)
            CentralWidgetLayout.setContentsMargins(0, 0, 0, 0)
        else:
            CentralWidgetLayout = QVBoxLayout(self.CentralWidget)
            CentralWidgetLayout.setContentsMargins(0, 0, 0, 0)

        # ************************************************************************************
        # ************************************ Top Widget ************************************
        # ************************************************************************************

        # Top Widget
        TopWidget = QWidget()
        TopWidget.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")

        # Top Widget Layout
        TopWidgetLayout = QHBoxLayout(TopWidget)
        TopWidgetLayout.setAlignment(Qt.AlignVCenter)

        # *************** Compose Button ***************

        ComposeButtonWidget = QWidget()
        ComposeButtonWidgetLayout = QHBoxLayout(ComposeButtonWidget)
        ComposeButtonWidgetLayout.setAlignment(Qt.AlignLeft)

        # Compose Button
        ComposeButton = QPushButton()
        ComposeButton.setText("Compose")
        ComposeButton.setIcon(QIcon("Images/Compose.png"))
        ComposeButton.setIconSize(QSize(25, 25))
        ComposeButton.setStyleSheet(
            """
                QPushButton{
                    background-color: #005072;
                    color: #ffffff;
                    border-width: 1px;
                    border-color: #1e1e1e;
                    border-style: solid;
                    border-radius: 15;
                    padding: 3px;
                    font-weight: 900;
                    font-size: 16px;
                    padding-left: 5px;
                    padding-right: 5px;
                    min-width: 40px;
                }
                QPushButton:hover{
                    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #005b82, stop: 1 #d4e8f2);
                }                     
            """
        )
        ComposeButton.clicked.connect(lambda: self.ComposeMessageDialog())

        ComposeButtonWidgetLayout.addWidget(ComposeButton)
        TopWidgetLayout.addWidget(ComposeButtonWidget)

        # *************** Setting Button ***************

        SettingButtonWidget = QWidget()
        SettingButtonWidgetLayout = QHBoxLayout(SettingButtonWidget)
        SettingButtonWidgetLayout.setAlignment(Qt.AlignRight)

        # Setting Button
        SettingButton = QPushButton();
        SettingButton.setIcon(QIcon("Images/Setting.png"))
        SettingButton.setIconSize(QSize(50, 50))
        SettingButton.setStyleSheet(
            """
                QPushButton{
                    border: 0px solid;
                }    
            """
        )

        menu = QMenu("Menu");
        menu.setLayoutDirection(Qt.RightToLeft)

        # Account Button
        AccountButton = QAction('Account', self)
        AccountButton.setStatusTip('Account')
        AccountButton.triggered.connect(self.AccountInfo)
        menu.addAction(AccountButton)

        # Logout Button
        LogoutButton = QAction('Logout', self)
        LogoutButton.setStatusTip('Logout')
        LogoutButton.triggered.connect(self.LogoutDialog)
        menu.addAction(LogoutButton)

        # About STD Button
        HelpButton = QAction('Help', self)
        HelpButton.setStatusTip('Help')
        HelpButton.triggered.connect(lambda: QMessageBox().about(self, 'About STD', '''
                                                                                        <h2 style="text-align:center">Steps to send secure messages using STD:</h2>
                                                                                        <br>
                                                                                        <ol>
                                                                                            <li>Signin/Signup using a valid email address</li>
                                                                                            <li>Click 'Compose' Button on the top left corner of homepage</li>
                                                                                            <li>Upload an image (max size: 100kb) to secure message</li>
                                                                                            <li>Enter recipients email address</li>
                                                                                            <li>Enter the text message you intend to send (max characters: 1000)</li>                                                                                            
                                                                                            <li>Click Send</li>                                                                                            
                                                                                        </ol>
                                                                                    '''
                                                                    )
                                      )
        menu.addAction(HelpButton)

        # Delete Account
        DeleteButton = QAction('Delete Account', self)
        DeleteButton.setStatusTip('Delete Account')
        DeleteButton.triggered.connect(self.DeleteAccountDialog)
        menu.addAction(DeleteButton)

        SettingButton.setMenu(menu)
        SettingButtonWidgetLayout.addWidget(SettingButton)

        TopWidgetLayout.addWidget(SettingButtonWidget)
        CentralWidgetLayout.addWidget(TopWidget)

        # ************************************************************************************
        # ********************************** Bottom Widget ***********************************
        # ************************************************************************************

        BottomWidget = QWidget()
        BottomWidgetLayout = QHBoxLayout(BottomWidget)

        # List Widget
        CategoryList = QListWidget()
        CategoryList.setStyleSheet(
            """
                QListWidget::item 
                {
                    color: #005072;
                    background-color: #ffffff;                                                                  
                }
                
                QListWidget::item:selected 
                {
                    color: #ffffff;
                    background-color: #005072;                      
                }
            """
        )
        BottomWidgetLayout.addWidget(CategoryList, 25)

        # Inbox Category
        InboxCategory = QListWidgetItem()
        InboxCategory.setTextAlignment(Qt.AlignHCenter | Qt.AlignHCenter)
        InboxCategory.setText("Inbox")
        InboxCategory.setFont(QFont('Ubuntu', 15, QFont.Medium))
        CategoryList.addItem(InboxCategory)

        # Sent Category
        SentCategory = QListWidgetItem()
        SentCategory.setTextAlignment(Qt.AlignHCenter | Qt.AlignHCenter)
        SentCategory.setText("Sent")
        SentCategory.setFont(QFont('Ubuntu', 15, QFont.Medium))
        CategoryList.addItem(SentCategory)

        CategoryList.item(0).setSelected(True)

        # Table
        TableWidget = QWidget()
        TableWidgetLayout = QVBoxLayout(TableWidget)

        # Search Widget
        SearchWidget = QWidget()
        SearchWidgetLayout = QHBoxLayout(SearchWidget)
        SearchWidgetLayout.setAlignment(Qt.AlignVCenter)
        SearchWidgetLayout.setContentsMargins(SearchWidget.width()*0.5, 0, 0, 0)
        SearchWidgetLayout.setSpacing(50)

        SearchWidgetLayout.addWidget(QWidget(), 50)

        # Search LineEdit
        SearchLineEdit = QLineEdit()
        SearchLineEdit.setAlignment(Qt.AlignLeft)
        SearchLineEdit.setClearButtonEnabled(True)
        SearchLineEdit.addAction(QIcon("Images/Search.png"), QLineEdit.LeadingPosition)
        SearchLineEdit.setPlaceholderText("Search...")
        SearchWidgetLayout.addWidget(SearchLineEdit, 50)

        TableWidgetLayout.addWidget(SearchWidget, 10)

        # Table Widget
        MessagesTable = QTableWidget()
        MessagesTable.verticalHeader().setVisible(False)
        TableWidgetLayout.addWidget(MessagesTable, 90)

        BottomWidgetLayout.addWidget(TableWidget, 75)

        self.Inbox(MessagesTable)

        CategoryList.currentItemChanged.connect(lambda: self.CategoryListCurrentItemChanged(MessagesTable))
        SearchLineEdit.textChanged.connect(lambda: self.SearchEmail(MessagesTable))
        CentralWidgetLayout.addWidget(BottomWidget, 90)

    # Compose Message
    def ComposeMessageDialog(self):
        # Compose Message Dialog
        ComposeMessageDialogBox = QDialog()
        ComposeMessageDialogBox.setModal(True)
        ComposeMessageDialogBox.setWindowTitle("Compose Message")
        ComposeMessageDialogBox.setParent(self)
        ComposeMessageDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        ComposeMessageDialogBox.setFixedWidth(self.width / 4)
        ComposeMessageDialogBox.setStyleSheet('background-color: #ffffff')

        ComposeMessageDailogLayout = QVBoxLayout(ComposeMessageDialogBox)
        ComposeMessageDailogLayout.setContentsMargins(50, 50, 50, 50)

        # ****************** Choose File ********************

        ImageFileWidget = QWidget()
        ImageFileLayout = QHBoxLayout(ImageFileWidget)
        ImageFileLayout.setAlignment(Qt.AlignVCenter)

        # Image File Path LineEdit
        ImageFilePathLineEdit = QLineEdit()
        ImageFilePathLineEdit.setReadOnly(True)
        ImageFileLayout.addWidget(ImageFilePathLineEdit)

        # Image Browse Button
        ImageBrowseButton = QPushButton()
        ImageBrowseButton.setText("Choose File")
        ImageBrowseButton.clicked.connect(lambda: self.ComposeChooseButton(ImageFilePathLineEdit))
        ImageBrowseButton.setStyleSheet(
            """
                background-color: #005072;
                color: #ffffff;
                border-width: 1px;
                border-color: #1e1e1e;
                border-style: solid;
                border-radius: 10;
                padding: 3px;
                font-weight: 700;
                font-size: 12px;
                padding-left: 5px;
                padding-right: 5px;
                min-width: 40px;
            """
        )
        ImageFileLayout.addWidget(ImageBrowseButton)

        ComposeMessageDailogLayout.addWidget(ImageFileWidget)

        # ************** Max File Size Labels ***************
        MaxFileSizeLabel = QLabel()
        MaxFileSizeLabel.setText('Max Size: 100kb')
        MaxFileSizeLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        MaxFileSizeLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        ComposeMessageDailogLayout.addWidget(MaxFileSizeLabel)

        # ********************** To *************************
        SendToLabel = QLabel()
        SendToLabel.setText("To")
        SendToLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        ComposeMessageDailogLayout.addWidget(SendToLabel)

        SendToLineEdit = QLineEdit()
        SendToCompleter = QCompleter()
        SendToLineEdit.setCompleter(SendToCompleter)
        SendToModel = QStringListModel()
        SendToCompleter.setModel(SendToModel)
        ComposeMessageDailogLayout.addWidget(SendToLineEdit)

        # ****************** Text Message ********************
        MessageLabel = QLabel()
        MessageLabel.setText("Message")
        ComposeMessageDailogLayout.addWidget(MessageLabel)

        MessageTextEdit = QTextEdit()
        ComposeMessageDailogLayout.addWidget(MessageTextEdit)

        # *************** Characters Labels **********************
        CharLabel = QLabel()
        CharLabel.setText('1000 char left')
        CharLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        CharLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
        ComposeMessageDailogLayout.addWidget(CharLabel)

        # ******************* Button Box *********************
        ComposeButtonBox = QDialogButtonBox()
        ComposeButtonBox.setCenterButtons(True)
        ComposeButtonBox.setStandardButtons(QDialogButtonBox.Ok)
        ComposeButtonBox.button(QDialogButtonBox.Ok).setText('Send')
        ComposeButtonBox.button(QDialogButtonBox.Ok).setIcon(QIcon("Images/Send.png"))
        ComposeButtonBox.button(QDialogButtonBox.Ok).setLayoutDirection(Qt.RightToLeft)
        ComposeButtonBox.button(QDialogButtonBox.Ok).setStyleSheet(
            """
                background-color: #005072;
                color: #ffffff;
                border-width: 1px;
                border-color: #1e1e1e;
                border-style: solid;
                border-radius: 10;
                padding: 3px;
                font-weight: 700;
                font-size: 12px;
                padding-left: 5px;
                padding-right: 5px;
                min-width: 40px;
            """
        )



        ImageFilePathLineEdit.textChanged.connect(lambda: self.ToggleSendButton(ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, ComposeButtonBox))
        SendToLineEdit.textChanged.connect(lambda: self.EmailSuggestion(SendToModel, SendToLineEdit.text()))
        SendToLineEdit.textChanged.connect(lambda: self.ToggleSendButton(ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, ComposeButtonBox))
        MessageTextEdit.textChanged.connect(lambda: self.ToggleSendButton(ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, ComposeButtonBox))
        MessageTextEdit.textChanged.connect(lambda: self.CharacterLimit(CharLabel))

        ComposeButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        ComposeMessageDailogLayout.addWidget(ComposeButtonBox)

        ComposeButtonBox.accepted.connect(ComposeMessageDialogBox.accept)
        ComposeButtonBox.rejected.connect(ComposeMessageDialogBox.reject)

        ComposeButtonBox.accepted.connect(lambda: self.SendMessage(ImageFilePathLineEdit.text(),
                                                                   SendToLineEdit.text(),
                                                                   MessageTextEdit.toPlainText()))

        ComposeMessageDialogBox.exec_()

    # Email Suggestion
    def EmailSuggestion(self, SendToModel, CurrentText):
        try:
            mycursor = mydb.cursor()

            sql_insert_query = """
                                    SELECT email FROM users where not email = %s                                     
                               """

            insert_tuple = (self.email,)
            mycursor.execute(sql_insert_query, insert_tuple)
            EmailList = mycursor.fetchall()
            EmailList = [element for tupl in EmailList for element in tupl]

            matching = [s for s in EmailList if CurrentText in s]
            SendToModel.setStringList(matching)


        except mysql.connector.Error as error:
            QMessageBox.critical(self, 'Database Error',
                                 'Connection to database failed', QMessageBox.Ok)

    # Character Limit
    def CharacterLimit(self, CharLabel):
        MessageTextEdit = self.sender()

        if len(MessageTextEdit.toPlainText()) > 1000:
            MessageTextEdit.textCursor().deletePreviousChar()

        CharLabel.setText(str(1000 - len(MessageTextEdit.toPlainText())) + " char left")

    # Toggle Send Button
    def ToggleSendButton(self, ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, ComposeButtonBox):
        if len(ImageFilePathLineEdit.text()) == 0 or len(SendToLineEdit.text()) == 0 or len(MessageTextEdit.toPlainText()) == 0:
            ImageFilePathLineEdit.setStyleSheet("border: 1px solid black;")
            SendToLineEdit.setStyleSheet("border: 1px solid black;")
            MessageTextEdit.setStyleSheet("border: 1px solid black;")
            ComposeButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        # Email
        elif not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', SendToLineEdit.text()):
            SendToLineEdit.setStyleSheet("border: 1px solid red;")
            ComposeButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        else:
            ImageFilePathLineEdit.setStyleSheet("border: 1px solid black;")
            SendToLineEdit.setStyleSheet("border: 1px solid black;")
            MessageTextEdit.setStyleSheet("border: 1px solid black;")
            ComposeButtonBox.button(QDialogButtonBox.Ok).setDisabled(False)

    # Send Message
    def SendMessage(self, ImageFilePath, To, Message):
        try:
            try :
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM users where email = %s", (To,))

                myresult = mycursor.fetchall()

            except mysql.connector.Error as error:
                QMessageBox.critical(self, 'Database Error',
                                    'Connection to database failed', QMessageBox.Ok)

            if len(myresult) > 0 and not To == self.email:

                sql_insert_query = """ 
                                            INSERT INTO messages (sender_id, receiver_id, enc_key, img_byte_array, datetime, read_flag)
                                            VALUES(
                                                (SELECT id FROM users where email = %s), 
                                                (SELECT id FROM users where email = %s), 
                                                %s, %s, SYSDATE(), 0) 
                                    """

                # Random Key Generation
                Key = str(random.randint(0, 1000))

                # key inserted here
                crypto_steganography = CryptoSteganography(Key)

                # Image Loaded
                SteganoImage = Image.open(ImageFilePath)

                if SteganoImage.mode == "RGB":
                    SteganoImage = SteganoImage.convert('RGB')

                # Encrypt Data in Image
                EncryptedImage = crypto_steganography.hide(SteganoImage, Message)

                # Converting Encrypted Image to Byte Array
                imgByteArr = io.BytesIO()
                EncryptedImage.save(imgByteArr, format='PNG')

                insert_tuple = (self.email, To, Key, imgByteArr.getvalue())
                result = mycursor.execute(sql_insert_query, insert_tuple)
                mydb.commit()

                QMessageBox.information(self, "Message Send",
                                        "Message Successfully Send to " + To,
                                        QMessageBox.Ok)

            elif len(myresult) == 0:
                QMessageBox.critical(self, 'Message Error',
                                     'No Such Email Address Exist', QMessageBox.Ok)

            elif To == self.email:
                QMessageBox.critical(self, 'Message Error',
                                     'Cannot send a Message to yourself', QMessageBox.Ok)

        except Exception as e:
            print(str(e))

    # Compose FIle Button
    def ComposeChooseButton(self, ImageFilePathLineEdit):
        path = QFileDialog.getOpenFileName(self, 'Open Image File', "", 'Image files (*.png *.bmp *.jpeg *.jpg *.webp *.tiff *.tif *.pfm *.jp2 *.hdr *.pic *.exr *.ras *.sr *.pbm *.pgm *.ppm *.pxm *.pnm)')

        if all(path):
            ImageFilePathLineEdit.clear()

            if os.stat(path[0]).st_size < 102400:
                ImageFilePathLineEdit.setText(path[0])
            else:
                QMessageBox.critical(self, "Image File Size",
                                     "Please Select a File Size under 100kb", QMessageBox.Ok)

    # Account Information
    def AccountInfo(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users where email = %s",  (self.email,))

        myresult = mycursor.fetchall()

        if len(myresult) > 0:
            # Edit Row Dialog
            AccountInfoDialogBox = QDialog()
            AccountInfoDialogBox.setModal(True)
            AccountInfoDialogBox.setWindowTitle(self.email)
            AccountInfoDialogBox.setParent(self)
            AccountInfoDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
            AccountInfoDialogBox.setFixedWidth(self.width / 4)
            AccountInfoDialogBox.setStyleSheet('background-color: #ffffff')

            AccountInfoDailogLayout = QVBoxLayout(AccountInfoDialogBox)
            AccountInfoDailogLayout.setContentsMargins(50, 50, 50, 50)

            font = QFont()
            font.setBold(True)
            font.setPointSize(10)
            font.setFamily('Ubuntu')

            # ****************** Name ********************
            NameWidget = QWidget()
            NameWidgetLayout = QHBoxLayout(NameWidget)

            # Name Label
            NameLabel = QLabel()
            NameLabel.setText("Name:")
            NameLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            NameLabel.setFont(font)
            NameLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
            NameWidgetLayout.addWidget(NameLabel, 50)

            # Name LineEdit
            NameLineEdit = QLineEdit()
            NameLineEdit.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            NameLineEdit.setText(myresult[0][3] + " " + myresult[0][4])
            NameLineEdit.setCursorPosition(0)
            NameWidgetLayout.addWidget(NameLineEdit, 50)

            AccountInfoDailogLayout.addWidget(NameWidget)

            # ****************** Age ********************
            AgeWidget = QWidget()
            AgeWidgetLayout = QHBoxLayout(AgeWidget)

            # Age Label
            AgeLabel = QLabel()
            AgeLabel.setText("Age:")
            AgeLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            AgeLabel.setFont(font)
            AgeLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
            AgeWidgetLayout.addWidget(AgeLabel, 50)

            # Age LineEdit
            AgeLineEdit = QLineEdit()
            AgeLineEdit.setReadOnly(True)
            AgeLineEdit.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            AgeLineEdit.setText(str(datetime.date.today().year - myresult[0][5].year - ((datetime.date.today().month, datetime.date.today().day) < (myresult[0][5].month, myresult[0][5].day))))
            AgeWidgetLayout.addWidget(AgeLineEdit, 50)

            AccountInfoDailogLayout.addWidget(AgeWidget)

            # ****************** BirthDate ********************
            BirthDateWidget = QWidget()
            BirthDateWidgetLayout = QHBoxLayout(BirthDateWidget)

            # BirthDate Label
            BirthDateLabel = QLabel()
            BirthDateLabel.setText("BirthDate:")
            BirthDateLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            BirthDateLabel.setFont(font)
            BirthDateLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
            BirthDateWidgetLayout.addWidget(BirthDateLabel, 50)

            #BirthDate DateEdit
            BirthDateCalendar = QDateEdit()
            BirthDateCalendar.setCalendarPopup(True)
            BirthDateCalendar.setStyleSheet(
                """
                    background-color: #ffffff;
                    color: #005072;
                    border-width: 1px;
                    border-color: #005072;
                    border-style: solid;
                    border-radius: 10;                
                """
            )
            BirthDateCalendar.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            BirthDateCalendar.setMaximumDate(datetime.datetime.now() - datetime.timedelta(days=5840))
            BirthDateCalendar.setMinimumDate(QDate(1903, 2, 2))
            BirthDateCalendar.setDate(myresult[0][5])
            BirthDateWidgetLayout.addWidget(BirthDateCalendar, 50)

            AccountInfoDailogLayout.addWidget(BirthDateWidget)

            # ****************** Gender ********************
            GenderWidget = QWidget()
            GenderWidgetLayout = QHBoxLayout(GenderWidget)

            # Gender Label
            GenderLabel = QLabel()
            GenderLabel.setText("Gender:")
            GenderLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            GenderLabel.setFont(font)
            GenderLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
            GenderWidgetLayout.addWidget(GenderLabel, 50)

            # Gender LineEdit
            GenderComboBox = QComboBox()
            GenderComboBox.addItem("Male")
            GenderComboBox.addItem("Female")
            GenderComboBox.setCurrentText(myresult[0][6])
            GenderWidgetLayout.addWidget(GenderComboBox, 50)
            AccountInfoDailogLayout.addWidget(GenderWidget)


            # Account Update Button
            UpdateButtonBox = QDialogButtonBox()
            UpdateButtonBox.setCenterButtons(True)
            UpdateButtonBox.setStandardButtons(QDialogButtonBox.Ok)
            UpdateButtonBox.button(QDialogButtonBox.Ok).setText('Update')
            UpdateButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)
            UpdateButtonBox.button(QDialogButtonBox.Ok).setLayoutDirection(Qt.RightToLeft)
            UpdateButtonBox.button(QDialogButtonBox.Ok).setStyleSheet(
                """
                    background-color: #005072;
                    color: #ffffff;
                    border-width: 1px;
                    border-color: #1e1e1e;
                    border-style: solid;
                    border-radius: 10;
                    padding: 3px;
                    font-weight: 700;
                    font-size: 12px;
                    padding-left: 5px;
                    padding-right: 5px;
                    min-width: 40px;
                """
            )
            AccountInfoDailogLayout.addWidget(UpdateButtonBox)

            NameLineEdit.textChanged.connect(lambda: self.UpdateButtonToggle(UpdateButtonBox))
            BirthDateCalendar.dateChanged.connect(lambda: self.UpdateButtonToggle(UpdateButtonBox))
            GenderComboBox.currentTextChanged.connect(lambda: self.UpdateButtonToggle(UpdateButtonBox))

            BirthDateCalendar.dateChanged.connect(lambda: self.BirthDateChanged(AgeLineEdit))

            UpdateButtonBox.accepted.connect(AccountInfoDialogBox.accept)
            UpdateButtonBox.rejected.connect(AccountInfoDialogBox.reject)
            UpdateButtonBox.accepted.connect(lambda: self.UpdateInfo(NameLineEdit, BirthDateCalendar, GenderComboBox))

            AccountInfoDialogBox.exec_()

        else:
            QMessageBox.critical(self, "Error",
                                 'Unable to connect to Server',
                                 QMessageBox.Ok)

    # Toggle Update Button
    def UpdateButtonToggle(self, UpdateButtonBox):
        Widget = self.sender()

        if isinstance(Widget, QLineEdit):
            if len(Widget.text()) == 0:
                UpdateButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)
            else:
                UpdateButtonBox.button(QDialogButtonBox.Ok).setDisabled(False)

        elif isinstance(Widget, QComboBox):
            UpdateButtonBox.button(QDialogButtonBox.Ok).setDisabled(False)

        elif isinstance(Widget, QDateEdit):
            UpdateButtonBox.button(QDialogButtonBox.Ok).setDisabled(False)

    # Update Age
    def BirthDateChanged(self, AgeLineEdit):
        BirthDateCalendar = self.sender()
        BirthDate = datetime.datetime.strptime(BirthDateCalendar.text(), '%m/%d/%Y').date()
        AgeLineEdit.setText(str(datetime.date.today().year - BirthDate.year - ((datetime.date.today().month, datetime.date.today().day) < (BirthDate.month, BirthDate.day))))

    # Update
    def UpdateInfo(self, NameLineEdit, BirthDateCalendar, GenderComboBox):
        try:
            if len(NameLineEdit.text().split(" ", 2)) == 2:
                FirstName = NameLineEdit.text().split(" ", 2)[0]
                LastName = NameLineEdit.text().split(" ", 2)[1]
            else:
                FirstName = NameLineEdit.text()
                LastName = ''

            mycursor = mydb.cursor()
            mycursor.execute(
                """
                Update users set
                first_name = %s,
                last_name = %s,
                dob = %s,
                gender = %s
                where
                email = %s
                """,
                (FirstName,
                 LastName,
                 datetime.datetime.strptime(BirthDateCalendar.text(), '%m/%d/%Y').date(),
                 GenderComboBox.currentText(),
                 self.email,)
            )
            QMessageBox.information(self, "Account",
                                    "Account Info Successfully Updated", QMessageBox.Ok)

            mydb.commit()

        except mysql.connector.Error as error:
            QMessageBox.critical(self, 'Database Error',
                                 'Connection to database failed', QMessageBox.Ok)

    # Logout Dialog
    def LogoutDialog(self):
        LogoutQuestion = QMessageBox.question(self, 'Logout',
                                              'Are you sure you want to Logout?',
                                              QMessageBox.Yes | QMessageBox.No)

        if LogoutQuestion == QMessageBox.Yes:
            self.Logout()
        else:
            pass

    # Logout
    def Logout(self):
        self.settings.setValue('email', '')
        self.LoginLayout()

    # Delete Account Dialog
    def DeleteAccountDialog(self):
        DeleteAccountQuestion = QMessageBox.question(self, 'Delete Account',
                                              'Are you sure you want to Delete this Account?',
                                              QMessageBox.Yes | QMessageBox.No)

        if DeleteAccountQuestion == QMessageBox.Yes:
            self.DeleteAccount()
        else:
            pass

    # Delete Account
    def DeleteAccount(self):
        try:
            mycursor = mydb.cursor()
            mycursor.execute(
                """
                    DELETE FROM messages
                    WHERE
                    sender_id = (Select id from users where email = %s)
                    or
                    receiver_id = (Select id from users where email = %s);
                """,
                (self.email,
                 self.email,)
            )
            mydb.commit()

            mycursor.execute(
                """
                    DELETE FROM users WHERE email = %s
                """,
                (self.email,)
            )
            mydb.commit()

            QMessageBox.information(self, "Account",
                                    "Account Successfully Deleted", QMessageBox.Ok)
            self.Logout()

        except mysql.connector.Error as error:
            QMessageBox.critical(self, 'Database Error',
                                 'Connection to database failed', QMessageBox.Ok)

    # Category List Changed
    def CategoryListCurrentItemChanged(self, MessagesTable):
        CategoryList = self.sender()

        if CategoryList.currentItem().text() == "Inbox":
            self.Inbox(MessagesTable)
        elif CategoryList.currentItem().text() == "Sent":
            self.Sent(MessagesTable)

    # Search Email
    def SearchEmail(self, MessageTable):
        SearchLineEdit = self.sender()

        if len(SearchLineEdit.text()) == 0:
            for i in range(MessageTable.rowCount()):
                MessageTable.showRow(i)

        else:
            items = MessageTable.findItems(SearchLineEdit.text(), Qt.MatchContains)
            for i in range(MessageTable.rowCount()):
                MessageTable.hideRow(i)

            for i in items:
                MessageTable.showRow(i.row())

    # Inbox
    def Inbox(self, MessagesTable):
        while MessagesTable.rowCount() > 0:
            MessagesTable.removeRow(0)

        MessagesTable.setColumnCount(5)
        MessagesTable.setWindowFlags(MessagesTable.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        MessagesTable.setHorizontalHeaderLabels(["Message ID", "From", "Timestamp", "View", "Delete"])
        MessagesTable.horizontalHeader().setStyleSheet("::section {""background-color: #005072;  color: #ffffff;}")

        for i in range(MessagesTable.columnCount()):
            MessagesTable.horizontalHeaderItem(i).setFont(QFont("Ariel Black", 11))
            MessagesTable.horizontalHeaderItem(i).setFont(QFont(MessagesTable.horizontalHeaderItem(i).text(), weight=QFont.Bold))

        try:
            mycursor = mydb.cursor()

            sql_insert_query = """
                                Select msg_id, (SELECT email FROM users where id = sender_id), 
                                datetime, read_flag
                                from 
                                messages
                                where
                                receiver_id = (SELECT id FROM users where email = %s)
                                and 
                                delete_reciever_flag = 0 
                                order by
                                datetime desc 
                            """


            insert_tuple = (self.email,)
            mycursor.execute(sql_insert_query, insert_tuple)
            rowList = mycursor.fetchall()


            for row in rowList:
                MessagesTable.insertRow(rowList.index(row))

                # Message ID
                MessageIDItem = QTableWidgetItem()
                MessageIDItem.setData(Qt.EditRole, QVariant(row[0]))
                MessagesTable.setItem(rowList.index(row), 0, MessageIDItem)
                MessagesTable.item(rowList.index(row), 0).setToolTip(str(row[0]))
                MessagesTable.item(rowList.index(row), 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                MessagesTable.item(rowList.index(row), 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                # Reciever Email
                RecieverEmailItem = QTableWidgetItem()
                RecieverEmailItem.setData(Qt.EditRole, QVariant(row[1]))
                MessagesTable.setItem(rowList.index(row), 1, RecieverEmailItem)
                MessagesTable.item(rowList.index(row), 1).setToolTip(row[1])
                MessagesTable.item(rowList.index(row), 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                MessagesTable.item(rowList.index(row), 1).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                # Time Stramp
                TimestampItem = QTableWidgetItem()
                TimestampItem.setData(Qt.EditRole, QVariant(row[2].strftime("%a %b %d %Y %H:%M:%S")))
                MessagesTable.setItem(rowList.index(row), 2, TimestampItem)
                MessagesTable.item(rowList.index(row), 2).setToolTip(row[2].strftime("%a %b %d %Y %H:%M:%S"))
                MessagesTable.item(rowList.index(row), 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                MessagesTable.item(rowList.index(row), 2).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                # View Button
                viewButton = QPushButton("view")
                viewButton.clicked.connect(lambda: self.ViewInboxMessages(MessagesTable))
                MessagesTable.setCellWidget(rowList.index(row), 3, viewButton)
                MessagesTable.cellWidget(rowList.index(row), 3).setStyleSheet(
                    """
                        QPushButton 
                        {
                            border-width: 0px;
                            color: #005072;
                            padding: 3px;
                            font-size: 12px;
                            padding-left: 5px;
                            padding-right: 5px;
                            min - width: 40px;                            
                        }
                    """
                )

                # delete Button
                deleteButton = QPushButton("Delete")
                deleteButton.clicked.connect(lambda: self.DeleteInboxMessages(MessagesTable))
                MessagesTable.setCellWidget(rowList.index(row), 4, deleteButton)
                MessagesTable.cellWidget(rowList.index(row), 4).setStyleSheet(
                    """
                        QPushButton 
                        {
                            border-width: 0px;
                            color: #005072;
                            padding: 3px;
                            font-size: 12px;
                            padding-left: 5px;
                            padding-right: 5px;
                            min - width: 40px;                            
                        }
                    """
                )

                if row[3] == 0:
                    for j in range(5):
                        try:
                            MessagesTable.item(rowList.index(row), j).setBackground(QColor(177, 221, 240))
                        except Exception as e:
                            MessagesTable.cellWidget(rowList.index(row), j).setStyleSheet("background-color: #b1ddf0")

            MessagesTable.setColumnHidden(0, True)
            MessagesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
            MessagesTable.resizeColumnsToContents()
            MessagesTable.resizeRowsToContents()
            MessagesTable.setSortingEnabled(True)
            MessagesTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

            for i in range(MessagesTable.columnCount()):
                MessagesTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        except mysql.connector.Error as error:
                QMessageBox.critical(self, 'Database Error',
                                    'Connection to database failed', QMessageBox.Ok)

    # View Inbox Messages
    def ViewInboxMessages(self, MessagesTable):
        ViewButton = self.sender()

        if ViewButton:
            Message_id = MessagesTable.item(MessagesTable.indexAt(ViewButton.pos()).row(), 0).text()

            try:
                mycursor = mydb.cursor()

                sql_insert_query = """
                                        Select (SELECT email FROM users where id = sender_id), datetime, enc_key, img_byte_array 
                                        from 
                                        messages
                                        where
                                        msg_id = %s                                         
                                   """

                insert_tuple = (Message_id,)
                mycursor.execute(sql_insert_query, insert_tuple)
                rowList = mycursor.fetchall()

                # Edit Row Dialog
                ViewDialogBox = QDialog()
                ViewDialogBox.setModal(True)
                ViewDialogBox.setWindowTitle("View Message")
                ViewDialogBox.setParent(self)
                ViewDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
                ViewDialogBox.setFixedWidth(self.width / 4)
                ViewDialogBox.setStyleSheet('background-color: #ffffff')

                ViewDailogLayout = QVBoxLayout(ViewDialogBox)
                ViewDailogLayout.setContentsMargins(50, 50, 50, 50)

                font = QFont()
                font.setBold(True)
                font.setPointSize(9)
                font.setFamily('Ubuntu')

                # ****************** To ********************
                # From Label
                FromLabel = QLabel()
                FromLabel.setText("From:")
                FromLabel.setAlignment(Qt.AlignVCenter)
                FromLabel.setFont(font)
                FromLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
                ViewDailogLayout.addWidget(FromLabel)

                # To LineEdit
                FromLineEdit = QLineEdit()
                FromLineEdit.setAlignment(Qt.AlignVCenter)
                FromLineEdit.setText(rowList[0][0])
                FromLineEdit.setReadOnly(True)
                ViewDailogLayout.addWidget(FromLineEdit)

                # ****************** TimeStamp ********************
                # TimeStamp Label
                TimeStampLabel = QLabel()
                TimeStampLabel.setText("TimeStamp:")
                TimeStampLabel.setAlignment(Qt.AlignVCenter)
                TimeStampLabel.setFont(font)
                TimeStampLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
                ViewDailogLayout.addWidget(TimeStampLabel)

                # TimeStamp LineEdit
                TimeStampLineEdit = QLineEdit()
                TimeStampLineEdit.setAlignment(Qt.AlignVCenter)
                TimeStampLineEdit.setText(rowList[0][1].strftime("%a %b %d %Y %H:%M:%S"))
                TimeStampLineEdit.setReadOnly(True)
                ViewDailogLayout.addWidget(TimeStampLineEdit)

                # ****************** Message ********************
                # Message Label
                MessageLabel = QLabel()
                MessageLabel.setText("Message:")
                MessageLabel.setAlignment(Qt.AlignVCenter)
                MessageLabel.setFont(font)
                MessageLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
                ViewDailogLayout.addWidget(MessageLabel)

                # Message LineEdit
                MessageTextEdit = QTextEdit()
                MessageTextEdit.setAlignment(Qt.AlignVCenter)
                crypto_steganography = CryptoSteganography(rowList[0][2])
                MessageTextEdit.setText(crypto_steganography.retrieve(Image.open(io.BytesIO(rowList[0][3]))))
                MessageTextEdit.setReadOnly(True)
                ViewDailogLayout.addWidget(MessageTextEdit)

                # ******************* Button Box *********************
                ViewButtonBox = QDialogButtonBox()
                ViewButtonBox.setCenterButtons(True)
                ViewButtonBox.setStandardButtons(QDialogButtonBox.Ok)
                ViewButtonBox.button(QDialogButtonBox.Ok).setText('View Encrypted Image')
                ViewButtonBox.button(QDialogButtonBox.Ok).setLayoutDirection(Qt.RightToLeft)
                ViewButtonBox.button(QDialogButtonBox.Ok).setStyleSheet(
                    """
                        background-color: #005072;
                        color: #ffffff;
                        border-width: 1px;
                        border-color: #1e1e1e;
                        border-style: solid;
                        border-radius: 10;
                        padding: 3px;
                        font-weight: 700;
                        font-size: 12px;
                        padding-left: 5px;
                        padding-right: 5px;
                        min-width: 40px;
                    """
                )
                ViewDailogLayout.addWidget(ViewButtonBox)

                ViewButtonBox.accepted.connect(ViewDialogBox.accept)
                ViewButtonBox.rejected.connect(ViewDialogBox.reject)
                ViewButtonBox.accepted.connect(lambda: Image.open(io.BytesIO(rowList[0][3])).show())

                ViewDialogBox.exec_()

                mycursor.execute("Update messages set read_flag = 1 where msg_id = %s", (Message_id,))
                mydb.commit()

                self.Inbox(MessagesTable)

            except mysql.connector.Error as error:
                QMessageBox.critical(self, 'Database Error',
                                     'Connection to database failed', QMessageBox.Ok)

    # Toggle Decrypt Button
    def ToggleDecryptButton(self, KeyLineEdit, ViewButtonBox):
        # Empty Fields
        if len(KeyLineEdit.text()) == 0:
            ViewButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        else:
            ViewButtonBox.button(QDialogButtonBox.Ok).setDisabled(False)

    # Delete Inbox Messages
    def DeleteInboxMessages(self, MessagesTable):
        DeleteButton = self.sender()
        if DeleteButton:
            Message_id = MessagesTable.item(MessagesTable.indexAt(DeleteButton.pos()).row(), 0).text()

            DeleteMessageQuestion = QMessageBox.question(self, 'Delete Message',
                                                         'Are you sure you want to Delete this message?',
                                                         QMessageBox.Yes | QMessageBox.No)

            if DeleteMessageQuestion == QMessageBox.Yes:
                try:
                    mycursor = mydb.cursor()
                    mycursor.execute("Update messages set delete_reciever_flag = 1 where msg_id = %s", (Message_id,))
                    mydb.commit()
                    self.Inbox(MessagesTable)

                except mysql.connector.Error as error:
                    QMessageBox.critical(self, 'Database Error',
                                    'Connection to database failed', QMessageBox.Ok)
            else:
                pass

    # Sent
    def Sent(self, MessagesTable):
        while MessagesTable.rowCount() > 0:
            MessagesTable.removeRow(0)

        MessagesTable.setColumnCount(5)
        MessagesTable.setWindowFlags(MessagesTable.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        MessagesTable.setHorizontalHeaderLabels(["Message ID", "To", "Timestamp", "View", "Delete"])
        MessagesTable.horizontalHeader().setStyleSheet("::section {""background-color: #005072;  color: #ffffff;}")

        for i in range(MessagesTable.columnCount()):
            MessagesTable.horizontalHeaderItem(i).setFont(QFont("Ariel Black", 11))
            MessagesTable.horizontalHeaderItem(i).setFont(QFont(MessagesTable.horizontalHeaderItem(i).text(), weight=QFont.Bold))

        try:

            mycursor = mydb.cursor()

            sql_insert_query = """
                                    Select msg_id, (SELECT email FROM users where id = receiver_id), datetime
                                    from 
                                    messages
                                    where
                                    sender_id = (SELECT id FROM users where email = %s)
                                    and 
                                    delete_sender_flag = 0                                
                                    order by
                                    datetime desc 
                            """

            insert_tuple = (self.email,)
            mycursor.execute(sql_insert_query, insert_tuple)
            rowList = mycursor.fetchall()

            for row in rowList:
                MessagesTable.insertRow(rowList.index(row))

                # Message ID
                MessageIDItem = QTableWidgetItem()
                MessageIDItem.setData(Qt.EditRole, QVariant(row[0]))
                MessagesTable.setItem(rowList.index(row), 0, MessageIDItem)
                MessagesTable.item(rowList.index(row), 0).setToolTip(str(row[0]))
                MessagesTable.item(rowList.index(row), 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                MessagesTable.item(rowList.index(row), 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                # Reciever Email
                RecieverEmailItem = QTableWidgetItem()
                RecieverEmailItem.setData(Qt.EditRole, QVariant(row[1]))
                MessagesTable.setItem(rowList.index(row), 1, RecieverEmailItem)
                MessagesTable.item(rowList.index(row), 1).setToolTip(row[1])
                MessagesTable.item(rowList.index(row), 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                MessagesTable.item(rowList.index(row), 1).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                # Time Stramp
                TimestampItem = QTableWidgetItem()
                TimestampItem.setData(Qt.EditRole, QVariant(row[2].strftime("%a %b %d %Y %H:%M:%S")))
                MessagesTable.setItem(rowList.index(row), 2, TimestampItem)
                MessagesTable.item(rowList.index(row), 2).setToolTip(row[2].strftime("%a %b %d %Y %H:%M:%S"))
                MessagesTable.item(rowList.index(row), 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                MessagesTable.item(rowList.index(row), 2).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                # View Button
                viewButton = QPushButton("view")
                viewButton.clicked.connect(lambda: self.ViewSentMessages(MessagesTable))
                MessagesTable.setCellWidget(rowList.index(row), 3, viewButton)
                MessagesTable.cellWidget(rowList.index(row), 3).setStyleSheet(
                    """
                        QPushButton 
                        {                            
                            border-width: 0px;
                            color: #005072;
                            padding: 3px;
                            font-size: 12px;
                            padding-left: 5px;
                            padding-right: 5px;
                            min - width: 40px;                            
                        }
                    """
                )

                # delete Button
                deleteButton = QPushButton("Delete")
                deleteButton.clicked.connect(lambda: self.DeleteSentMessages(MessagesTable))
                MessagesTable.setCellWidget(rowList.index(row), 4, deleteButton)
                MessagesTable.cellWidget(rowList.index(row), 4).setStyleSheet(
                    """
                        QPushButton 
                        {
                            border-width: 0px;
                            color: #005072;
                            padding: 3px;
                            font-size: 12px;
                            padding-left: 5px;
                            padding-right: 5px;
                            min - width: 40px;                            
                        }
                    """
                )

            MessagesTable.setColumnHidden(0, True)
            MessagesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
            MessagesTable.resizeColumnsToContents()
            MessagesTable.resizeRowsToContents()
            MessagesTable.setSortingEnabled(True)
            MessagesTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

            for i in range(MessagesTable.columnCount()):
                MessagesTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        except mysql.connector.Error as error:
                QMessageBox.critical(self, 'Database Error',
                                    'Connection to database failed', QMessageBox.Ok)

    # View Send Messages
    def ViewSentMessages(self, MessagesTable):
        ViewButton = self.sender()
        if ViewButton:
            Message_id = MessagesTable.item(MessagesTable.indexAt(ViewButton.pos()).row(), 0).text()

            try: 
                mycursor = mydb.cursor()

                sql_insert_query = """
                                        Select (SELECT email FROM users where id = receiver_id), datetime, enc_key, img_byte_array 
                                        from 
                                        messages
                                        where
                                        msg_id = %s                                         
                                """

                insert_tuple = (Message_id,)
                mycursor.execute(sql_insert_query, insert_tuple)
                rowList = mycursor.fetchall()

                # Edit Row Dialog
                ViewDialogBox = QDialog()
                ViewDialogBox.setModal(True)
                ViewDialogBox.setWindowTitle("View Message")
                ViewDialogBox.setParent(self)
                ViewDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
                ViewDialogBox.setFixedWidth(self.width / 4)
                ViewDialogBox.setStyleSheet('background-color: #ffffff')

                ViewDailogLayout = QVBoxLayout(ViewDialogBox)
                ViewDailogLayout.setContentsMargins(50, 50, 50, 50)

                font = QFont()
                font.setBold(True)
                font.setPointSize(9)
                font.setFamily('Ubuntu')

                # ****************** To ********************
                # To Label
                ToLabel = QLabel()
                ToLabel.setText("To:")
                ToLabel.setAlignment(Qt.AlignVCenter)
                ToLabel.setFont(font)
                ToLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
                ViewDailogLayout.addWidget(ToLabel)

                # To LineEdit
                ToLineEdit = QLineEdit()
                ToLineEdit.setAlignment(Qt.AlignVCenter)
                ToLineEdit.setText(rowList[0][0])
                ToLineEdit.setReadOnly(True)
                ToLineEdit.setValidator(QIntValidator(0, 10000, self))
                ViewDailogLayout.addWidget(ToLineEdit)

                # ****************** TimeStamp ********************
                # TimeStamp Label
                TimeStampLabel = QLabel()
                TimeStampLabel.setText("TimeStamp:")
                TimeStampLabel.setAlignment(Qt.AlignVCenter)
                TimeStampLabel.setFont(font)
                TimeStampLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
                ViewDailogLayout.addWidget(TimeStampLabel)

                # TimeStamp LineEdit
                TimeStampLineEdit = QLineEdit()
                TimeStampLineEdit.setAlignment(Qt.AlignVCenter)
                TimeStampLineEdit.setText(rowList[0][1].strftime("%a %b %d %Y %H:%M:%S"))
                TimeStampLineEdit.setReadOnly(True)
                ViewDailogLayout.addWidget(TimeStampLineEdit)

                # ****************** Message ********************
                # Message Label
                MessageLabel = QLabel()
                MessageLabel.setText("Message:")
                MessageLabel.setAlignment(Qt.AlignVCenter)
                MessageLabel.setFont(font)
                MessageLabel.setStyleSheet("background-color: rgba(0,0,0,0%);color: #005072;")
                ViewDailogLayout.addWidget(MessageLabel)

                # Message LineEdit
                MessageTextEdit = QTextEdit()
                MessageTextEdit.setAlignment(Qt.AlignVCenter)
                crypto_steganography = CryptoSteganography(rowList[0][2])
                MessageTextEdit.setText(crypto_steganography.retrieve(Image.open(io.BytesIO(rowList[0][3]))))
                MessageTextEdit.setReadOnly(True)
                ViewDailogLayout.addWidget(MessageTextEdit)

                # ******************* Button Box *********************
                ViewButtonBox = QDialogButtonBox()
                ViewButtonBox.setCenterButtons(True)
                ViewButtonBox.setStandardButtons(QDialogButtonBox.Ok)
                ViewButtonBox.button(QDialogButtonBox.Ok).setText('View Encrypted Image')
                ViewButtonBox.button(QDialogButtonBox.Ok).setLayoutDirection(Qt.RightToLeft)
                ViewButtonBox.button(QDialogButtonBox.Ok).setStyleSheet(
                    """
                        background-color: #005072;
                        color: #ffffff;
                        border-width: 1px;
                        border-color: #1e1e1e;
                        border-style: solid;
                        border-radius: 10;
                        padding: 3px;
                        font-weight: 700;
                        font-size: 12px;
                        padding-left: 5px;
                        padding-right: 5px;
                        min-width: 40px;
                    """
                )
                ViewDailogLayout.addWidget(ViewButtonBox)

                ViewButtonBox.accepted.connect(ViewDialogBox.accept)
                ViewButtonBox.rejected.connect(ViewDialogBox.reject)
                ViewButtonBox.accepted.connect(lambda: Image.open(io.BytesIO(rowList[0][3])).show())

                ViewDialogBox.exec_()

            except mysql.connector.Error as error:
                QMessageBox.critical(self, 'Database Error',
                                    'Connection to database failed', QMessageBox.Ok)

    # Delete Send Messages
    def DeleteSentMessages(self, MessagesTable):
        DeleteButton = self.sender()
        if DeleteButton:
            Message_id = MessagesTable.item(MessagesTable.indexAt(DeleteButton.pos()).row(), 0).text()

            DeleteMessageQuestion = QMessageBox.question(self, 'Delete Message',
                                                         'Are you sure you want to Delete this message?',
                                                         QMessageBox.Yes | QMessageBox.No)

            if DeleteMessageQuestion == QMessageBox.Yes:
                mycursor = mydb.cursor()
                mycursor.execute("Update messages set delete_sender_flag = 1 where msg_id = %s", (Message_id,))
                mydb.commit()
                self.Sent(MessagesTable)

            else:
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

    DBError = False
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="STD"
        )
    except:
        DBError = True

    STD = Window()
    STD.setStyleSheet(
        """
            QPushButton::menu-indicator 
            {
                image: url(myindicator.png);
                subcontrol-position: right center;
                subcontrol-origin: padding;
                left: -2px;
            }

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
            
            QMessageBox
            {
                background-color: #ffffff;
                color: #005072;
            }
            
            QWidget:focus, QMessageBox:focus
            {
                border: 1px solid darkgray;
            }
            
            QLineEdit
            {
                padding: 1px;
                border-style: solid;
                color: #005072;
                border: 1px solid #005072;
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
                border: 1px solid #005072;
                border-radius: 5;
                color: #005072;                
            }
            
            QComboBox:hover,QPushButton:hover
            {
                border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #005b82, stop: 1 #d4e8f2);
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
            QTextEdit
            {
                color: #005072;
                border: 1px solid #005072;
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
    if not DBError:
        if STD.email == '':
            STD.LoginLayout()
        else:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM users where email = %s",
                             (STD.email,))

            myresult = mycursor.fetchall()

            if not len(myresult):
                STD.settings.setValue('email', '')
                STD.LoginLayout()
            else:
                STD.MainWindow()

        STD.show()
    else:
        STD.show()
        QMessageBox.critical(STD, 'Database Error',
                            'Could Not connect to Database', QMessageBox.Ok)

        sys.exit(0)

    sys.exit(App.exec())
