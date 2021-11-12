import sqlite3
import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QApplication, QTableWidgetItem, QPushButton, QMessageBox, \
    QAbstractItemView, QLineEdit

from payment import Payment

from work_with_db import save_db

NAME_DATABASE = "online_store_database.sqlite"
BACKGROUND_PICTURE = 'pictures/2b2b2b.png'
SEPARATOR_PICTURES = 'pictures/separator.png'


class InvalidValue(Exception):
    pass


class Cart(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.q_label_style = 'QLabel {color: #1790ff;}'
        self.q_line_edit_style = 'QLineEdit {background-color: #1790ff; color: #e5eaf1; border: 1px solid #1790ff;}'
        self.q_push_button_style = 'QPushButton {background-color: #1790ff; color: #e5eaf1;}'
        self.q_table_widget_style = 'QTableWidget {background-color: #3c3f41; color: #a9b1b4;}'
        self.q_message_box_style = 'QMessageBox {font: Times bold 16px; border: 1px solid #2b2b2b;' \
                                   ' border-radius: 1px; background-color: #2b2b2b;}' \
                                   ' QMessageBox QLabel {color: #1790ff} ' \
                                   'QPushButton {background-color: #1790ff; color: #e5eaf1;}'
        self.item_in_basket = args[1]
        self.main = args[0]
        self.current_id = args[2]
        self.table_create = False
        self.initUI(args)

    def initUI(self, args):
        self.move(200, 200)
        self.setFixedSize(690, 280)
        self.setWindowTitle('Cart')

        self.pixmap = QPixmap(BACKGROUND_PICTURE)
        self.backend = QLabel(self)
        self.backend.setPixmap(self.pixmap)

        self.pixmap = QPixmap(SEPARATOR_PICTURES)
        self.separator = QLabel(self)
        self.separator.setGeometry(0, 38, 800, 2)
        self.separator.setPixmap(self.pixmap)

        self.name_shop = QLabel("Корзина", self)
        self.name_shop.setGeometry(29, 5, 120, 30)
        self.name_shop.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.name_shop.setStyleSheet(self.q_label_style)
        self.name_shop.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))

        self.status_bar = QLabel("", self)
        self.status_bar.setGeometry(5, 550, 250, 20)
        self.status_bar.setStyleSheet(self.q_label_style)
        self.status_bar.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))

        self.btn_back = QPushButton("Вернуться в католог для выбора товара", self)
        self.btn_back.setStyleSheet(self.q_push_button_style)
        self.btn_back.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_back.setGeometry(410, 120, 250, 20)
        self.btn_back.clicked.connect(self.back_to_catalog)

        self.btn_main_back = QPushButton("Вернуться в католог для выбора товара", self)
        self.btn_main_back.setStyleSheet(self.q_push_button_style)
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
        self.btn_delete.setStyleSheet(self.q_push_button_style)
        self.btn_delete.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_delete.setGeometry(410, 64, 250, 20)
        self.btn_delete.clicked.connect(self.delete_from_cart)

        self.status_delete = QLabel("", self)
        self.status_delete.setGeometry(410, 89, 250, 20)
        self.status_delete.setStyleSheet(self.q_label_style)
        self.status_delete.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))

        self.calculation = QLabel("", self)
        self.calculation.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.calculation.setGeometry(410, 89, 250, 20)
        self.calculation.setStyleSheet(self.q_label_style)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(5, 40, 400, 200)
        self.tableWidget.setStyleSheet(self.q_table_widget_style)
        self.tableWidget.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.itemChanged.connect(self.change_finished)
        self.fill_in_the_table()

        self.payment = QPushButton("Оформить заказ", self)
        self.payment.setStyleSheet(self.q_push_button_style)
        self.payment.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.payment.setGeometry(410, 150, 250, 20)
        self.payment.clicked.connect(self.open_payment)

    def fill_in_the_table(self):
        if len(self.item_in_basket) == 0:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.paint_over_contours(0)
            self.status_delete.setText("В корзине пока ничего нет")
        else:
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
            self.paint_over_contours(len(result))
            self.change_cost()
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
            self.messagebox.setStyleSheet(self.q_message_box_style)
            self.messagebox.setWindowTitle("Подтверждение удаления из корзины")
            self.messagebox.setText("Вы уверены, что хотите удалить " + ", ".join(items) + " из корзины?")
            self.btn_yes = self.messagebox.addButton("Да", QMessageBox.YesRole)
            self.btn_yes.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            self.btn_no = self.messagebox.addButton("Нет", QMessageBox.NoRole)
            self.btn_no.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            self.messagebox.show()
            if self.messagebox.exec_() == 0:
                for elem in items:
                    del self.item_in_basket[elem]
                self.fill_in_the_table()
                self.change_cost()
                self.move_cost()
                self.status_delete.setText("Предметы успешно удалены")
        else:
            if len(self.item_in_basket) != 0:
                self.status_delete.setText("Выберите товары")
                self.move_cost()

    def change_cost(self):
        self.calculation.setText(f"Итого: {str(self.finding_count())} шт. на {str(self.finding_cost())}р.")

    def finding_cost(self):
        con = sqlite3.connect(NAME_DATABASE)
        cur = con.cursor()
        if len(self.item_in_basket) == 1:
            for i in self.item_in_basket.keys():
                result = cur.execute(f"""SELECT price FROM price_list
                                             WHERE title == '{i}'""").fetchall()
        else:
            result = cur.execute(f"""SELECT price FROM price_list
                                             WHERE title in {tuple(self.item_in_basket.keys())}""").fetchall()
        data = [i[:-3] for i in self.get_data()]
        amount = 0
        result = [i[0][:-2] for i in result]
        for index, elem in enumerate(result):
            amount += int(elem) * int(data[index])
        return amount

    def finding_count(self):
        return sum([int(i[:-3]) for i in self.get_data()])

    def get_data(self):
        data = []
        for i in range(self.tableWidget.rowCount()):
            data.append(self.tableWidget.item(i, 2).text())
        return data

    def paint_over_contours(self, *args):
        self.table_create = True
        self.pixmap = QPixmap(BACKGROUND_PICTURE)
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
        self.fill_in_the_table()
        if self.status_delete.text() != "В корзине пока ничего нет":
            save_db(self.item_in_basket, self.current_id)
            self.Payment = Payment(self, self.item_in_basket, self.current_id, self.main)
            self.Payment.show()
            self.hide()

    def change_finished(self):
        if self.table_create and self.tableWidget.currentColumn() == 2:
            try:
                text = self.tableWidget.currentItem().text()
                text = "".join(text.split())
                if len(text) == 0:
                    raise InvalidValue('Неверный формат количества товаров')
                elif len(text) == 1:
                    if not (len(text) == 1 and text[0] != '0' and text[0].isdigit()):
                        raise InvalidValue('Неверный формат количества товаров')
                elif len(text) == 4:
                    if text[-3:] != 'шт.':
                        raise InvalidValue('Неверный формат количества товаров')
                    elif text[0] == '0':
                        raise InvalidValue('Неверный формат количества товаров')
                    for i in text[:-3]:
                        if not i.isdigit():
                            raise InvalidValue('Неверный формат количества товаров')
                    if len(text[:-3]) != 1:
                        raise InvalidValue('Данный товар доступен не более 9 штук')
                else:
                    if text[0].isdigit() and text[1].isdigit():
                        raise InvalidValue('Данный товар доступен не более 9 штук')
                    else:
                        raise InvalidValue('Неверный формат количества товаров')
                if self.item_in_basket[self.tableWidget.item(self.tableWidget.currentRow(), 0).text()] == text[0]:
                    raise InvalidValue('Введите новое число')
                self.item_in_basket[self.tableWidget.item(self.tableWidget.currentRow(), 0).text()] = text[0]
                self.tableWidget.currentItem().setText(text[0] + 'шт.')
                self.change_cost()
                self.finding_cost()
                self.move_cost()
                self.status_delete.setText("Успешно изменено количество товара")
            except InvalidValue as iv:
                self.tableWidget.currentItem().setText(
                    str(self.item_in_basket[self.tableWidget.item(self.tableWidget.currentRow(), 0).text()]) + 'шт.')
                self.status_delete.setText(str(iv))
                self.move_cost()

    def closeEvent(self, event):
        self.messagebox_close = QtWidgets.QMessageBox(self)
        self.messagebox_close.setIcon(QMessageBox.NoIcon)
        self.messagebox_close.setStyleSheet(self.q_message_box_style)
        self.messagebox_close.setWindowTitle("Подтверждение выхода")
        self.messagebox_close.setText("Вы уверены, что хотите выйти из приложения?")
        self.btn_yes = self.messagebox_close.addButton("Да", QMessageBox.YesRole)
        self.btn_yes.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_no = self.messagebox_close.addButton("Нет", QMessageBox.NoRole)
        self.btn_no.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        if self.messagebox_close.exec_() == 0:
            save_db(self.item_in_basket, self.current_id)
            event.accept()
        else:
            event.ignore()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

# app = QApplication(sys.argv)
# # app.setStyle('Fusion')
# ex = Cart()
# ex.show()
# sys.excepthook = except_hook
# sys.exit(app.exec())
