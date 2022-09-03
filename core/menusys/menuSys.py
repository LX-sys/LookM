# -*- coding:utf-8 -*-
# @time:2022/7/259:25
# @author:LX
# @file:menuSys.py
# @software:PyCharm

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QAction,QMenu,QMenuBar,QMainWindow

'''
# 原生代码
# self.menubar = QMenuBar(self)
# self.menu = QMenu(self.menubar)
# self.setMenuBar(self.menubar)
# self.menubar.addAction(self.menu.menuAction())
# self.menu.setTitle("文件")
#
#
# self.about = QMenu(self.menubar)
# self.setMenuBar(self.menubar)
# self.menubar.addAction(self.about.menuAction())
# self.about.setTitle("关于")
#
# # --------------文件------------------
# self.newjs = QAction("新建脚本",self)
# self.menu.addAction(self.newjs)
# self.newjs.triggered.connect(self.newJS_Event)
#
# self.updatejs = QAction("修改脚本", self)
# self.menu.addAction(self.updatejs)
#
# self.setting = QAction("设置", self)
# self.menu.addAction(self.setting)
#
# self.toLogin = QAction("返回登录界面", self)
# self.menu.addAction(self.toLogin)
# self.toLogin.triggered.connect(self.toLogin_Event)
#
# # ----------关于-------------------
# self.info_js = QAction("脚本管理系统",self)
# self.about.addAction(self.info_js)
'''

# 菜单操作类
class MenuSys:
    def __init__(self,main_win:QMainWindow, *args, **kwargs) -> None:
        '''
                self.menu = MenuSys(self)
                self.menu.addMenuHeader(["文件", "编辑"])
                self.menu.addMenuChild("文件", ["新建", "修改"])
                # self.menu.createMenu({"文件":["新建","修改"],"编辑":["撤销","重做"]})
                self.menu.connect("文件","新建",self.test)
                self.menu.setShortcut("文件","新建","Ctrl+N")


        :param main_win:
        :param args:
        :param kwargs:
        '''
        super().__init__(*args, **kwargs)
        # 主窗口对象
        self.main_win = main_win
        # 菜单栏树
        '''
            {
                "文件":["新建","修改"],
            }
        '''
        self.menu_tree = dict()
        '''
          {
            "文件":{
                    "obj":xxx,"child_obj":{"新建":xxx,"修改":xxx}
                    
                    }
          },
        '''
        self.menu_tree_obj = dict()
        # 菜单栏
        self.menubar = QMenuBar(self.main_win)
        self.Init()

    def Init(self) -> None:
        pass

    # 创建菜单
    def createMenu(self, menu_tree:dict) -> None:
        for parentNode,childNode in menu_tree.items():
            if parentNode not in self.menu_tree_obj:
                self.addMenuHeader([parentNode])
                self.addMenuChild(parentNode,childNode)

    # 只创建菜单栏
    def addMenuHeader(self, menu_hear:list):
        for menu_text in menu_hear:
            menu = QMenu(self.menubar)
            self.main_win.setMenuBar(self.menubar)
            self.menubar.addAction(menu.menuAction())
            menu.setTitle(menu_text)
            if menu_text not in self.menu_tree_obj:
                self.menu_tree_obj[menu_text]=dict()
                self.menu_tree_obj[menu_text]["obj"]=menu

    # 根据菜单名创建子菜单
    def addMenuChild(self,menu_header:str,child:list):
        self.menu_tree_obj[menu_header]["child_obj"] = dict() # 子菜单
        for child_text in child:
            action = QAction(child_text, self.main_win)
            self.menu_tree_obj[menu_header]["obj"].addAction(action)
            self.menu_tree_obj[menu_header]["child_obj"][child_text]=action

    # 返回子项对象
    def getChildObj(self,menu_header:str,child_text:str)->QAction:
        return self.menu_tree_obj[menu_header]["child_obj"][child_text]

    def connect(self,parent_menu_name:str,child_menu_name:str,target,args=tuple(),icon=None):
        obj = self.getChildObj(parent_menu_name,child_menu_name)
        if icon:
            obj.setIcon(QIcon(icon))
        obj.triggered.connect(lambda:target(*args))

    # 绑定快捷键
    def setShortcut(self,parent_menu_name:str,child_menu_name:str,shortcut:str):
        obj = self.getChildObj(parent_menu_name,child_menu_name)
        obj.setShortcut(shortcut)
        # obj.setShortcutContext(Qt.ApplicationShortcut)
        # obj.setShortcutEnabled(True)

    # 禁用/开放所有功能
    def allDisable(self,b:bool=True):
        for parentNode,childNode in self.menu_tree_obj.items():
            child_obj = childNode.get("child_obj")
            if child_obj:
                for child_obj in child_obj.values():
                    child_obj.setEnabled(b)


# 测试菜单操作类
class Test(QMainWindow):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        # self.Init()
        self.menu = MenuSys(self)
        self.menu.addMenuHeader(["文件", "编辑"])
        self.menu.addMenuChild("文件", ["新建", "修改"])
        # self.menu.createMenu({"文件":["新建","修改"],"编辑":["撤销","重做"]})
        self.menu.connect("文件","新建",self.test)

    def test(self):
        print("Dsad")

    def test2(self,h):
        print("dd",h)

if __name__ == '__main__':
    app = QApplication(sys.argv)


    win = Test()
    win.show()

    sys.exit(app.exec_())