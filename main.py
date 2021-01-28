import sys
import sqlite3

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication  # for QT app itself
from PyQt5 import uic  # first time using the thing


con = sqlite3.connect('coffee.sqlite')
c = con.cursor()


# c.execute('''CREATE TABLE coffee([id] INTEGER PRIMARY KEY, [title] text, [frying_degree] text,
# [ground_or_beans] text, [taste_desc] text, [price] text, [package_volume] integer)''')


class GitCoffeeInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        for elem in c.execute('''SELECT * FROM coffee''').fetchall():
            self.coffee_listWidget.addItem(QtWidgets.QListWidgetItem(" ||| ".join(map(str, elem))))


app = QApplication(sys.argv)
ex = GitCoffeeInfo()
ex.show()
sys.exit(app.exec_())
