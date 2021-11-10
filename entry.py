import sys
import sqlite3

from PyQt5 import QtGui

from main import MainWindow

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QWidget


class NumberError(Exception):
    pass


class PasswordError(Exception):
    pass


NAME_DATABASE = "online_store_database.sqlite"


class EntryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.number = 0

    def initUI(self):
        self.move(200, 200)
        self.setFixedSize(400, 360)
        self.setWindowTitle('Angels Shop Entry')

        self.pixmap = QPixmap('pictures/2b2b2b.png')
        self.backend = QLabel(self)
        self.backend.resize(400, 400)
        self.backend.setPixmap(self.pixmap)

        self.pixmap = QPixmap('pictures/logo_blue.png')
        self.image = QLabel(self)
        self.image.move(20, 5)
        self.image.resize(360, 204)
        self.image.setPixmap(self.pixmap)

        self.email_input = QLineEdit("", self)
        self.email_input.setPlaceholderText("Телефон")
        self.email_input.setStyleSheet('QLineEdit {background-color: #1790ff; color: #e5eaf1;'
                                       ' border: 1px solid #1790ff;}')
        self.email_input.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.email_input.setGeometry(50, 195, 300, 20)

        self.password_input = QLineEdit("", self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setStyleSheet('QLineEdit {background-color: #1790ff; color: #e5eaf1;'
                                          ' border: 1px solid #1790ff;}')
        self.password_input.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.password_input.setGeometry(50, 220, 300, 20)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.btn_auth = QPushButton("Авторизация", self)
        self.btn_auth.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_auth.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_auth.setGeometry(50, 270, 300, 20)
        self.btn_auth.clicked.connect(self.authorization)

        self.btn_reg = QPushButton("Регистрация", self)
        self.btn_reg.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_reg.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_reg.setGeometry(50, 295, 300, 20)
        self.btn_reg.clicked.connect(self.registration)

        self.number_error = QLabel("", self)
        self.number_error.setStyleSheet('QLabel {color: #1790ff;}')
        self.number_error.resize(300, 20)

        self.password_error = QLabel("", self)
        self.password_error.setStyleSheet('QLabel {color: #1790ff;}')
        self.password_error.resize(300, 20)

    def authorization(self):
        if self.email_input.text() == "":
            self.move_number("Введите номер телефона")
        elif self.password_input.text() == "":
            self.move_password("Введите пароль")
        elif self.correct_data() and self.correct_data_in_database():
            self.MainWindow = MainWindow(self, self.curent_id)
            self.MainWindow.show()
            self.hide()

    def registration(self):
        if self.email_input.text() == "":
            self.move_number("Введите номер телефона")
        elif self.password_input.text() == "":
            self.move_password("Введите пароль")
        elif len(self.password_input.text()) > 20:
            self.move_password("Ваш пароль слишком длинный")
        elif self.correct_data():
            con = sqlite3.connect(NAME_DATABASE)
            cur = con.cursor()
            number = self.number
            password = self.password_input.text()
            data = cur.execute(f"""SELECT title FROM information
                                    WHERE title = '{number}'""").fetchall()
            if len(data) == 0:
                con = sqlite3.connect(NAME_DATABASE)
                cur = con.cursor()
                cur.execute(f"""INSERT INTO information(title, password)
                                         VALUES('{number}', '{password}')""").fetchall()
                con.commit()
                self.move_password("Пользователь успешно зарегистрирован")
            else:
                self.move_number("Пользователь с даннным номером уже зарегистрирован")

    def correct_data(self):
        try:
            number = self.email_input.text()
            if number[0] == "8":
                number = "+7" + number[1:]
            elif number[:2] != "+7":
                raise NumberError("Необходимо указать коректный номер телефона")
            number = "".join(number.split())
            if number.count("(") > 1 or number.count(")") > 1 \
                    or number.find("(") > number.find(")") \
                    or ")" in number and "(" not in number:
                raise NumberError("Необходимо указать коректный номер телефона")
            elif number[0] == "-" or number[-1] == "-" or "--" in number:
                raise NumberError("Необходимо указать коректный номер телефона")
            else:
                number_res = "+"
                for i in number[1:]:
                    if i.isdigit():
                        number_res += i
                    elif i.isalpha():
                        raise NumberError("Необходимо указать коректный номер телефона")
                if len(number_res) != 12:
                    raise NumberError("Неверное количество цифр")
                else:
                    self.number = number_res
                    return True

        except NumberError as ne:
            self.move_number(ne)
            return False
        except PasswordError as pe:
            self.move_password(pe)
            return False

    def correct_data_in_database(self):
        try:
            number = self.number
            password = self.password_input.text()
            con = sqlite3.connect(NAME_DATABASE)
            cur = con.cursor()
            correct_number = cur.execute(f"""SELECT title FROM information
                                            WHERE title = '{number}'""").fetchall()
            if len(correct_number) == 0:
                raise NumberError("Указанный номер еще не зарегистрирован")
            correct_password = cur.execute(f"""SELECT password FROM information
                                            WHERE title = '{number}' and password = '{password}'""").fetchall()
            if len(correct_password) == 0:
                raise PasswordError("Введите корректный пароль")
            else:
                self.curent_id = cur.execute(f"""SELECT id FROM information
                                            WHERE title = '{number}'""").fetchall()[0][0]
                return True
        except NumberError as ne:
            self.move_number(ne)
            return False
        except PasswordError as pe:
            self.move_password(pe)
            return False

    def move_password(self, text):
        self.number_error.setText("")
        self.number_error.move(0, 0)
        self.password_input.move(50, 220)
        self.password_error.setText(str(text))
        self.password_error.move(50, 245)

    def move_number(self, text):
        self.password_error.setText("")
        self.password_error.move(0, 0)
        self.number_error.setText(str(text))
        self.number_error.move(50, 220)
        self.password_input.move(50, 245)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
# app.setStyle('Fusion')
ex = EntryWindow()
ex.show()
sys.excepthook = except_hook
sys.exit(app.exec())