import sqlite3
import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QPixmap, QRegExpValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QApplication, QTableWidgetItem, QPushButton, QMessageBox, \
    QTabWidget, QTextEdit, QFormLayout, QLineEdit, QCheckBox

from work_with_db import make_status_paid

NAME_DATABASE = "online_store_database.sqlite"


class Payment(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.cart_show = args[0]
        self.item_in_basket = args[1]
        self.id = args[2]
        self.main = args[3]
        self.status_paid = True
        self.initUI(args)

    def initUI(self, args):
        self.move(200, 200)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Payment')

        self.pixmap = QPixmap('pictures/2b2b2b.png')
        self.backend = QLabel(self)
        self.backend.setPixmap(self.pixmap)

        self.pixmap = QPixmap('pictures/separator.png')
        self.separator = QLabel(self)
        self.separator.setGeometry(0, 38, 800, 2)
        self.separator.setPixmap(self.pixmap)

        self.name_shop = QLabel("Angels Shop", self)
        self.name_shop.setGeometry(5, 5, 120, 30)
        self.name_shop.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.name_shop.setStyleSheet('QLabel {color: #1790ff;}')

        self.method_obtaining = QLabel("Способ получения", self)
        self.method_obtaining.setGeometry(10, 45, 200, 20)
        self.method_obtaining.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))
        self.method_obtaining.setStyleSheet('QLabel {color: #1790ff;}')

        self.tab = QTabWidget(self)
        self.tab.setGeometry(10, 70, 250, 150)
        self.tab.setStyleSheet("""QTabBar::tab {
                                        border: 2px solid #1790ff;
                                        border-bottom-color: #1790ff;
                                        color: #a9b1b4;
                                        min-width: 117px;
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
                                'border: 1px solid #3c3f41;'
                                'background-color: #3c3f41;}'
                                'QLabel {'
                                'color: #a9b1b4}')
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
                                'border: 1px solid #3c3f41;'
                                'background-color: #3c3f41;}'
                                'QLabel {'
                                'color: #a9b1b4}')
        self.paint_over_contours()

        self.payment_method = QLabel("Способ оплаты", self)
        self.payment_method.setGeometry(10, 230, 200, 20)
        self.payment_method.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))
        self.payment_method.setStyleSheet('QLabel {color: #1790ff;}')

        self.tab_payment = QTabWidget(self)
        self.tab_payment.setGeometry(10, 260, 250, 120)
        self.tab_payment.setStyleSheet("""QTabBar::tab {
                                                border: 2px solid #1790ff;
                                                border-bottom-color: #1790ff;
                                                color: #a9b1b4;
                                                min-width: 117px;
                                                min-height: 20px
                                            }
                                            QTabBar::tab:selected, QTabBar::tab:hover {
                                                background: #3c3f41;
                                            }""")
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab_payment.addTab(self.tab3, "Онлайн")
        layout3 = QFormLayout()
        self.input_card_number = QLineEdit(self)
        validator = QRegExpValidator(QRegExp("[1-9][0-9]{15}"))
        self.input_card_number.setValidator(validator)
        self.input_card_number.setPlaceholderText("Номер карты")
        layout3.addRow(self.input_card_number)
        layout5 = QFormLayout()
        self.month_input = QLineEdit(self)
        self.month_input.textChanged.connect(self.change_validator_month)
        validator = QRegExpValidator(QRegExp("[0-1][0-9]"))
        self.month_input.setValidator(validator)
        self.month_input.setPlaceholderText("Месяц")
        self.year_input = QLineEdit(self)
        self.year_input.textChanged.connect(self.change_validator_year)
        validator = QRegExpValidator(QRegExp("[0-9]{2}"))
        self.year_input.setValidator(validator)
        self.year_input.setPlaceholderText("Год")
        layout5.addRow(self.month_input, self.year_input)
        layout3.addRow(layout5)
        self.cvc_input = QLineEdit(self)
        validator = QRegExpValidator(QRegExp("[0-9]{3}"))
        self.cvc_input.textChanged.connect(self.change_validator_cvc)
        self.cvc_input.setValidator(validator)
        self.cvc_input.setPlaceholderText("CVC")
        layout3.addRow(self.cvc_input)
        self.tab3.setLayout(layout3)
        self.tab3.setStyleSheet('QWidget {'
                                'font: Times bold 16px;'
                                'border: 1px solid #3c3f41;'
                                'background-color: #3c3f41;}'
                                'QLabel {'
                                'color: #a9b1b4}'
                                'QLabel {'
                                'color: #a9b1b4}'
                                'QLineEdit {background-color: #3c3f41; color: #a9b1b4;'
                                ' border: 1px solid #1790ff;}'
                                )
        self.tab_payment.addTab(self.tab4, "При получении")
        layout4 = QFormLayout()
        layout4.addRow(QLabel("В магазине Angels", self))
        layout4.addRow(QLabel("можно оплатить наличными, ", self))
        layout4.addRow(QLabel("картой или в кредит.", self))
        self.tab4.setLayout(layout4)
        self.tab4.setStyleSheet('QWidget {'
                                'font: Times bold 16px;'
                                'border: 1px solid #3c3f41;'
                                'background-color: #3c3f41;}'
                                'QLabel {'
                                'color: #a9b1b4}')
        self.paint_over_contours_payment()

        self.cart = QLabel("Корзина", self)
        self.cart.setGeometry(280, 45, 200, 20)
        self.cart.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))
        self.cart.setStyleSheet('QLabel {color: #1790ff;}')

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(270, 70, 380, 310)
        self.tableWidget.setStyleSheet('QTableWidget {background-color: #3c3f41; color: #a9b1b4;}')
        self.tableWidget.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        con = sqlite3.connect(NAME_DATABASE)
        cur = con.cursor()
        if len(self.item_in_basket) == 1:
            for i in self.item_in_basket.keys():
                result = cur.execute(f"""SELECT * FROM price_list
                                                     WHERE title = '{i}'""").fetchall()
        else:
            result = cur.execute(f"""SELECT * FROM price_list
                                                 WHERE title in {tuple(self.item_in_basket.keys())}""").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setColumnWidth(0, 245)
        self.tableWidget.setColumnWidth(1, 69)
        self.tableWidget.setColumnWidth(2, 30)
        result = [i[1:] for i in result]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(i, j, item)
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(self.item_in_basket[elem[0]]) + "шт."))
        self.draw_above_table()

        self.cb = QCheckBox("Сохранить чек в txt файл", self)
        self.cb.setGeometry(10, 390, 250, 20)
        # self.cb.setStyleSheet('QCheckBox::indicator {background-color: #1790ff; color: #1790ff}')
        self.cb.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.status_bar = QLabel("", self)
        self.status_bar.setGeometry(10, 420, 380, 20)
        self.status_bar.setStyleSheet('QLabel {color: #1790ff;}')
        self.status_bar.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.btn_payment = QPushButton("Оплата", self)
        self.btn_payment.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_payment.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.btn_payment.setGeometry(270, 390, 350, 20)
        self.btn_payment.clicked.connect(self.payment)

        self.btn_payment = QPushButton("Вернуться в корзину", self)
        self.btn_payment.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_payment.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.btn_payment.setGeometry(270, 420, 350, 20)
        self.btn_payment.clicked.connect(self.back_to_cart)

    def change_validator_cvc(self):
        if len(self.sender().text()) == 2:
            if self.sender().text() == "00":
                validator = QRegExpValidator(QRegExp("[0-9]{2}[1-9]"))
                self.cvc_input.setValidator(validator)
        else:
            validator = QRegExpValidator(QRegExp("[0-9]{3}"))
            self.cvc_input.setValidator(validator)

    def change_validator_year(self):
        if len(self.sender().text()) == 1:
            if self.sender().text() == "0":
                validator = QRegExpValidator(QRegExp("[0-9][1-9]"))
                self.year_input.setValidator(validator)
        else:
            validator = QRegExpValidator(QRegExp("[0-9]{2}"))
            self.year_input.setValidator(validator)

    def change_validator_month(self):
        if len(self.sender().text()) == 1:
            if self.sender().text() == "0":
                validator = QRegExpValidator(QRegExp("[0-1][1-9]"))
                self.month_input.setValidator(validator)
            if self.sender().text() == "1":
                validator = QRegExpValidator(QRegExp("[0-1][0-2]"))
                self.month_input.setValidator(validator)
        else:
            validator = QRegExpValidator(QRegExp("[0-1][0-9]"))
            self.month_input.setValidator(validator)

    def paint_over_contours(self):
        self.pixmap = QPixmap('pictures/1790ff.png')
        self.backend_table_widget = QLabel(self)
        self.backend_table_widget.setGeometry(10, 93, 250, 2)
        self.backend_table_widget.setPixmap(self.pixmap)
        self.backend_table_widget2 = QLabel(self)
        self.backend_table_widget2.setGeometry(10, 93, 2, 127)
        self.backend_table_widget2.setPixmap(self.pixmap)
        self.backend_table_widget3 = QLabel(self)
        self.backend_table_widget3.setGeometry(250, 93, 2, 127)
        self.backend_table_widget3.setPixmap(self.pixmap)
        self.backend_table_widget4 = QLabel(self)
        self.backend_table_widget4.setGeometry(10, 216, 250, 4)
        self.backend_table_widget4.setPixmap(self.pixmap)
        self.pixmap = QPixmap('pictures/2b2b2b.png')
        self.backend_table_widget5 = QLabel(self)
        self.backend_table_widget5.setGeometry(252, 93, 10, 127)
        self.backend_table_widget5.setPixmap(self.pixmap)

    def paint_over_contours_payment(self):
        self.pixmap = QPixmap('pictures/1790ff.png')
        self.backend_table_widget = QLabel(self)
        self.backend_table_widget.setGeometry(10, 283, 250, 2)
        self.backend_table_widget.setPixmap(self.pixmap)
        self.backend_table_widget2 = QLabel(self)
        self.backend_table_widget2.setGeometry(10, 283, 2, 97)
        self.backend_table_widget2.setPixmap(self.pixmap)
        self.backend_table_widget3 = QLabel(self)
        self.backend_table_widget3.setGeometry(250, 283, 2, 97)
        self.backend_table_widget3.setPixmap(self.pixmap)
        self.backend_table_widget4 = QLabel(self)
        self.backend_table_widget4.setGeometry(10, 376, 250, 4)
        self.backend_table_widget4.setPixmap(self.pixmap)
        self.pixmap = QPixmap('pictures/2b2b2b.png')
        self.backend_table_widget5 = QLabel(self)
        self.backend_table_widget5.setGeometry(252, 283, 10, 97)
        self.backend_table_widget5.setPixmap(self.pixmap)

    def draw_above_table(self):
        self.pixmap = QPixmap('pictures/1790ff.png')
        self.backend_table_widget = QLabel(self)
        self.backend_table_widget.setGeometry(270, 70, 370, 1)
        self.backend_table_widget.setPixmap(self.pixmap)
        self.backend_table_widget2 = QLabel(self)
        self.backend_table_widget2.setGeometry(270, 70, 1, 310)
        self.backend_table_widget2.setPixmap(self.pixmap)
        self.backend_table_widget3 = QLabel(self)
        self.backend_table_widget3.setGeometry(270, 379, 370, 1)
        self.backend_table_widget3.setPixmap(self.pixmap)
        self.backend_table_widget4 = QLabel(self)
        self.backend_table_widget4.setGeometry(619, 70, 1, 310)
        self.backend_table_widget4.setPixmap(self.pixmap)
        self.pixmap = QPixmap('pictures/2b2b2b.png')
        self.backend_table_widget5 = QLabel(self)
        self.backend_table_widget5.setGeometry(620, 70, 40, 310)
        self.backend_table_widget5.setPixmap(self.pixmap)

    def payment(self):
        if self.status_paid:
            if self.correct_cart():
                make_status_paid(self.id, self.tab_payment.currentIndex())
                self.status_paid = False
                self.status_bar.setText("Оплата прошла")
                self.btn_payment.setText("Вернуться в каталог")
                self.btn_payment.clicked.connect(self.back_to_catalog)
            else:
                self.status_bar.setText("Введите данные карты")
        else:
            self.status_bar.setText("Заказ оплачен, вернитесь в каталог")

    def correct_cart(self):
        if self.tab_payment.currentIndex() == 0:
            if len(self.input_card_number.text()) == 16 and len(self.cvc_input.text()) == 3 and \
                    len(self.year_input.text()) == 2 and len(self.month_input.text()) == 2:
                return True
            else:
                return False
        else:
            return True

    def back_to_cart(self):
        self.hide()
        self.cart_show.show()

    def back_to_catalog(self):
        self.hide()
        self.main.show()
        self.main.update()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# app = QApplication(sys.argv)
# # app.setStyle('Fusion')
# ex = Payment()
# ex.show()
# sys.excepthook = except_hook
# sys.exit(app.exec())
