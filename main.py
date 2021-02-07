import sys
import sqlite3

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication  # for QT app itself
from PyQt5 import uic  # first time using the thing


con = sqlite3.connect('coffee.sqlite')
c = con.cursor()


# c.execute('''CREATE TABLE coffee([id] INTEGER PRIMARY KEY, [title] text, [frying_degree] text,
# [ground_or_beans] text, [taste_desc] text, [price] text, [package_volume] integer)''')


class NoneWithClose:
    def close(self):
        pass

# aa = QtWidgets.QLineEdit

class EditAddWindow(QMainWindow):
    def __init__(self, mode, func_end, elem=0):
        super().__init__()

        uic.loadUi('addEditCoffeeForm.ui', self)

        if elem == 0:
            self.id = None
        else:
            self.id = elem[0].elem[0]

        if mode == 'edit':
            self.lineEdit_taste.setText(elem[0].elem[4])
            self.lineEdit_name.setText(elem[0].elem[1])
            self.lineEdit_degree.setText(elem[0].elem[2])
            self.lineEdit_price.setText(elem[0].elem[5])
            self.lineEdit_volume.setText(str(elem[0].elem[6]))
            self.lineEdit_ground_or_whatever.setText(elem[0].elem[3])

            self.lineEdit_taste.bonded_text = elem[0].elem[4]
            self.lineEdit_name.bonded_text = elem[0].elem[1]
            self.lineEdit_degree.bonded_text = elem[0].elem[2]
            self.lineEdit_price.bonded_text = elem[0].elem[5]
            self.lineEdit_volume.bonded_text = elem[0].elem[6]
            self.lineEdit_ground_or_whatever.bonded_text = elem[0].elem[3]
        else:
            self.lineEdit_taste.bonded_text = ''
            self.lineEdit_name.bonded_text = ''
            self.lineEdit_degree.bonded_text = ''
            self.lineEdit_price.bonded_text = ''
            self.lineEdit_volume.bonded_text = ''
            self.lineEdit_ground_or_whatever.bonded_text = ''

        self.lineEdit_taste.textEdited.connect(self.change_text)
        self.lineEdit_name.textEdited.connect(self.change_text)
        self.lineEdit_degree.textEdited.connect(self.change_text)
        self.lineEdit_price.textEdited.connect(self.change_text)
        self.lineEdit_volume.textEdited.connect(self.change_text)
        self.lineEdit_ground_or_whatever.textEdited.connect(self.change_text)

        self.pushButton_apply.clicked.connect(func_end)

    def change_text(self):
        self.sender().bonded_text = self.sender().text()


class GitCoffeeInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.pushButton_edit.clicked.connect(self.edit_open)
        self.pushButton_add.clicked.connect(self.add_open)

        # self.tableWidget_coffee = QtWidgets.QTableWidget(self)

        self.edit_window = NoneWithClose()
        self.add_window = NoneWithClose()

        self.update_table()

    def edit_open(self):
        self.edit_window.close()
        if len(self.tableWidget_coffee.selectedItems()) == 0:
            return
        self.edit_window = EditAddWindow('edit', self.edit_entry, elem=self.tableWidget_coffee.selectedItems())
        self.edit_window.show()

    def add_open(self):
        self.add_window.close()
        self.add_window = EditAddWindow('add', self.add_entry)
        self.add_window.show()

    def edit_entry(self):
        idd = self.edit_window.id
        taste = self.edit_window.lineEdit_taste.bonded_text
        name = self.edit_window.lineEdit_name.bonded_text
        degree = self.edit_window.lineEdit_degree.bonded_text
        price = self.edit_window.lineEdit_price.bonded_text
        volume = self.edit_window.lineEdit_volume.bonded_text
        ground_or_whatever = self.edit_window.lineEdit_ground_or_whatever.bonded_text
        self.edit_window.close()
        if not self.check(taste, name, degree, price, volume, ground_or_whatever):
            return
        c.execute('''UPDATE coffee
        SET
        title = ?, frying_degree = ?,
        ground_or_beans = ?, taste_desc = ?,
        price = ?, package_volume = ?
        WHERE id = ?''', (name, degree,
                          ground_or_whatever, taste, price,
                          int(volume), idd))
        self.update_table()

    def add_entry(self):
        taste = self.add_window.lineEdit_taste.bonded_text
        name = self.add_window.lineEdit_name.bonded_text
        degree = self.add_window.lineEdit_degree.bonded_text
        price = self.add_window.lineEdit_price.bonded_text
        volume = self.add_window.lineEdit_volume.bonded_text
        ground_or_whatever = self.add_window.lineEdit_ground_or_whatever.bonded_text
        self.add_window.close()
        if not self.check(taste, name, degree, price, volume, ground_or_whatever):
            return
        c.execute('''INSERT INTO 
        coffee(title, frying_degree, ground_or_beans, taste_desc, price, package_volume)
        VALUES(?, ?, ?, ?, ?, ?)''', (name, degree, ground_or_whatever, taste, price, int(volume)))
        con.commit()
        self.update_table()

    def check(self, taste, name, degree, price, volume, ground_or_whatever):
        if len(taste) == 0 or \
           len(name) == 0 or \
           len(degree) == 0 or \
           len(price) == 0 or \
           len(ground_or_whatever) == 0:
            return False
        return True

    def update_table(self):
        self.tableWidget_coffee.clear()
        self.res = c.execute('''SELECT * FROM coffee''').fetchall()
        self.tableWidget_coffee.setRowCount(len(self.res))
        self.tableWidget_coffee.setColumnCount(len(self.res[0]))
        for i, elem in enumerate(self.res):
            itm = QtWidgets.QTableWidgetItem(str(elem[0]))
            itm.elem = elem
            self.tableWidget_coffee.setItem(i, 0, itm)
            itm = QtWidgets.QTableWidgetItem(str(elem[1]))
            itm.elem = elem
            self.tableWidget_coffee.setItem(i, 1, itm)
            itm = QtWidgets.QTableWidgetItem(str(elem[2]))
            itm.elem = elem
            self.tableWidget_coffee.setItem(i, 2, itm)
            itm = QtWidgets.QTableWidgetItem(str(elem[3]))
            itm.elem = elem
            self.tableWidget_coffee.setItem(i, 3, itm)
            itm = QtWidgets.QTableWidgetItem(str(elem[4]))
            itm.elem = elem
            self.tableWidget_coffee.setItem(i, 4, itm)
            itm = QtWidgets.QTableWidgetItem(str(elem[5]))
            itm.elem = elem
            self.tableWidget_coffee.setItem(i, 5, itm)
            itm = QtWidgets.QTableWidgetItem(str(elem[6]))
            itm.elem = elem
            self.tableWidget_coffee.setItem(i, 6, itm)


app = QApplication(sys.argv)
ex = GitCoffeeInfo()
ex.show()
sys.exit(app.exec_())
