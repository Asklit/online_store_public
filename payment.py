import sqlite3
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QApplication, QTableWidgetItem, QPushButton, QMessageBox, \
    QTabWidget, QTextEdit, QFormLayout, QLineEdit

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

        self.tab = QTabWidget(self)
        self.tab.setGeometry(10, 70, 400, 190)
        self.tab.setStyleSheet("""QTabBar::tab {
                                        border: 2px solid #1790ff;
                                        border-bottom-color: #1790ff;
                                        color: #1790ff;
                                        min-width: 192px;
                                        min-height: 20px
                                    }
                                    QTabBar::tab:selected, QTabBar::tab:hover {
                                        background: #3c3f41;
                                    }""")
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.tab.addTab(self.tab1, "It-куб")
        layout = QFormLayout()
        layout.addRow(QLabel("Дополнительное образование,", self))
        layout.addRow(QLabel("It-куб,", self))
        layout.addRow(QLabel("ул. Чернышевского, 28, Пермь (эт. 3),", self))
        layout.addRow(QLabel("пн-пт 09:00–18:00,", self))
        layout.addRow(QLabel("перерыв 12:00–13:00", self))
        self.tab1.setLayout(layout)
        self.tab1.setStyleSheet('QWidget {'
                                'font: Times bold 16px;'
                                'border: 1px solid #2b2b2b;'
                                'background-color: #2b2b2b;}'
                                'QLabel {'
                                'color: #1790ff}')
        self.tab.addTab(self.tab2, "Муравейник")
        layout2 = QFormLayout()
        layout2.addRow(QLabel("Клуб для детей и подростков,", self))
        layout2.addRow(QLabel("Пермский краевой центр Муравейник,", self))
        layout2.addRow(QLabel("ул. Пушкина, 76, Пермь,", self))
        layout2.addRow(QLabel("ежедневно, 09:00–20:00,", self))
        layout2.addRow(QLabel("перерыв 12:00–12:48", self))
        self.tab2.setLayout(layout2)
        self.tab2.setStyleSheet('QWidget {'
                                'font: Times bold 16px;'
                                'border: 1px solid #2b2b2b;'
                                'background-color: #2b2b2b;}'
                                'QLabel {'
                                'color: #1790ff}')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
# app.setStyle('Fusion')
ex = Payment()
ex.show()
sys.excepthook = except_hook
sys.exit(app.exec())
