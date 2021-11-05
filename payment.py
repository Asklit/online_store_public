import sqlite3
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QApplication, QTableWidgetItem, QPushButton, QMessageBox, \
    QTabWidget, QTextEdit

NAME_DATABASE = "online_store_database.sqlite"


class Payment(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        # self.main = args[0]
        self.move(200, 200)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Payment')

        self.pixmap = QPixmap('2b2b2b.png')
        self.backend = QLabel(self)
        self.backend.setPixmap(self.pixmap)

        self.pixmap = QPixmap('separator.png')
        self.separator = QLabel(self)
        self.separator.setGeometry(0, 38, 800, 2)
        self.separator.setPixmap(self.pixmap)

        self.name_shop = QLabel("Angels Shop", self)
        self.name_shop.setGeometry(5, 5, 120, 30)
        self.name_shop.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.name_shop.setStyleSheet('QLabel {color: #1790ff;}')

        self.method_obtaining = QLabel("Способ получения", self)
        self.method_obtaining.setGeometry(10, 45, 490, 20)
        self.method_obtaining.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.method_obtaining.setStyleSheet('QLabel {color: #1790ff;}')

        self.store_address = QTextEdit("", self)
        self.store_address.append("Клуб для детей и подростков,")
        self.store_address.append("Пермский краевой центр Муравейник,")
        self.store_address.append("ул. Пушкина, 76, Пермь,")
        self.store_address.append("ежедневно, 09:00–20:00,")
        self.store_address.append("перерыв 12:00–12:48")
        self.store_address.setGeometry(10, 70, 270, 90)
        self.store_address.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.store_address.setStyleSheet('QTextEdit {'
                                         'background-color: #3c3f41;'
                                         'color: #a9b1b4;'
                                         'border: 1px solid #3c3f41;}')
        self.store_address.setReadOnly(True)

        self.payment_method = QLabel("Способ оплаты", self)
        self.payment_method.setGeometry(10, 165, 160, 20)
        self.payment_method.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.payment_method.setStyleSheet('QLabel {color: #1790ff;}')

        self.tab = QTabWidget(self)
        self.tab.setGeometry(10, 190, 400, 200)
        self.tab.tabBar().setStyleSheet('background-color: #3c3f41;')
        # self.tab.setStyleSheet('background-color: #3c3f41;')
        self.tab.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.tab.addTab(QLabel("В магазине можно оплатить наличными, картой или в кредит", self), "При получении")
        self.tab.addTab(QLabel("Банковской картой", self), "Онлайн")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
# app.setStyle('Fusion')
ex = Payment()
ex.show()
sys.excepthook = except_hook
sys.exit(app.exec())
