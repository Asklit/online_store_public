import sqlite3
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QApplication, QTableWidgetItem, QPushButton, QMessageBox

NAME_DATABASE = "price_list.sqlite"


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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# app = QApplication(sys.argv)
# # app.setStyle('Fusion')
# ex = Payment()
# ex.show()
# sys.excepthook = except_hook
# sys.exit(app.exec())
