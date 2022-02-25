import sys
sys.path.insert(0,"C:/Users/3400g/Documents/MILES/CLASS")
sys.path.insert(0,"C:/Users/3400g/Documents/MILES/Images")
from email_receiver import Email_Receiving
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from email.header import decode_header
import time

class MilesWindow(QMainWindow):
    def __init__(self):
        super(MilesWindow, self).__init__()
        self.email = Email_Receiving()
        self.n_mails = 0
        self.inbox = []
        self.logged = False

        self.setWindowIcon(QtGui.QIcon('Images/icon.png'))
        self.setObjectName("Machine Learning")
        self.resize(490, 417)
        self.cur_screen = "home"

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(40, 60, 411, 241))
        self.listWidget.setObjectName("listWidget")

        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(0, 30, 481, 301))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("Images/Bright Minimal Business Logo.png"))
        self.logo.setObjectName("logo")

        self.b_custom = QtWidgets.QPushButton(self.centralwidget)
        self.b_custom.setGeometry(QtCore.QRect(340, 330, 141, 51))
        self.b_custom.setFont(font)
        self.b_custom.setFlat(False)
        self.b_custom.setObjectName("b_custom")
        self.b_custom.clicked.connect(lambda: self.switchScreen("custom"))

        self.b_login = QtWidgets.QPushButton(self.centralwidget)
        self.b_login.setGeometry(QtCore.QRect(190, 330, 141, 51))
        self.b_login.setFont(font)
        self.b_login.setObjectName("b_login")
        self.b_login.clicked.connect(lambda: self.switchScreen("miles1"))

        self.b_about = QtWidgets.QPushButton(self.centralwidget)
        self.b_about.setGeometry(QtCore.QRect(10, 330, 171, 51))
        self.b_about.setFont(font)
        self.b_about.setObjectName("b_about")
        self.b_about.clicked.connect(lambda: self.switchScreen("about"))

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 10, 411, 23))
        self.progressBar.setObjectName("progressBar")

        self.b_automate = QtWidgets.QPushButton(self.centralwidget)
        self.b_automate.setGeometry(QtCore.QRect(40, 310, 201, 51))
        self.b_automate.setFont(font)
        self.b_automate.setFlat(False)
        self.b_automate.setObjectName("b_automate")
        self.b_automate.clicked.connect(lambda: self.switchScreen("miles2"))

        self.b_flush = QtWidgets.QPushButton(self.centralwidget)
        self.b_flush.setGeometry(QtCore.QRect(260, 310, 191, 51))
        self.b_flush.setFont(font)
        self.b_flush.setObjectName("b_flush")
        self.b_flush.clicked.connect(self.flushInbox)

        self.b_returnhome = QtWidgets.QPushButton(self.centralwidget)
        self.b_returnhome.setGeometry(QtCore.QRect(160, 370, 171, 31))
        self.b_returnhome.setFont(font)
        self.b_returnhome.setObjectName("b_returnhome")
        self.b_returnhome.clicked.connect(self.returnScreen)
       

        self.l_header = QtWidgets.QLabel(self.centralwidget)
        self.l_header.setGeometry(QtCore.QRect(130, 0, 241, 51))
        
        hfont = QtGui.QFont()
        hfont.setFamily("Unispace")
        hfont.setPointSize(12)
        hfont.setBold(True)
        hfont.setWeight(75)
        self.l_header.setFont(hfont)
        self.l_header.setAlignment(QtCore.Qt.AlignCenter)
        self.l_header.setObjectName("l_header")
        self.l_subheader = QtWidgets.QLabel(self.centralwidget)
        self.l_subheader.setGeometry(QtCore.QRect(120, 40, 241, 20))

        sfont = QtGui.QFont()
        sfont.setFamily("Unispace")
        sfont.setPointSize(8)
        sfont.setBold(True)
        sfont.setWeight(75)
        self.l_subheader.setFont(font)
        self.l_subheader.setAlignment(QtCore.Qt.AlignCenter)
        self.l_subheader.setObjectName("l_subheader")

        self.b_process = QtWidgets.QPushButton(self.centralwidget)
        self.b_process.setGeometry(QtCore.QRect(200, 310, 201, 51))
        self.b_process.setFont(font)
        self.b_process.setFlat(False)
        self.b_process.setObjectName("b_process")
        self.b_process.clicked.connect(self.processMail)

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(100, 320, 81, 31))
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        
        self.setCentralWidget(self.centralwidget)
        self._translate = QtCore.QCoreApplication.translate
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.initHomeScreen()

    def initHomeScreen(self):
        self.hideAll()
        self.switchScreen("home")

    def processMail(self):
        self.n_mails = self.email.getNumberMails()
        if self.n_mails == 0:
            self.l_subheader.setText(self._translate("MainWindow", "Inbox is empty"))
            self.checkBox.setChecked(False)
        if self.checkBox.isChecked() is True:
            if self.n_mails > 0:
                self.checkBox.setText(self._translate("MainWindow", "Automating.."))
                self.l_subheader.setText(self._translate("MainWindow", "PROCESSING EMAIL"))
                self.email.processMail(self.listWidget, self.progressBar, self.l_header)
                self.n_mails = self.email.getNumberMails()
            print("Automate is checked processing next mail")
            self.l_subheader.setText(self._translate("MainWindow", "PROCESSING ANOTHER MAIL IN 6.."))
            for x in range(3):
                print("PAUSING: {} seconds".format(x))
                self.l_subheader.setText(self._translate("MainWindow", "PROCESSING ANOTHER MAIL IN {}..".format(x)))
                time.sleep(1)
            self.processMail()
        elif self.checkBox.isChecked() is False:
            if self.n_mails > 0:
                self.checkBox.setText(self._translate("MainWindow", "Automate"))
                self.l_subheader.setText(self._translate("MainWindow", "PROCESSING EMAIL"))
                self.email.processMail(self.listWidget, self.progressBar, self.l_header)
                self.l_subheader.setText(self._translate("MainWindow", "SUCCESSFUL"))

    def switchScreen(self, destination):
        if destination == "home":
            self.cur_screen = "home"
            self.inbox = []
            self.listWidget.clear()
            print("Current Screen: ", self.cur_screen)
            if self.logged is True:
                self.email.logout()
                self.logged = False
                print("Successfully Logged out")
            self.showThis("home")
            
        elif destination == "custom":
            self.cur_screen = "quit"
            print("Current Screen: ", self.cur_screen)
            self.close()
            print("Closed the program")

        elif destination == "miles1":
            self.cur_screen = "miles1"
            
            print("Current Screen: ", self.cur_screen)
            self.progressBar.show()
            for x in range(0, 40):
                self.progressBar.setProperty("value", x)

            self.l_subheader.setText(self._translate("MainWindow", "Check your internet connection."))
            self.l_subheader.show()
            
            self.email.init()
            self.email.login("miles.verify@gmail.com", "milesMILES123!@#")
            self.logged = True
            print("Sucessfully Logged In")

            for x in range(41, 80):
                self.progressBar.setProperty("value", x)

            self.inbox = []
            self.n_mails = self.email.getNumberMails()
            if self.n_mails > 0:
                self.inbox = self.email.extractInbox(self.n_mails)
                for mail in self.inbox:
                    self.listWidget.addItem(mail)
            print("Number of Mails:{}".format(self.n_mails))

            self.l_subheader.setText(self._translate("MainWindow", "Emails in inbox: {0}".format(str(self.n_mails))))
            self.l_header.setText(self._translate("MainWindow", "SUCCESSFULLY LOGGED IN"))
            
            for x in range(81, 100):
                self.progressBar.setProperty("value", x)
            self.progressBar.hide()

            self.showThis("miles1")

        elif destination == "miles1.5":
            self.cur_screen = "miles1"
            print("Current Screen: ", self.cur_screen)

            self.inbox = []
            self.listWidget.clear()
            self.n_mails = self.email.getNumberMails()
            if self.n_mails > 0:
                self.inbox = self.email.extractInbox(self.n_mails)
                for mail in self.inbox:
                    self.listWidget.addItem(mail)
            print("Number of Mails:{}".format(self.n_mails))

            self.l_header.setText(self._translate("MainWindow", "UPDATED INBOX"))
            self.l_subheader.setText(self._translate("MainWindow", "Emails in inbox: {0}".format(str(self.n_mails))))
            self.showThis("miles1")

        elif destination == "miles2":
            self.cur_screen = "miles2"
            self.l_header.setText(self._translate("MainWindow", "PROCESS EMAILS"))
            self.showThis("miles2")
            
        elif destination == "about":
            self.cur_screen = "about"
            print("Current Screen: ", self.cur_screen)
            self.l_header.setText(self._translate("MainWindow", "DEVELOPED BY"))
            self.l_subheader.setText(self._translate("MainWindow", "Gatab, Hombre, Salik"))
            self.showThis("about")
            

    def hideAll(self):
        self.progressBar.hide()
        self.b_about.hide()
        self.b_custom.hide()
        self.b_login.hide()
        self.b_automate.hide()
        self.b_flush.hide()
        self.b_returnhome.hide()
        self.l_header.hide()
        self.l_subheader.hide()
        self.listWidget.hide()
        self.b_returnhome.hide()
        self.logo.hide()
        self.b_process.hide()
        self.checkBox.hide()

    def showThis(self, this):
        self.hideAll()
        if this == "home":
            self.b_about.show()
            self.b_custom.show()
            self.b_login.show()
            self.logo.show()
        elif this == "miles1":
            self.b_automate.show()
            self.b_flush.show()
            self.b_returnhome.show()
            self.l_header.show()
            self.l_subheader.show()
            self.listWidget.show()
        elif this == "miles2":
            self.b_process.show()
            self.checkBox.show()
            self.b_returnhome.show()
            self.l_header.show()
            self.l_subheader.show()
            self.listWidget.show()
        elif this == "about":
            self.l_header.show()
            self.l_subheader.show()
            self.b_returnhome.show()

    def returnScreen(self):
        if self.cur_screen == "miles1":
            print("Returning From: ", self.cur_screen, " to home")
            self.switchScreen("home")
        elif self.cur_screen == "miles2":
            print("Returning From: ", self.cur_screen, " to miles Screen 1")
            self.switchScreen("miles1.5")
        elif self.cur_screen == "about":
            print("Returning From: ", self.cur_screen, " to home")
            self.switchScreen("home")

    def flushInbox(self):
        if self.n_mails > 0:
            self.email.deleteMail()
            self.l_header.setText(self._translate("MainWindow", "DELETED INBOX"))

        self.n_mails = 0
        self.inbox = []

        self.l_subheader.setText(self._translate("MainWindow", "Emails in inbox: {0}".format(str(self.n_mails))))
        
        self.listWidget.clear()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(self._translate("MainWindow", "MACHINE LEARNING: Miles (Logistic Regression)"))
        self.b_custom.setText(self._translate("MainWindow", "Quit"))
        self.b_login.setText(self._translate("MainWindow", "Login"))
        self.b_about.setText(self._translate("MainWindow", "About"))

        self.b_automate.setText(self._translate("MainWindow", "Process"))
        self.b_flush.setText(self._translate("MainWindow", "Fush Inbox"))
        self.b_returnhome.setText(self._translate("MainWindow", "BACK"))
        self.b_process.setText(self._translate("MainWindow", "Process Mail"))
        self.checkBox.setText(self._translate("MainWindow", "Automate"))
        
