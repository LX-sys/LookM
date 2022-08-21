# -*- coding:utf-8 -*-
# @time:2022/8/2015:25
# @author:LX
# @file:IpTree.py
# @software:PyCharm
import copy
import re
import sys,os
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt, pyqtSignal, QSize, QModelIndex
from PyQt5.QtGui import QMouseEvent, QCursor,QIcon,QColor
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QMenu, QInputDialog,
                             QListWidgetItem, QMessageBox, QTreeWidgetItem)

from Database.open_mysql import Machine
from core.ssh_reset_machine import reset_machine,off_machine,on_machine,state_machine,is_ssl_machine
from core.mchine import MachineDispose

# 路径
RootPath = os.path.abspath(os.path.dirname(__file__))
icon_Path = os.path.join(RootPath, "icon")


# 元组模拟dict的get
def getTuple(data,index):
    try:
        return data[index]
    except:
        return None


class IpTree(QTreeWidget):
    RED = (255,0,0)
    BLUE = (85, 255, 255)

    # 发送 ip和 范围
    ipScope = pyqtSignal(tuple)

    def __init__(self,*args,**kwargs):
        super(IpTree,self).__init__(*args,**kwargs)

        self.__node = dict()
        #  处理机器的类
        self.__mchine = MachineDispose()

        self.setHeaderLabels(["IP","范围"])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.myEvent()
        self.Init()

    # 默认图标
    def get_default_icon(self)->QIcon:
        icon = QIcon()
        icon.addFile(os.path.join(icon_Path, "folder.png"), QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(os.path.join(icon_Path, "folder_open.png"), QSize(), QIcon.Normal, QIcon.On)
        icon.addFile(os.path.join(icon_Path, "folder_av.png"), QSize(), QIcon.Selected, QIcon.Off)
        icon.addFile(os.path.join(icon_Path, "folder_av_open.png"), QSize(), QIcon.Selected, QIcon.On)
        return icon

    # 构建树
    def structData(self)->dict:
        machine_data = self.__mchine.get_machine_addr_all(sort=False)
        tree = dict()
        for data in machine_data:
            ip = data[0]
            spcre = data[1]
            is_delete = data[2]
            s, e = spcre.split("-")
            s, e = int(s), int(e)+1
            if is_delete == 1:
                tree[(ip, spcre,IpTree.RED)] = [str(i) for i in range(s, e)]
            else:
                tree[(ip, spcre)] = [str(i) for i in range(s, e)]
        return tree

    def Init(self):
        # 这里不能直接传QColor(255,0,0),但是可以传元组
        # print(self.structData())
        # self.createTree({("198.204.247.82", "1-40",IpTree.BLUE): ["450", "123"]})
        self.createTree(self.structData())

    def createTree(self, data: dict,p_Item: QTreeWidgetItem = None):
        for info, v_list in data.items():
            if p_Item is None:
                item = QTreeWidgetItem(self)
                item.setIcon(0, self.get_default_icon())
                if isinstance(info,tuple):
                    item.setText(0, info[0])
                    item.setText(1, info[1])
                    if getTuple(info,2):
                        r,g,b = getTuple(info,2)
                        item.setBackground(0, QColor(r,g,b))
                if isinstance(info, str):
                    item.setText(0, info)
            else:
                item = p_Item
                item = QTreeWidgetItem(item)
                item.setIcon(0, self.get_default_icon())
                item.setText(0, info)
            self.addTopLevelItem(item)
            for v in v_list:
                if isinstance(v, str):
                    item_c = QTreeWidgetItem(item)
                    item_c.setText(0, v)
                    if getTuple(info,2):
                        r, g, b = getTuple(info, 2)
                        item_c.setBackground(0, QColor(r,g,b))
                    self.addTopLevelItem(item_c)
                else:
                    self.createTree(v, item)

    def ip_spcre_Event(self,index:QModelIndex):
        number = index.data()
        if number and number.isdigit():
            ip = self.currentItem().parent().text(0)
            machine_number = self.currentItem().parent().childCount() # 机器总数
            if __name__ == '__main__':
                print(ip,number)
            # 发送 ip和 范围
            self.ipScope.emit((ip,number,machine_number))
        else:
            print(number)
            print(index.data())


    def myEvent(self):
        self.doubleClicked.connect(self.ip_spcre_Event)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = IpTree()
    tree.show()

    sys.exit(app.exec_())