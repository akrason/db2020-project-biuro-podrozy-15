from PyQt5.QtWidgets import *
import src.app.modules.login as login


class Start(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def interfejs(self):
        self.setWindowTitle("Biuro podróży - start")

        zalogujBtn = QPushButton("&Logowanie", self)
        zarejestrujBtn = QPushButton("&Rejestracja", self)

        uklad1 = QGridLayout()
        uklad1.addWidget(zalogujBtn, 0, 0)
        uklad1.addWidget(zarejestrujBtn, 1, 0)
        self.setLayout(uklad1)
        self.resize(300, 100)
        self.show()

        zalogujBtn.clicked.connect(self.logowanie)
        #zalogujBtn.clicked.connect(self.logowanie)
        #zarejestrujBtn.clicked.connect(self.rejestracja)

    def logowanie(self):
        print("asfafd")
        dialog = login.Login(self)
        QGridLayout()
        dialog.show()

    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Wyjście',
            "Czy na pewno chcesz zakończyć?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

