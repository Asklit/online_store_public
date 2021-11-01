import sqlite3
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QApplication, QTableWidgetItem, QPushButton, QMessageBox

from payment import Payment

NAME_DATABASE = "price_list.sqlite"


class Cart(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.item_in_basket = args[1]
        self.main = args[0]
        self.table_create = False
        self.initUI(args)

    def initUI(self, args):
        self.move(200, 200)
        self.setFixedSize(690, 280)
        self.setWindowTitle('Cart')

        self.pixmap = QPixmap('2b2b2b.png')
        self.backend = QLabel(self)
        self.backend.setPixmap(self.pixmap)

        self.pixmap = QPixmap('separator.png')
        self.separator = QLabel(self)
        self.separator.setGeometry(0, 38, 800, 2)
        self.separator.setPixmap(self.pixmap)

        self.name_shop = QLabel("Корзина", self)
        self.name_shop.setGeometry(29, 5, 120, 30)
        self.name_shop.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.name_shop.setStyleSheet('QLabel {color: #1790ff;}')
        self.name_shop.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))

        self.status_bar = QLabel("", self)
        self.status_bar.setGeometry(5, 550, 250, 20)
        self.status_bar.setStyleSheet('QLabel {color: #1790ff;}')
        self.status_bar.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))

        self.btn_back = QPushButton("Вернуться в католог для выбора товара", self)
        self.btn_back.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_back.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_back.setGeometry(410, 120, 250, 20)
        self.btn_back.clicked.connect(self.back_to_catalog)

        self.btn_main_back = QPushButton("Вернуться в католог для выбора товара", self)
        self.btn_main_back.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_main_back.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_main_back.setGeometry(29, 75, 250, 20)
        self.btn_main_back.hide()
        self.btn_main_back.clicked.connect(self.back_to_catalog)

        self.bar = QLabel("В корзине пока что ничего нет", self)
        self.bar.setGeometry(29, 45, 250, 20)
        self.bar.setStyleSheet('QLabel {color: #1790ff;}')
        self.bar.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.bar.hide()

        self.btn_delete = QPushButton("Удалить выбранные товары из корзины", self)
        self.btn_delete.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_delete.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_delete.setGeometry(410, 64, 250, 20)
        self.btn_delete.clicked.connect(self.delete_from_cart)

        self.status_delete = QLabel("", self)
        self.status_delete.setGeometry(410, 89, 250, 20)
        self.status_delete.setStyleSheet('QLabel {color: #1790ff;}')
        self.status_delete.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))

        self.calculation = QLabel("", self)
        self.change_cost()
        self.calculation.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.calculation.setGeometry(410, 89, 250, 20)
        self.calculation.setStyleSheet('QLabel {color: #1790ff;}')

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(5, 40, 400, 200)
        self.tableWidget.setStyleSheet('QTableWidget {background-color: #3c3f41; color: #a9b1b4;}')
        self.tableWidget.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.fill_in_the_table()

        self.payment = QPushButton("Оформить заказ", self)
        self.payment.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.payment.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.payment.setGeometry(410, 150, 250, 20)
        self.payment.clicked.connect(self.open_payment)

    def fill_in_the_table(self):
        if len(self.item_in_basket) == 0:
            self.tableWidget.hide()
            if self.table_create:
                self.backend_table_widget.hide()
                self.backend_table_widget2.hide()
                self.backend_table_widget3.hide()
                self.backend_table_widget4.hide()
            self.bar.show()
            self.btn_main_back.show()
            self.setFixedSize(300, 120)
        else:
            con = sqlite3.connect(NAME_DATABASE)
            cur = con.cursor()
            if len(self.item_in_basket) == 1:
                result = cur.execute(f"""SELECT * FROM price_list
                                         WHERE title = '{self.item_in_basket[0]}'""").fetchall()
            else:
                result = cur.execute(f"""SELECT * FROM price_list
                                     WHERE title in {tuple(self.item_in_basket)}""").fetchall()
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]) - 1)
            self.tableWidget.setColumnWidth(0, 285)
            self.tableWidget.setColumnWidth(1, 69)
            result = [i[1:] for i in result]
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.paint_over_contours(len(result))
            con.close()

    def back_to_catalog(self):
        self.hide()
        self.main.show()

    def delete_from_cart(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        items = [self.tableWidget.item(i, 0).text() for i in rows]
        if items:
            self.messagebox = QtWidgets.QMessageBox(self)
            self.messagebox.setIcon(QMessageBox.NoIcon)
            self.messagebox.setStyleSheet(
                'QMessageBox {'
                'font: Times bold 16px;'
                'border: 1px solid #2b2b2b;'
                'border-radius: 1px;'
                'background-color: #2b2b2b;}'
                'QMessageBox QLabel {'
                'color: #1790ff}'
                'QPushButton {'
                'background-color: #1790ff;'
                ' color: #e5eaf1;}')
            self.messagebox.setWindowTitle("Подтверждение удаления из корзины")
            self.messagebox.setText("Вы уверены, что хотите удалить " + ", ".join(items) + " из корзины?")
            self.btn_yes = self.messagebox.addButton("Да", QMessageBox.YesRole)
            self.btn_yes.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            self.btn_no = self.messagebox.addButton("Нет", QMessageBox.NoRole)
            self.btn_no.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            self.messagebox.show()
            if self.messagebox.exec_() == 0:
                for elem in items:
                    del self.item_in_basket[self.item_in_basket.index(elem)]
                self.fill_in_the_table()
                self.change_cost()
                self.status_delete.setText("Предметы успешно удалены")
                self.move_cost()
        else:
            if len(self.item_in_basket) != 0:
                self.status_delete.setText("Выберите товары")
                self.move_cost()

    def change_cost(self):
        if len(self.item_in_basket) == 1:
            self.calculation.setText(f"Итого: {len(self.item_in_basket)} товар на {self.finding_cost()}р.")
        else:
            self.calculation.setText(f"Итого: {len(self.item_in_basket)} товара на {self.finding_cost()}р.")

    def finding_cost(self):
        con = sqlite3.connect(NAME_DATABASE)
        cur = con.cursor()
        if len(self.item_in_basket) == 1:
            result = cur.execute(f"""SELECT price FROM price_list
                                             WHERE title = '{self.item_in_basket[0]}'""").fetchall()
        else:
            result = cur.execute(f"""SELECT price FROM price_list
                                             WHERE title in {tuple(self.item_in_basket)}""").fetchall()
        amount = 0
        result = [i[0][:-2] for i in result]
        for elem in result:
            amount += int(elem)
        return amount

    def paint_over_contours(self, *args):
        self.table_create = True
        self.pixmap = QPixmap('2b2b2b.png')
        self.backend_table_widget = QLabel(self)
        self.backend_table_widget.setGeometry(5, 40, 400, 24)
        self.backend_table_widget.setPixmap(self.pixmap)

        self.backend_table_widget2 = QLabel(self)
        if args[0] <= 9:
            self.tableWidget.setGeometry(12, 40, 393, 200)
        self.backend_table_widget2.setGeometry(5, 40, 24, 200)
        self.backend_table_widget2.setPixmap(self.pixmap)

        self.backend_table_widget3 = QLabel(self)
        self.backend_table_widget3.setGeometry(381, 40, 24, 200)
        self.backend_table_widget3.setPixmap(self.pixmap)

        self.backend_table_widget4 = QLabel(self)
        self.backend_table_widget4.setGeometry(5, 239, 400, 2)
        self.backend_table_widget4.setPixmap(self.pixmap)

    def move_cost(self):
        self.calculation.move(410, 114)
        self.btn_back.move(410, 145)
        self.payment.move(410, 170)

    def open_payment(self):
        self.Payment = Payment(self, self.item_in_basket)
        self.Payment.show()
        self.hide()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# app = QApplication(sys.argv)
# # app.setStyle('Fusion')
# ex = Cart()
# ex.show()
# sys.excepthook = except_hook
# sys.exit(app.exec())
