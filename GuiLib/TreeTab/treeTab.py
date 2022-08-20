# -*- coding:utf-8 -*-
# @time:2022/8/2014:46
# @author:LX
# @file:treeTab.py
# @software:PyCharm
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSplitter
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEnginePage,QWebEngineSettings
from GuiLib.Tree.IpTree import IpTree
from GuiLib.tabbar.tabBar import TabBar


def url(ip):
    return "https://{}/ui/".format(ip)

# 返回具体机器的访问url
def machineIDUrl(ip,id):
    return  "https://{}/ui/#/host/vms/{}".format(ip,id)

class TreeTab(QWidget):
    def __init__(self,*args,**kwargs) -> None:
        super(TreeTab, self).__init__(*args,**kwargs)

        # 网格布局,水平分裂器
        self.gbox = QGridLayout(self)
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)
        self.gbox.addWidget(self.splitter)

        # 树,tab,webview
        self.tree = IpTree(self.splitter)
        self.tab= TabBar(self.splitter)

        self.myEvent()
        self.Init()

    def Init(self) -> None:
        # 调整布局
        tree_w = int(self.width() * 0.25)
        self.splitter.setSizes([tree_w, self.width() - tree_w])

        # self.tree.createTree({("69.30.245.162", "1-20", True): ["450", "123"]})


    def addTab(self,text:str,url:str) -> None:
        # print(name)
        self.tab.addTab(text=text,url=url)

    def ip_Event(self,ip_scope) -> None:
        ip = ip_scope[0]
        number = int(ip_scope[1])
        machine_number = int(ip_scope[2])  # 机器数量
        # 获取真实的机器访问id
        real_id = number % machine_number
        if real_id >1:
            real_id += 1
        # self.addTab(text=str(number),url=machineIDUrl(ip,real_id))
        print(url(ip))
        self.addTab(text=str(number),url=url(ip))
        # print("url:",machineIDUrl(ip,real_id))

    def myEvent(self):
        self.tree.ipScope.connect(self.ip_Event)
        # self.tree.filenameedit.connect(self.addTab)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeTab = TreeTab()
    treeTab.show()

    sys.exit(app.exec_())