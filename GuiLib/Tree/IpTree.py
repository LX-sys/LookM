# -*- coding:utf-8 -*-
# @time:2022/8/2015:25
# @author:LX
# @file:IpTree.py
# @software:PyCharm
import sys,os

from PyQt5.QtCore import Qt, pyqtSignal, QSize, QModelIndex
from PyQt5.QtGui import QCursor,QIcon,QColor
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QMenu, QTreeWidgetItem, QHeaderView, QMessageBox)

# from Database.open_mysql import Machine
from core.mchine import MachineDispose
from core.ConfigSys import ConfigSys

# 顶级路径
def rootPath()->str:
    z_path= os.getcwd().split("LookM")
    return os.path.join(z_path[0],"LookM")

# 路径
RootPath = os.path.abspath(os.path.dirname(__file__))
# icon_Path = os.path.join(RootPath, "icon")
icon_Path = os.path.join(rootPath(),"GuiLib","Tree","icon")


# 配置文件的路径
Config_Path = os.path.join(rootPath(),"Config","machine.json")


# 自定义右键菜单
class RightMenu(QMenu):
    def __init__(self,*args,**kwargs):
        super(RightMenu,self).__init__(*args,**kwargs)
        # 注册的菜单列表
        self._menu_list = []

    # 添加菜单
    def addMenu(self,menu:str):
        action = self.addAction(menu)
        self.addAction(action)
        self._menu_list.append({
            "menu":menu,
            "action":action
        })

    def addMenus(self,menus:list):
        for menu in menus:
            self.addMenu(menu)

    # 获取菜单对象
    def getMenuObj(self,menu:str)->list:
        for v in self._menu_list:
            if v["menu"] == menu:
                return v["action"]

    # 连接信号槽
    def connect(self,menu:str,trigger_func=None):
        self.getMenuObj(menu).triggered.connect(trigger_func)

    # 禁用/启用指定功能
    def disableMenu(self,menus:list,enable:bool=True):
        for menu in menus:
            self.getMenuObj(menu).setEnabled(enable)

    # 隐藏获取显示指定功能
    def hideMenu(self,menus:list,hide:bool=True):
        for menu in menus:
            self.getMenuObj(menu).setVisible(hide)

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
    # 登录信号
    logined = pyqtSignal(dict)
    # 重新加载窗口
    reloaded = pyqtSignal(str)

    def __init__(self,*args,**kwargs):
        super(IpTree,self).__init__(*args,**kwargs)

        self.default_style()

        # 是否显示删除的机器
        self.__is_show_delete = True

        # self.__node = dict()
        #  处理机器的类
        self.__machine = MachineDispose()
        # 配置实例化,读取配置
        self._config = ConfigSys()
        self._config.read(Config_Path, encoding="utf-8")

        self.setHeaderLabels(["IP","范围"])
        self.header().setVisible(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 注册右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_Event)
        self.myEvent()
        self.Init()

    # 默认样式
    def default_style(self):
        self.setStyleSheet('''
QTreeWidget{
border:none;
border-right:5px solid rgb(82, 82, 122);
}
QTreeWidget::item:hover{
background-color: rgb(152, 152, 226);
}
QTreeWidget::item:selected{
background-color: rgb(152, 152, 226);
}
QTreeWidget::item:hover{
background-color: rgb(152, 152, 226);
}
QTreeWidget::item:selected{
background-color: rgb(152, 152, 226);
}
                ''')

    # 可用的机器列表
    def usableMachine(self):
        return self.__machine.usableMachine()

    # 是否显示删除的机器
    def setIsShowDelete(self,is_show_delete:bool):
        self.__is_show_delete = is_show_delete
        # self.refresh()

    # 默认图标
    def get_default_icon(self)->QIcon:
        icon = QIcon()
        icon.addFile(os.path.join(icon_Path, "folder.png"), QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(os.path.join(icon_Path, "folder_open.png"), QSize(), QIcon.Normal, QIcon.On)
        icon.addFile(os.path.join(icon_Path, "folder_av.png"), QSize(), QIcon.Selected, QIcon.Off)
        icon.addFile(os.path.join(icon_Path, "folder_av_open.png"), QSize(), QIcon.Selected, QIcon.On)
        return icon

    # 构建树
    def structData(self,refresh:bool=False)->dict:
        '''

        :param refresh:   是否刷新
        :return:
        '''
        if refresh == False:
            machine_data = self.__machine.get_machine_addr_all(sort=False)
        else:
            machine_data = self.__machine.refresh(sort=False)
        tree = dict()
        for data in machine_data:
            ip = data[0]
            spcre = data[1]
            is_delete = data[2]
            s, e = spcre.split("-")
            s, e = int(s), int(e)+1
            if is_delete == 1: # 删除的机器
                if self.__is_show_delete:
                    tree[(ip, spcre,IpTree.RED)] = [str(i) for i in range(s, e)]
            else:
                tree[(ip, spcre)] = [str(i) for i in range(s, e)]
        return tree

    def Init(self):
        # 这里不能直接传QColor(255,0,0),但是可以传元组
        # print(self.structData())
        # self.createTree({("198.204.247.82", "1-40",IpTree.BLUE): ["450", "123"]})
        self.setIsShowDelete(False)
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
        # number点击后有可能为空,直接用当前节点的text
        if number is None:
            number = self.currentItem().text(0)

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

    # 获取所有子节点
    def getAllChildNode(self)->list:
        node = []
        item_list = self.getAllParentNode()
        for item in item_list:
            child_count = item.childCount()
            node.extend(
                [item.child(i) for i in range(child_count)]
            )
        return node

    # 获取所有父节点
    def getAllParentNode(self)->list:
        item_count = self.topLevelItemCount()
        return [self.topLevelItem(item) for item in range(item_count)]

    # 根据文本获取树节点
    def getNode(self,text:str)->QTreeWidgetItem:
        for item in self.getAllChildNode():
            if item.text(0) == text:
                return item

    # 右键刷新
    def refresh(self):
        self.clear()
        self.createTree(self.structData(True))

    # 右键登录
    def login(self):
        number = self.currentItem().text(0)
        if number.isdigit(): # 只有数字才能登录
            # 从配置文件中读取登录信息
            user = self._config.get("Machine","user")
            pwd = self._config.get("Machine","pwd")
            print(user,pwd)
            self.logined.emit({"number":number,"user":user,"pwd":pwd})

    # 根据文本展开节点,并选中
    def textExpanded(self,text:str):
        item = self.getNode(text)
        if item:
            parent_item = item.parent()
            parent_item.setExpanded(True)
            self.setCurrentItem(item)

    # 全部展开/收起
    def allExpanded(self,expanded:bool=False):
        for item in self.getAllParentNode():
            item.setExpanded(expanded)

    # 重新加载窗口
    def reload(self):
        number = self.currentItem().text(0)
        if number.isdigit():
            self.reloaded.emit(number)

    # 菜单事件
    def menu_Event(self):
        # 创建菜单
        menu = RightMenu()
        # 添加菜单项
        menu.addMenu("刷新")
        menu.connect("刷新",self.refresh)
        menu.addMenu("登录")
        menu.connect("登录",self.login)
        menu.addMenu("全部收起")
        menu.connect("全部收起",self.allExpanded)
        menu.addMenu("重新加载窗口")
        menu.connect("重新加载窗口",self.reload)
        menu.exec_(QCursor.pos())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = IpTree()
    tree.show()

    sys.exit(app.exec_())