# def prediction(body):
#     miles_P = Url_processing()
#     dangerous_mails = []
#     for urls in body:
#         print("CURRENT URL: ", urls)
#         status = miles_P.prediction(str(urls))
        
#         if status == 0:
#             dangerous_mails.append(urls)
#             print("This url is suspicious")
#         else:
#             print("This url looks safe")

#     return dangerous_mails



if __name__ == "__main__":
    import sys
    print("Opened the program")
    app = QApplication(sys.argv)
    win = MilesWindow()
    win.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     miles_R = Email_receiving()
#     address, body = miles_R.checkNewmail()
#     statement = ''
#     condition = 0

#     print("MAIN: Processing links")
#     print("DEBUG: List extracted", body)

#     print("MAIN: Predicting links")
#     # list_dangerous_mails = prediction(body)

#     # if len(list_dangerous_mails) > 0:
#     #     with open('C:/Users/3400g/Documents/MILES/MESSAGES/unsafe.txt') as f:
#     #         statement = f.readlines()
#     #         f.close
#     #     statement += list_dangerous_mails
#     #     condition = 0
#     #     print("DEBUG: Predicted dangerous links in mails", list_dangerous_mails)
#     # elif len(list_dangerous_mails) == 0:
#     #     with open('C:/Users/3400g/Documents/MILES/MESSAGES/safe.txt') as f:
#     #         statement = f.readlines()
#     #         f.close
#     #     condition = 1
#     #     print("DEBUG: There are no dangerous links in the mail")

#     # miles_S = Email_sending()
#     # miles_S.sendEmail(condition, address, str(statement))
#     # print(condition, str(address), str(statement))
#     print("MAIN: Program exited")
