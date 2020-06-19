from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PIL import Image
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from stegano import lsb

import os, sys, datetime, mysql.connector, re, hashlib, io, base64, hashlib

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
        self.title = "Crypto"

        self.width = QDesktopWidget().screenGeometry(0).width()/2
        self.height = QDesktopWidget().screenGeometry(0).height()*0.8

        self.settings = QSettings('Crypto', 'Crypto')
        self.initWindows()

    # Initiate Windows
    def initWindows(self):
        self.setWindowIcon(QIcon('Images/Logo.png'))
        self.setWindowTitle(self.title)
        self.setFixedHeight(self.height)
        self.setFixedWidth(self.width)

        self.CentralWidget = QWidget(self)
        self.setCentralWidget(self.CentralWidget)



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

        self.email = self.settings.value('email', '')

        if self.email == '':
            self.LoginLayout()
        else:
            self.MainWindow()

        #self.MainWindow()

    # Login Layout
    def LoginLayout(self):
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
        emailLabel = QLabel()
        emailLabel.setText("Email")
        emailLabel.setAlignment(Qt.AlignVCenter)
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
                }
            """
        )
        CentralWidgetLayout.addWidget(emailLineEdit)

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

    # Register Layout
    def RegisterLayout(self):
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

        # Birth Date Label
        BirthDateLabel = QLabel()
        BirthDateLabel.setText("Birth Date:")
        BirthDateLabel.setAlignment(Qt.AlignVCenter)
        CentralWidgetLayout.addWidget(BirthDateLabel)

        # Birth Date Calendar
        BirthDateCalendar = QDateEdit()
        BirthDateCalendar.setCalendarPopup(True)
        BirthDateCalendar.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
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

        FirstNameLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        LastNameLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        emailLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        BirthDateCalendar.dateChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        EnterPasswordLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))
        RetypePasswordLineEdit.textChanged.connect(lambda: self.RegisterButtonToggle(FirstNameLineEdit, LastNameLineEdit, emailLineEdit, BirthDateCalendar, EnterPasswordLineEdit, RetypePasswordLineEdit, RegisterButton))

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
        elif not EnterPasswordLineEdit.text() == RetypePasswordLineEdit.text():
            EnterPasswordLineEdit.setStyleSheet("border: 1px solid red;")
            RetypePasswordLineEdit.setStyleSheet("border: 1px solid red;")
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
        TopWidget.setStyleSheet("background-color: white;")

        # Top Widget Layout
        TopWidgetLayout = QHBoxLayout(TopWidget)
        TopWidgetLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Compose Button
        ComposeButton = QPushButton()
        ComposeButton.setText("Compose")
        ComposeButton.setIcon(QIcon("Images/Compose.png"))
        ComposeButton.setIconSize(QSize(25, 25))
        ComposeButton.setStyleSheet(
            """
                QPushButton{
                    background-color: black;
                    color: white;
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
                    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffffff, stop: 1 #d4e8f2);
                }                
            """
        )
        ComposeButton.clicked.connect(lambda: self.ComposeMessageDialog())

        TopWidgetLayout.addWidget(ComposeButton, 15)
        TopWidgetLayout.addWidget(QWidget(), 70)

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

        AccountButton = QAction('Account', self)
        AccountButton.setStatusTip('Account')
        AccountButton.triggered.connect(self.AccountInfo)
        menu.addAction(AccountButton)

        LogoutButton = QAction('Logout', self)
        LogoutButton.setStatusTip('Logout')
        LogoutButton.triggered.connect(self.Logout)
        menu.addAction(LogoutButton)

        SettingButton.setMenu(menu)

        TopWidgetLayout.addWidget(SettingButton, 15)

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
                    color: black;
                    background-color: white;                        
                }
                
                QListWidget::item:selected 
                {
                    color: white;
                    background-color: black;
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

        # Table Widget
        MessagesTable = QTableWidget()
        BottomWidgetLayout.addWidget(MessagesTable, 75)

        self.Inbox(MessagesTable)

        CategoryList.currentItemChanged.connect(lambda: self.CategoryListCurrentItemChanged(MessagesTable))
        CentralWidgetLayout.addWidget(BottomWidget, 90)

    # Compose Message
    def ComposeMessageDialog(self):
        # Compose Message Dialog
        ComposeMessageDialogBox = QDialog()
        ComposeMessageDialogBox.setModal(True)
        ComposeMessageDialogBox.setWindowTitle("Compose Message")
        ComposeMessageDialogBox.setParent(self)
        ComposeMessageDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        ComposeMessageDialogBox.setFixedWidth(self.width / 2)

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
        ImageFileLayout.addWidget(ImageBrowseButton)

        ComposeMessageDailogLayout.addWidget(ImageFileWidget)

        # ********************** To *************************
        SendToLabel = QLabel()
        SendToLabel.setText("To")
        ComposeMessageDailogLayout.addWidget(SendToLabel)

        SendToLineEdit = QLineEdit()
        ComposeMessageDailogLayout.addWidget(SendToLineEdit)

        # ****************** Text Message ********************
        MessageLabel = QLabel()
        MessageLabel.setText("Message")
        ComposeMessageDailogLayout.addWidget(MessageLabel)

        MessageTextEdit = QTextEdit()
        ComposeMessageDailogLayout.addWidget(MessageTextEdit)

        # ********************** Key *************************
        KeyLabel = QLabel()
        KeyLabel.setText("Key")
        ComposeMessageDailogLayout.addWidget(KeyLabel)

        KeyLineEdit = QLineEdit()
        KeyLineEdit.setValidator(QIntValidator(0, 10000, self))
        ComposeMessageDailogLayout.addWidget(KeyLineEdit)

        # ******************* Button Box *********************
        ComposeButtonBox = QDialogButtonBox()
        ComposeButtonBox.setCenterButtons(True)
        ComposeButtonBox.setStandardButtons(QDialogButtonBox.Ok)
        ComposeButtonBox.button(QDialogButtonBox.Ok).setText('Send')
        ComposeButtonBox.button(QDialogButtonBox.Ok).setIcon(QIcon("Images/Send.png"))
        ComposeButtonBox.button(QDialogButtonBox.Ok).setLayoutDirection(Qt.RightToLeft)
        ComposeButtonBox.button(QDialogButtonBox.Ok).setStyleSheet(
            """
                background-color: black;
                color: white;
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

        ImageFilePathLineEdit.textChanged.connect(lambda: self.ToggleSendButton(ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, KeyLineEdit, ComposeButtonBox))
        SendToLineEdit.textChanged.connect(lambda: self.ToggleSendButton(ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, KeyLineEdit, ComposeButtonBox))
        MessageTextEdit.textChanged.connect(lambda: self.ToggleSendButton(ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, KeyLineEdit, ComposeButtonBox))
        KeyLineEdit.textChanged.connect(lambda: self.ToggleSendButton(ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, KeyLineEdit, ComposeButtonBox))

        ComposeButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        ComposeMessageDailogLayout.addWidget(ComposeButtonBox)

        ComposeButtonBox.accepted.connect(ComposeMessageDialogBox.accept)
        ComposeButtonBox.rejected.connect(ComposeMessageDialogBox.reject)

        ComposeButtonBox.accepted.connect(lambda: self.SendMessage(ImageFilePathLineEdit.text(),
                                                                   SendToLineEdit.text(),
                                                                   MessageTextEdit.toPlainText(),
                                                                   KeyLineEdit.text()))

        ComposeMessageDialogBox.exec_()

    # Toggle Send Button
    def ToggleSendButton(self, ImageFilePathLineEdit, SendToLineEdit, MessageTextEdit, KeyLineEdit, ComposeButtonBox):
        if len(ImageFilePathLineEdit.text()) == 0 or len(SendToLineEdit.text()) == 0 or len(MessageTextEdit.toPlainText()) == 0 or len(KeyLineEdit.text()) == 0:
            ImageFilePathLineEdit.setStyleSheet("border: 1px solid black;")
            SendToLineEdit.setStyleSheet("border: 1px solid black;")
            MessageTextEdit.setStyleSheet("border: 1px solid black;")
            KeyLineEdit.setStyleSheet("border: 1px solid black;")
            ComposeButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        # Email
        elif not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', SendToLineEdit.text()):
            SendToLineEdit.setStyleSheet("border: 1px solid red;")
            ComposeButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        else:
            ImageFilePathLineEdit.setStyleSheet("border: 1px solid black;")
            SendToLineEdit.setStyleSheet("border: 1px solid black;")
            MessageTextEdit.setStyleSheet("border: 1px solid black;")
            KeyLineEdit.setStyleSheet("border: 1px solid black;")
            ComposeButtonBox.button(QDialogButtonBox.Ok).setDisabled(False)

    # Send Message
    def SendMessage(self, ImageFilePath, To, Message, Key):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users where email = %s", (To,))

        myresult = mycursor.fetchall()

        if len(myresult) > 0:

            sql_insert_query = """ 
                                    INSERT INTO messages (sender_id, receiver_id, enc_key, img_byte_array, datetime, read_flag)
                                    VALUES(
                                        (SELECT id FROM users where email = %s), 
                                        (SELECT id FROM users where email = %s), 
                                        %s, %s, SYSDATE(), 0) 
                               """

            # key inserted here
            crypto_steganography = CryptoSteganography(Key)

            # Image Loaded
            SteganoImage = Image.open(ImageFilePath)

            if SteganoImage.mode == "RGB":
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

            else:
                QMessageBox.critical(self, 'Message Error',
                                     'Please select and RGB Image', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Message Error',
                                 'No Such Email Address Exist', QMessageBox.Ok)

    # Compose FIle Button
    def ComposeChooseButton(self, ImageFilePathLineEdit):
        path = QFileDialog.getOpenFileName(self, 'Open Image File', "", 'Image files (*.png *.bmp *.jpeg *.jpg *.webp *.tiff *.tif *.pfm *.jp2 *.hdr *.pic *.exr *.ras *.sr *.pbm *.pgm *.ppm *.pxm *.pnm)')

        if all(path):
            ImageFilePathLineEdit.setText(path[0])

    # Account Information
    def AccountInfo(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users where email = %s",  (self.email,))

        myresult = mycursor.fetchall()

        if len(myresult) > 0:
            # Edit Row Dialog
            AccountInfoDialogBox = QDialog()
            AccountInfoDialogBox.setModal(True)
            AccountInfoDialogBox.setWindowTitle("Account Information")
            AccountInfoDialogBox.setParent(self)
            AccountInfoDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
            AccountInfoDialogBox.setFixedWidth(self.width / 2)

            AccountInfoDailogLayout = QVBoxLayout(AccountInfoDialogBox)
            AccountInfoDailogLayout.setContentsMargins(50, 50, 50, 50)


            # ****************** Email ********************
            EmailWidget = QWidget()
            EmailWidgetLayout = QHBoxLayout(EmailWidget)

            # Email Label
            EmailLabel = QLabel()
            EmailLabel.setText("Email:")
            EmailLabel.setAlignment(Qt.AlignVCenter)
            EmailWidgetLayout.addWidget(EmailLabel, 25)

            # Email LineEdit
            EmailLineEdit = QLineEdit()
            EmailLineEdit.setReadOnly(True)
            EmailLineEdit.setText(myresult[0][1])
            EmailLineEdit.setAlignment(Qt.AlignVCenter)
            EmailWidgetLayout.addWidget(EmailLineEdit, 75)

            AccountInfoDailogLayout.addWidget(EmailWidget)

            # ****************** Name ********************
            NameWidget = QWidget()
            NameWidgetLayout = QHBoxLayout(NameWidget)

            # Name Label
            NameLabel = QLabel()
            NameLabel.setText("Name:")
            NameLabel.setAlignment(Qt.AlignVCenter)
            NameWidgetLayout.addWidget(NameLabel, 25)

            # Name LineEdit
            NameLineEdit = QLineEdit()
            NameLineEdit.setReadOnly(True)
            NameLineEdit.setText(myresult[0][3] + " " + myresult[0][4])
            NameLineEdit.setAlignment(Qt.AlignVCenter)
            NameWidgetLayout.addWidget(NameLineEdit, 75)

            AccountInfoDailogLayout.addWidget(NameWidget)

            # ****************** Age ********************
            AgeWidget = QWidget()
            AgeWidgetLayout = QHBoxLayout(AgeWidget)

            # Age Label
            AgeLabel = QLabel()
            AgeLabel.setText("Age:")
            AgeLabel.setAlignment(Qt.AlignVCenter)
            AgeWidgetLayout.addWidget(AgeLabel, 25)

            # Age LineEdit
            AgeLineEdit = QLineEdit()
            AgeLineEdit.setReadOnly(True)
            AgeLineEdit.setText(str(datetime.date.today().year - myresult[0][5].year - ((datetime.date.today().month, datetime.date.today().day) < (myresult[0][5].month, myresult[0][5].day))))
            AgeLineEdit.setAlignment(Qt.AlignVCenter)
            AgeWidgetLayout.addWidget(AgeLineEdit, 75)

            AccountInfoDailogLayout.addWidget(AgeWidget)

            # ****************** BirthDate ********************
            BirthDateWidget = QWidget()
            BirthDateWidgetLayout = QHBoxLayout(BirthDateWidget)

            # BirthDate Label
            BirthDateLabel = QLabel()
            BirthDateLabel.setText("BirthDate:")
            BirthDateLabel.setAlignment(Qt.AlignVCenter)
            BirthDateWidgetLayout.addWidget(BirthDateLabel, 25)

            # BirthDate LineEdit
            BirthDateLineEdit = QLineEdit()
            BirthDateLineEdit.setReadOnly(True)
            BirthDateLineEdit.setText(myresult[0][5].strftime("%a %b %d %Y"))
            BirthDateLineEdit.setAlignment(Qt.AlignVCenter)
            BirthDateWidgetLayout.addWidget(BirthDateLineEdit, 75)

            AccountInfoDailogLayout.addWidget(BirthDateWidget)

            # ****************** Gender ********************
            GenderWidget = QWidget()
            GenderWidgetLayout = QHBoxLayout(GenderWidget)

            # Gender Label
            GenderLabel = QLabel()
            GenderLabel.setText("Gender:")
            GenderLabel.setAlignment(Qt.AlignVCenter)
            GenderWidgetLayout.addWidget(GenderLabel, 25)

            # Gender LineEdit
            GenderLineEdit = QLineEdit()
            GenderLineEdit.setReadOnly(True)
            GenderLineEdit.setText(myresult[0][6])
            GenderLineEdit.setAlignment(Qt.AlignVCenter)
            GenderWidgetLayout.addWidget(GenderLineEdit, 75)

            AccountInfoDailogLayout.addWidget(GenderWidget)

            AccountInfoDialogBox.exec_()

        else:
            QMessageBox.critical(self, "Error",
                                 'Unable to connect to Server',
                                 QMessageBox.Ok)

    # Logout
    def Logout(self):
        self.settings.setValue('email', '')
        self.LoginLayout()

    # Category List Changed
    def CategoryListCurrentItemChanged(self, MessagesTable):
        CategoryList = self.sender()

        if CategoryList.currentItem().text() == "Inbox":
            self.Inbox(MessagesTable)
        elif CategoryList.currentItem().text() == "Sent":
            self.Sent(MessagesTable)

    # Inbox
    def Inbox(self, MessagesTable):
        while MessagesTable.rowCount() > 0:
            MessagesTable.removeRow(0)

        MessagesTable.setColumnCount(5)
        MessagesTable.setWindowFlags(MessagesTable.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        MessagesTable.setHorizontalHeaderLabels(["Message ID", "Sender", "Timestramp", "View", "Delete"])
        MessagesTable.horizontalHeader().setStyleSheet("::section {""background-color: black;  color: white;}")

        for i in range(MessagesTable.columnCount()):
            MessagesTable.horizontalHeaderItem(i).setFont(QFont("Ariel Black", 11))
            MessagesTable.horizontalHeaderItem(i).setFont(QFont(MessagesTable.horizontalHeaderItem(i).text(), weight=QFont.Bold))

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

            if row[3] == 0:
                pass

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
            TimestrampItem = QTableWidgetItem()
            TimestrampItem.setData(Qt.EditRole, QVariant(row[2].strftime("%m/%d/%Y, %H:%M:%S")))
            MessagesTable.setItem(rowList.index(row), 2, TimestrampItem)
            MessagesTable.item(rowList.index(row), 2).setToolTip(row[2].strftime("%m/%d/%Y, %H:%M:%S"))
            MessagesTable.item(rowList.index(row), 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            MessagesTable.item(rowList.index(row), 2).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

            # View Button
            viewButton = QPushButton("view")
            viewButton.clicked.connect(lambda: self.ViewInboxMessages(MessagesTable))
            MessagesTable.setCellWidget(rowList.index(row), 3, viewButton)

            # delete Button
            deleteButton = QPushButton("Delete")
            deleteButton.clicked.connect(lambda: self.DeleteInboxMessages(MessagesTable))
            MessagesTable.setCellWidget(rowList.index(row), 4, deleteButton)

        MessagesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        MessagesTable.resizeColumnsToContents()
        MessagesTable.resizeRowsToContents()
        MessagesTable.setSortingEnabled(True)
        MessagesTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        for i in range(MessagesTable.columnCount()):
            MessagesTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    # View Inbox Messages
    def ViewInboxMessages(self, MessagesTable):
        ViewButton = self.sender()
        if ViewButton:
            Message_id = MessagesTable.item(MessagesTable.indexAt(ViewButton.pos()).row(), 0).text()

            # Edit Row Dialog
            ViewDialogBox = QDialog()
            ViewDialogBox.setModal(True)
            ViewDialogBox.setWindowTitle("View Message")
            ViewDialogBox.setParent(self)
            ViewDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
            ViewDialogBox.setFixedWidth(self.width / 2)

            ViewDailogLayout = QVBoxLayout(ViewDialogBox)
            ViewDailogLayout.setContentsMargins(50, 50, 50, 50)

            # ****************** Key ********************
            KeyWidget = QWidget()
            KeyWidgetLayout = QHBoxLayout(KeyWidget)

            # Key Label
            KeyLabel = QLabel()
            KeyLabel.setText("Key:")
            KeyLabel.setAlignment(Qt.AlignVCenter)
            KeyWidgetLayout.addWidget(KeyLabel, 25)

            # Key LineEdit
            KeyLineEdit = QLineEdit()
            KeyLineEdit.setAlignment(Qt.AlignVCenter)
            KeyLineEdit.setValidator(QIntValidator(0, 10000, self))
            KeyWidgetLayout.addWidget(KeyLineEdit, 75)

            ViewDailogLayout.addWidget(KeyWidget)

            # ******************* Button Box *********************
            ViewButtonBox = QDialogButtonBox()
            ViewButtonBox.setCenterButtons(True)
            ViewButtonBox.setStandardButtons(QDialogButtonBox.Ok)
            ViewButtonBox.button(QDialogButtonBox.Ok).setText('Decrypt')
            ViewButtonBox.button(QDialogButtonBox.Ok).setIcon(QIcon("Images/Decrypt.png"))
            ViewButtonBox.button(QDialogButtonBox.Ok).setLayoutDirection(Qt.RightToLeft)
            ViewButtonBox.button(QDialogButtonBox.Ok).setStyleSheet(
                """
                    background-color: black;
                    color: white;
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
            ViewButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)
            ViewDailogLayout.addWidget(ViewButtonBox)

            KeyLineEdit.textChanged.connect(lambda: self.ToggleDecryptButton(KeyLineEdit, ViewButtonBox))

            ViewButtonBox.accepted.connect(ViewDialogBox.accept)
            ViewButtonBox.rejected.connect(ViewDialogBox.reject)

            ViewButtonBox.accepted.connect(lambda: self.DecryptMessage(Message_id, KeyLineEdit.text()))

            ViewDialogBox.exec_()

    # Toggle Decrypt Button
    def ToggleDecryptButton(self, KeyLineEdit, ViewButtonBox):
        # Empty Fields
        if len(KeyLineEdit.text()) == 0:
            ViewButtonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        else:
            ViewButtonBox.button(QDialogButtonBox.Ok).setDisabled(False)

    # Decrypt Message
    def DecryptMessage(self, Message_id, Key):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT img_byte_array FROM messages where msg_id = %s", (Message_id,))

        myresult = mycursor.fetchall()

        crypto_steganography = CryptoSteganography(Key)
        message = crypto_steganography.retrieve(Image.open(io.BytesIO(myresult[0][0])))

        if message is not None:
            mycursor.execute("Update messages set read_flag = 1 where msg_id = %s", (Message_id,))
            mydb.commit()

            QMessageBox.information(self, "Success", "Decryption Successful", QMessageBox.Ok)

            # Edit Row Dialog
            DecryptMessageDialogBox = QDialog()
            DecryptMessageDialogBox.setModal(True)
            DecryptMessageDialogBox.setWindowTitle("View Message")
            DecryptMessageDialogBox.setParent(self)
            DecryptMessageDialogBox.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
            DecryptMessageDialogBox.setFixedWidth(self.width / 2)

            DecryptMessageDailogLayout = QVBoxLayout(DecryptMessageDialogBox)
            DecryptMessageDailogLayout.setContentsMargins(50, 50, 50, 50)

            # Message Label
            MessageLabel = QLabel()
            MessageLabel.setText("Message:")
            MessageLabel.setAlignment(Qt.AlignVCenter)
            DecryptMessageDailogLayout.addWidget(MessageLabel)

            # Message Text Edit
            MessageTextEdit = QTextEdit()
            MessageTextEdit.setReadOnly(True)
            MessageTextEdit.setText(message)
            DecryptMessageDailogLayout.addWidget(MessageTextEdit)

            # ******************* Button Box *********************
            EncryptedImageShow = QPushButton()
            EncryptedImageShow.setText('View Encrypted Image')
            EncryptedImageShow.setIcon(QIcon("Images/Decrypt.png"))
            EncryptedImageShow.setLayoutDirection(Qt.RightToLeft)
            EncryptedImageShow.setStyleSheet(
                """
                    background-color: black;
                    color: white;
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
            EncryptedImageShow.clicked.connect(lambda: Image.open(io.BytesIO(myresult[0][0])).show())
            DecryptMessageDailogLayout.addWidget(EncryptedImageShow)

            DecryptMessageDialogBox.exec_()
        else:
            QMessageBox.critical(self, "Error", "Invalid Key", QMessageBox.Ok)

    # Delete Inbox Messages
    def DeleteInboxMessages(self, MessagesTable):
        DeleteButton = self.sender()
        if DeleteButton:
            Message_id = MessagesTable.item(MessagesTable.indexAt(DeleteButton.pos()).row(), 0).text()

            DeleteMessageQuestion = QMessageBox.question(self, 'Delete Message',
                                                         'Are you sure you want to Delete this message?',
                                                         QMessageBox.Yes | QMessageBox.No)

            if DeleteMessageQuestion == QMessageBox.Yes:
                mycursor = mydb.cursor()
                mycursor.execute("Update messages set delete_reciever_flag = 1 where msg_id = %s", (Message_id,))
                mydb.commit()
                self.Inbox(MessagesTable)
            else:
                pass

    # Sent
    def Sent(self, MessagesTable):
        while MessagesTable.rowCount() > 0:
            MessagesTable.removeRow(0)

        MessagesTable.setColumnCount(5)
        MessagesTable.setWindowFlags(MessagesTable.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        MessagesTable.setHorizontalHeaderLabels(["Message ID", "Reciever", "Timestramp", "View", "Delete"])
        MessagesTable.horizontalHeader().setStyleSheet("::section {""background-color: black;  color: white;}")

        for i in range(MessagesTable.columnCount()):
            MessagesTable.horizontalHeaderItem(i).setFont(QFont("Ariel Black", 11))
            MessagesTable.horizontalHeaderItem(i).setFont(
                QFont(MessagesTable.horizontalHeaderItem(i).text(), weight=QFont.Bold))

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
            TimestrampItem = QTableWidgetItem()
            TimestrampItem.setData(Qt.EditRole, QVariant(row[2].strftime("%m/%d/%Y, %H:%M:%S")))
            MessagesTable.setItem(rowList.index(row), 2, TimestrampItem)
            MessagesTable.item(rowList.index(row), 2).setToolTip(row[2].strftime("%m/%d/%Y, %H:%M:%S"))
            MessagesTable.item(rowList.index(row), 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            MessagesTable.item(rowList.index(row), 2).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

            # View Button
            viewButton = QPushButton("view")
            viewButton.clicked.connect(lambda: self.ViewSentMessages(MessagesTable))
            MessagesTable.setCellWidget(rowList.index(row), 3, viewButton)

            # delete Button
            deleteButton = QPushButton("Delete")
            deleteButton.clicked.connect(lambda: self.DeleteSentMessages(MessagesTable))
            MessagesTable.setCellWidget(rowList.index(row), 4, deleteButton)

        MessagesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        MessagesTable.resizeColumnsToContents()
        MessagesTable.resizeRowsToContents()
        MessagesTable.setSortingEnabled(True)
        MessagesTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        for i in range(MessagesTable.columnCount()):
            MessagesTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    # View Send Messages
    def ViewSentMessages(self, MessagesTable):
        ViewButton = self.sender()
        if ViewButton:
            Message_id = MessagesTable.item(MessagesTable.indexAt(ViewButton.pos()).row(), 0).text()

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
            ViewDialogBox.setFixedWidth(self.width / 2)

            ViewDailogLayout = QVBoxLayout(ViewDialogBox)
            ViewDailogLayout.setContentsMargins(50, 50, 50, 50)

            # ****************** To ********************
            # To Label
            ToLabel = QLabel()
            ToLabel.setText("To:")
            ToLabel.setAlignment(Qt.AlignVCenter)
            ViewDailogLayout.addWidget(ToLabel)

            # To LineEdit
            ToLineEdit = QLineEdit()
            ToLineEdit.setAlignment(Qt.AlignVCenter)
            ToLineEdit.setText(rowList[0][0])
            ToLineEdit.setReadOnly(True)
            ToLineEdit.setValidator(QIntValidator(0, 10000, self))
            ViewDailogLayout.addWidget(ToLineEdit)

            # ****************** TimeStramp ********************
            # TimeStramp Label
            TimeStrampLabel = QLabel()
            TimeStrampLabel.setText("TimeStramp:")
            TimeStrampLabel.setAlignment(Qt.AlignVCenter)
            ViewDailogLayout.addWidget(TimeStrampLabel)

            # TimeStramp LineEdit
            TimeStrampLineEdit = QLineEdit()
            TimeStrampLineEdit.setAlignment(Qt.AlignVCenter)
            TimeStrampLineEdit.setText(rowList[0][1].strftime("%m/%d/%Y, %H:%M:%S"))
            TimeStrampLineEdit.setReadOnly(True)
            ViewDailogLayout.addWidget(TimeStrampLineEdit)

            # ****************** Key ********************
            # To Label
            KeyLabel = QLabel()
            KeyLabel.setText("Key:")
            KeyLabel.setAlignment(Qt.AlignVCenter)
            ViewDailogLayout.addWidget(KeyLabel)

            # Key LineEdit
            KeyLineEdit = QLineEdit()
            KeyLineEdit.setAlignment(Qt.AlignVCenter)
            KeyLineEdit.setText(rowList[0][2])
            KeyLineEdit.setReadOnly(True)
            ViewDailogLayout.addWidget(KeyLineEdit)

            # ****************** Message ********************
            # Message Label
            MessageLabel = QLabel()
            MessageLabel.setText("Message:")
            MessageLabel.setAlignment(Qt.AlignVCenter)
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
                    background-color: black;
                    color: white;
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


    mydb = mysql.connector.connect(
        host="sql12.freemysqlhosting.net",
        user="sql12348621",
        password="nvcWV8lYIj",
        database= "sql12348621"
    )

    Crypto = Window()
    Crypto.setStyleSheet(
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