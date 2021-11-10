import sqlite3
import sys
from cart import Cart

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QLineEdit, QTableView, QCheckBox, QPushButton, QTableWidget, \
    QTableWidgetItem, QHeaderView, QInputDialog, QMessageBox

from work_with_db import save_db, get_result_from_db

NAME_DATABASE = "online_store_database.sqlite"


class MainWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.current_id = args[1]
        self.sorting = True
        self.item_in_basket = get_result_from_db(self.current_id)
        self.initUI(args)

    def initUI(self, args):
        self.move(200, 200)
        self.setFixedSize(500, 600)
        self.setWindowTitle('Angels Shop')

        self.pixmap = QPixmap('pictures/2b2b2b.png')
        self.backend = QLabel(self)
        self.backend.setPixmap(self.pixmap)

        self.pixmap = QPixmap('pictures/separator.png')
        self.separator = QLabel(self)
        self.separator.setGeometry(0, 38, 500, 2)
        self.separator.setPixmap(self.pixmap)

        self.name_shop = QLabel("Angels Shop", self)
        self.name_shop.setGeometry(5, 5, 120, 30)
        self.name_shop.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.name_shop.setStyleSheet('QLabel {color: #1790ff;}')

        self.input_request = QLineEdit(self)
        self.input_request.setGeometry(130, 10, 290, 20)
        self.input_request.setPlaceholderText("Название")
        self.input_request.setStyleSheet('QLineEdit {background-color: #1790ff; color: #e5eaf1;'
                                         ' border: 1px solid #1790ff;}')
        self.input_request.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.input_request.textChanged.connect(self.fill_in_the_table)

        self.btn_basket = QPushButton("Корзина", self)
        self.btn_basket.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_basket.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_basket.setGeometry(430, 10, 60, 20)
        self.btn_basket.clicked.connect(self.open_cart)

        self.status_bar = QLabel("", self)
        self.status_bar.setGeometry(29, 550, 250, 20)
        self.status_bar.setStyleSheet('QLabel {color: #1790ff;}')
        self.status_bar.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(5, 40, 490, 500)
        self.tableWidget.setStyleSheet('QTableWidget {background-color: #3c3f41; color: #a9b1b4;}')
        self.tableWidget.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.fill_in_the_table()

        self.btn_find = QPushButton("Добавить в корзину в корзину", self)
        self.btn_find.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_find.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_find.setGeometry(280, 550, 190, 20)
        self.btn_find.clicked.connect(self.add_to_card)

        self.sorting = QLabel("Сортировка:", self)
        self.sorting.setGeometry(230, 42, 100, 18)
        self.sorting.setStyleSheet('QLabel {color: #1790ff;}')
        self.sorting.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))

        self.btn_sorting = QPushButton("Сначала дорогие", self)
        self.btn_sorting.setGeometry(320, 42, 152, 18)
        self.btn_sorting.setStyleSheet('QPushButton {background-color: #1790ff; color: #e5eaf1;}')
        self.btn_sorting.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.btn_sorting.clicked.connect(self.table_sorting)

    def update(self):
        self.item_in_basket = get_result_from_db(self.current_id)
        self.fill_in_the_table()

    def fill_in_the_table(self):
        con = sqlite3.connect(NAME_DATABASE)
        cur = con.cursor()
        if self.input_request.text() == "":
            result = cur.execute(f"""SELECT * FROM price_list""").fetchall()
        else:
            result = cur.execute(f"""SELECT * FROM price_list
                                     WHERE title like '%{self.input_request.text()}%'""").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.status_bar.setText('Ничего не нашлось')
            return
        else:
            self.status_bar.setText('')
        self.tableWidget.setColumnCount(len(result[0]) - 1)
        self.tableWidget.setColumnWidth(0, 375)
        self.tableWidget.setColumnWidth(1, 69)
        self.result = [i[1:] for i in result]
        if self.sorting:
            self.result = sorted(self.result, key=lambda x: int(x[1][:-2]), reverse=True)
        else:
            self.result = sorted(self.result, key=lambda x: int(x[1][:-2]), reverse=False)
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.paint_over_contours()
        con.close()

    def add_to_card(self):
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
                    'color: #e5eaf1;}')
            self.messagebox.setWindowTitle("Подтверждение добавления")
            self.messagebox.setText("Вы уверены, что хотите добавить " + ", ".join(items) + " в корзину?")
            self.btn_yes = self.messagebox.addButton("Да", QMessageBox.YesRole)
            self.btn_yes.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            self.btn_no = self.messagebox.addButton("Нет", QMessageBox.NoRole)
            self.btn_no.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            self.messagebox.show()
            if self.messagebox.exec_() == 0:
                flag = True
                for i in items:
                    if i in self.item_in_basket:
                        flag = False
                if flag:
                    for i in items:
                        self.item_in_basket[i] = 1
                else:
                    self.status_bar.setText("Выбранный товар уже в корзине")
                if flag:
                    if len(items) > 1:
                        self.status_bar.setText('Предметы успешно добавлены в корзину')
                    else:
                        self.status_bar.setText('Предмет успешно добавлен в корзину')
            else:
                self.status_bar.setText('')
        else:
            self.status_bar.setText('Выберите товары')

    def open_cart(self):
        self.Cart = Cart(self, self.item_in_basket, self.current_id)
        self.Cart.show()
        self.hide()

    def paint_over_contours(self):
        self.pixmap = QPixmap('pictures/2b2b2b.png')
        self.backend_table_widget = QLabel(self)
        self.backend_table_widget.setGeometry(5, 40, 490, 24)
        self.backend_table_widget.setPixmap(self.pixmap)
        if len(self.result) < 9:
            self.tableWidget.move(12, 40)
        else:
            self.tableWidget.move(5, 40)
        self.backend_table_widget2 = QLabel(self)
        self.backend_table_widget2.setGeometry(5, 40, 24, 500)
        self.backend_table_widget2.setPixmap(self.pixmap)
        self.backend_table_widget2 = QLabel(self)
        self.backend_table_widget2.setGeometry(471, 40, 24, 500)
        self.backend_table_widget2.setPixmap(self.pixmap)
        self.backend_table_widget3 = QLabel(self)
        self.backend_table_widget3.setGeometry(5, 539, 490, 2)
        self.backend_table_widget3.setPixmap(self.pixmap)

    def table_sorting(self):
        if self.btn_sorting.text() == "Сначала дорогие":
            self.btn_sorting.setText("Сначала недорогие")
            self.sorting = False
        else:
            self.btn_sorting.setText("Сначала дорогие")
            self.sorting = True
        self.fill_in_the_table()

    def closeEvent(self, event):
        self.messagebox_close = QtWidgets.QMessageBox(self)
        self.messagebox_close.setIcon(QMessageBox.NoIcon)
        self.messagebox_close.setStyleSheet(
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
# ex = MainWindow()
# ex.show()
# sys.excepthook = except_hook
# sys.exit(app.exec())