# -*- coding:utf-8 -*-
# @time:2022/8/1317:44
# @author:LX
# @file:tab.py
# @software:PyCharm
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt,pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import (QApplication, QTabWidget, QWidget, QMainWindow, QWidget, QPushButton, QGridLayout)

from GuiLib.tabbar.tabBar import TabBar

class Tab(TabBar):
    # 关闭tab发送信号
    removeed = pyqtSignal(str)
    def __init__(self,*args,**kwargs) -> None:
        super(Tab, self).__init__(*args,**kwargs)

        self.__tab = dict()
        # 设置tab可关闭
        self.setTabsClosable(True)


        self.Init()
        # self.myEvent()
        self.addTab(QWidget(), "tab1")
        # self.addTab(QWidget(), "tab2")
        # print(self.getShowTab())
        # self.focusTab("tab2")

    # 获取tab
    def getTab(self,name)->QWidget:
        return self.__tab[name][name]

    def addTab(self, widget: QWidget, name: str,pos:int=None) -> None:
        self.__tab[name] = {name:widget,"state":True}
        new_win = QWidget()
        # gridLayout = QGridLayout(new_win)
        # gridLayout.setContentsMargins(0, 0, 0, 0)
        # gridLayout.setSpacing(0)
        # gridLayout.addWidget(widget, 0, 0, 1, 1)
        if pos is None:
            super(Tab, self).addTab(new_win, name)
        else:
            super(Tab, self).addTab(new_win, name,pos)


        print(self.__tab)

    def Init(self):
        pass

    # 聚焦tab
    def focusTab(self,name):
        for i in range(self.count()):
            if self.tabText(i) == name:
                self.setCurrentIndex(i)
                break

    def is_tab(self,name)->bool:
        if name in self.__tab:
            return True
        return False


    # 关闭tab是隐藏
    def closeTab_Event(self,index):
        text = self.tabText(index)
        self.removeTab(index)
        # 隐藏
        self.setTabState(text,False)
        self.removeed.emit(text)

    # 真实删除
    def delete(self,name):
        for i in range(self.count()):
            if self.tabText(i) == name:
                self.removeTab(i)
                del self.__tab[name]
                break
        print(self.__tab)

    # 修改tab状态()
    def setTabState(self,name,state):
        print(self.__tab)
        self.__tab[name]["state"] = state

        # 状态为真,则还原状态
        if state:
            pos = 0
            # 获取当前tab位置
            for i in range(self.count()):
                if self.tabText(i) == name:
                    pos = i
                    break
            win = self.getTab(name)
            self.delete(name)
            self.addTab(win,name,pos)

    # 获取当前显示的tab
    def getShowTab(self)->list:
        show_tab = []
        for tab in self.__tab:
            if self.__tab[tab]["state"]:
                show_tab.append(tab)
        return show_tab

    # 获取隐藏的tab
    def getHideTab(self)->list:
        hide_tab = []
        for tab in self.__tab:
            if self.__tab[tab]["state"] == False:
                hide_tab.append(tab)
        return hide_tab

    def eee(self,i):
        name = self.tabText(i)
        print("-->",name)

    def myEvent(self):
        super(Tab, self).myEvent()
        self.tabCloseRequested.connect(self.closeTab_Event)
        self.tabBarClicked.connect(self.eee)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Tab()
    w.show()
    sys.exit(app.exec_())