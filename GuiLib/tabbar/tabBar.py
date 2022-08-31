# -*- coding:utf-8 -*-
# @time:2022/7/209:47
# @author:LX
# @file:tabBar.py
# @software:PyCharm
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt, pyqtSignal, QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWidgets import (QApplication, QTabBar, QWidget,QTabWidget,QGridLayout,QFrame,
                             QDockWidget,QMainWindow)

from GuiLib.WebView.webView import WebView
'''
可移动TabBar
'''

class MyQDockWidget(QDockWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.dockWidgetContents = QFrame()
        self.setWidget(self.dockWidgetContents)

        self.lock = True
        self.setContentsMargins(0,0,0,0)
        # self.defaultStyleSheet()
        # 禁止关闭
        self.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        # self.setTitleBarWidget(QWidget())

    def setText(self,text:str):
        self.setWindowTitle(text)

    def defaultStyleSheet(self):
        self.setStyleSheet('''
                background-color: rgb(0, 255, 127);
                ''')

    def getWidget(self) -> QWidget:
        return self.dockWidgetContents

class MyTabBar(QTabBar):
    draged = pyqtSignal(bool) # 拖拽

    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        self.old_pos:QPoint

        self.setMovable(True)

        self.setAcceptDrops(True)

    # 判断鼠标当前位置是否在当前窗口区域
    def isMouseArea(self,apos:QPoint,pos:QPoint)->bool:
        x,y = apos.x(),apos.y()
        win_x,win_in_x = pos.x(),pos.x()+self.width()
        win_y,win_in_y = pos.y(),pos.y()+self.height()+30
        if x>= win_x and x <= win_in_x and \
            y>= win_y and y<=win_in_y:
            return True
        return False

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        super(MyTabBar, self).mousePressEvent(e)

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        if not self.isMouseArea(e.globalPos(),self.parent().pos()):
            print("脱出")
            self.draged.emit(True)
        else:
            self.draged.emit(False)
        super(MyTabBar, self).mouseReleaseEvent(e)


class TabBar(QTabWidget):
    # tab双击信号
    tabDoubleed = pyqtSignal(str)
    # 重新加载窗口
    reloadMachineed = pyqtSignal(dict)


    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)


        self.setStyleSheet('''
QTabWidget::pane{
background-color: rgb(152, 152, 226);
}
QTabWidget::pane{
background-color: rgb(152, 152, 226);
}
QTabBar::tab{
	background-color: rgb(58, 58, 173);
	height:28;
}
QTabBar::tab:hover,QTabBar::tab:selected{
	background-color: rgb(85, 85, 255);
}
        ''')
        # self.tab_list = []
        self.tab = MyTabBar()
        self.setTabBar(self.tab)
        self.setTabsClosable(True)

        '''
        {"web":"机器tab对象","state":True}
        '''
        self.__machine = dict()

        win = QMainWindow()
        self.docw = MyQDockWidget()
        win.addDockWidget(Qt.RightDockWidgetArea, self.docw)
        # self.addTab(number="tabbar")
        # print(self.__machine)

        self.myEvent()

    # 保存机器状态
    def saveMachineSate(self,number,webview:WebView=None,state:bool=True):
        if webview is None:
            self.__machine[number]["state"]=state
        else:
            self.__machine[number] = {"web":webview,"state":state}

    # 检测是否创建过number Tab
    def is_machine(self,number:str):
        if number in self.__machine:
            return True
        return False

    # 获取number的窗口
    def get_machine(self,number:str)->WebView:
        if self.__machine.get(number,None) is None:
            return None
        return self.__machine[number].get("web",None)

    # 重新加载窗口
    def reload_machine(self,number:str,url:str):
        if self.get_machine(number):
            self.get_machine(number).load(url)

    def addTab(self, widget: QWidget=None, number: str="",pos:int=None,url=None):
        win = QMainWindow()
        self.docw = MyQDockWidget()

        self.gbox = QGridLayout(self.docw.getWidget())
        # 如果机器打开过,则直接获取窗口
        if self.is_machine(number):
            webview = self.get_machine(number)
        else:
            webview = WebView(self.docw)
            webview.adjustSize()
            # 忽略证书
            webview.setPage(webview.web)
            webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            if url is None:
                # webview.load("http://www.baidu.com")
                webview.load("https://198.204.247.82/ui/")
            else:
                webview.load(url)
        self.gbox.addWidget(webview)
        win.addDockWidget(Qt.RightDockWidgetArea, self.docw)
        # self.tab_list.append(win)

        if pos is None:
            super().addTab(win, number)
        else:
            super().insertTab(pos, win, number)

        # 保存机器状态
        self.saveMachineSate(number,webview)

    # 自定义拖拽事件
    def tabDragEvent(self,b:bool):
        if b:
            self.docw.setFloating(True)

    # tab关闭
    def tab_close_Event(self,index:int):
        number = self.tabText(index)
        self.removeTab(index)
        self.saveMachineSate(number,None,False)

    # tab双击事件
    def tabDouble(self,index:int):
        number = self.tabText(index)
        if number:
            self.tabDoubleed.emit(number)

    def myEvent(self):
        # self.tab.draged.connect(self.tabDragEvent)
        self.tabCloseRequested.connect(self.tab_close_Event)
        # tab点击事件
        self.tabBarDoubleClicked.connect(self.tabDouble)


if __name__ == '__main__':
    app = QApplication(sys.argv + ["--no-sandbox"])
    QCoreApplication.setOrganizationName("QT")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    win = TabBar()
    win.show()

    sys.exit(app.exec_())
