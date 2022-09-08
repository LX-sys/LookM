# -*- coding:utf-8 -*-
# @time:2022/9/511:41
# @author:LX
# @file:table.py
# @software:PyCharm

import sys

from PyQt5.QtSql import QSqlRelationalTableModel,QSqlTableModel
from PyQt5.QtWidgets import QApplication, QTreeWidget,QTableView,QDirModel,QFileSystemModel
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import QStringListModel

class Table(QTableView):
    def __init__(self,*args,**kwargs):
        super(Table, self).__init__(*args,**kwargs)
        print(help(QSqlTableModel))
        self.__model = QSqlTableModel()
        self.setModel(self.__model)
        print(self.model())
        # self.__model.setColumnCount(3)
        self.init()

    def init(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Table()
    win.show()
    sys.exit(app.exec_())