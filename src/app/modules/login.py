from PyQt5.QtWidgets import *


class Login(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def interfejs(self):
        self.setWindowTitle("Biuro podróży - logowanie")

        etykieta1 = QLabel("Imię:", self)
        etykieta2 = QLabel("Nazwisko:", self)
        etykieta3 = QLabel("Hasło:", self)

        imie = QLineEdit()
        nazwisko = QLineEdit()
        haslo = QLineEdit()
        haslo.setEchoMode(QLineEdit.Password)

        okBtn = QPushButton("Zaloguj", self)

        uklad2 = QGridLayout()
        uklad2.addWidget(etykieta1, 0, 0)
        uklad2.addWidget(etykieta2, 0, 1)
        uklad2.addWidget(etykieta3, 0, 2)
        uklad2.addWidget(imie, 1, 0)
        uklad2.addWidget(nazwisko, 1, 1)
        uklad2.addWidget(haslo, 1, 2)
        uklad2.addWidget(okBtn, 2, 1)

        #zalogujBtn = QPushButton("&Logowanie", self)

        #ukladH = QGridLayout()
        #ukladH.addWidget(zalogujBtn, 0, 0)
        self.setLayout(uklad2)
        self.resize(300, 100)
        self.show()


        #zalogujBtn.clicked.connect(self.logowanie)
        #zarejestrujBtn.clicked.connect(self.rejestracja)

    def logowanie(self):
        print("asfafd")




