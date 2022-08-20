# -*- coding:utf-8 -*-
# @time:2022/8/612:00
# @author:LX
# @file:Tree.py
# @software:PyCharm

import copy
import re
import sys,os
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt, pyqtSignal, QSize, QModelIndex
from PyQt5.QtGui import QMouseEvent, QCursor,QIcon
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QMenu, QInputDialog,
                             QListWidgetItem, QMessageBox, QTreeWidgetItem)

# 路径
RootPath = os.path.abspath(os.path.dirname(__file__))
icon_Path = os.path.join(RootPath, "icon")



class Tree(QTreeWidget):
    filenameedit = pyqtSignal(str)  # 双击文件事情,发送文件名时间
    rightClicked = pyqtSignal()  # 鼠标右键信号
    rightClickFile = pyqtSignal(str)  # 鼠标右键信号,带文件名
    leftClicked = pyqtSignal(QTreeWidgetItem)  # 左键信号
    delefolder = pyqtSignal(str)  # 删除文件夹信号
    delefile = pyqtSignal(str)   #  删除文件信号

    def __init__(self, *args, **kwargs):
        super(Tree, self).__init__(*args, **kwargs)
        # default这是一个特殊的key,用于存储在最外层的.qss文件
        self.__structure_tree = dict()
        # 当前右键选中的节点
        self.currentItem = None  # type:QTreeWidgetItem
        # 后缀名
        self.suffix = ""
        # 鼠标右键功能,创建文件功能,而改为用事件代替
        self.right_menu_createfile_bool = True
        # 注册右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_Event)
        self.myEvent()
        self.Init()

    def Init(self):

        self.setHearderLabels(["IP", "范围"])
        self.setSuffix(".qss")
        self.createTree({("asd","1-20",True): ["450","123"]})
        self.setCloseMouseRight(False)

    def tree(self)->dict:
        return self.__structure_tree

    # 设置后缀
    def setSuffix(self, suffix: str):
        self.suffix = suffix

    # 隐藏头
    def setHeaderVisable(self, visable: bool):
        self.header().setVisible(visable)

    def setHearderLabels(self, labels: list):
        self.setHeaderLabels(labels)

    # 默认图标
    def get_default_icon(self)->QIcon:
        icon = QIcon()
        icon.addFile(os.path.join(icon_Path, "folder.png"), QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(os.path.join(icon_Path, "folder_open.png"), QSize(), QIcon.Normal, QIcon.On)
        icon.addFile(os.path.join(icon_Path, "folder_av.png"), QSize(), QIcon.Selected, QIcon.Off)
        icon.addFile(os.path.join(icon_Path, "folder_av_open.png"), QSize(), QIcon.Selected, QIcon.On)
        return icon

    # 创建树
    def createTree(self, tree_dict: dict, p_Item: QTreeWidgetItem = None):
        '''
        {
        "dasd":["301","302",{"ds":["ss"]}],
        }
        :return:
        '''
        # 展开
        # self.treeWidget.setItemsExpandable()
        for info, v_list in tree_dict.items():
            if p_Item is None:
                item = QTreeWidgetItem(self)
                item.setIcon(0, self.get_default_icon())
                if info not in self.__structure_tree:
                    if isinstance(info,tuple):
                        item.setText(0, info[0])
                        item.setText(1, info[1])
                        if info[2]:
                            item.setBackground(0, QtGui.QColor(255, 0, 0))
                    if isinstance(info, str):
                        item.setText(0, info)
                else:
                    raise Exception("文件夹已存在")
            else:
                item = p_Item
                item = QTreeWidgetItem(item)
                item.setIcon(0, self.get_default_icon())
                item.setText(0, info)
            self.addTopLevelItem(item)
            self.currentItem = item
            print(id(self.currentItem))
            for v in v_list:
                self.create_file(v)
            #     if isinstance(v, str):
            #         item_c = QTreeWidgetItem(item)
            #         item_c.setText(0, v)
            #         self.addTopLevelItem(item_c)
            #     else:
            #         self.createTree(v, item)

        # 结构树初始化
        self.__structure_tree = tree_dict

    # 判断节点是文件还是文件夹
    def is_folder(self, node: QTreeWidgetItem):
        if node is None:
            return None

        text = node.text(0)
        if self.suffix in text:
            return False
        return True


    def __is_have_file(self,name:str=None,mode:str=None)->bool:
        '''

        :param name: 节点
        :param mode: 文件或者是文件夹
            file
            folder
        :return:
        '''
        if self.currentItem is None:
            if self.tree().get("default") is None:
                return False
            else:
                f_list = self.tree()["default"]
                # 判断当前name是否为纯 xx.qss
                if re.findall("^[a-zA-Z0-9]*{}".format(self.suffix),name):
                    name="/"+name
                if name in f_list:
                    return True
                else:
                    return False

        if mode == "file":
            f_list = self.get_tree_list(self.currentItem)["file"]
        elif mode == "folder":
            f_list = self.get_tree_list(self.currentItem)["folder"]

        if name in f_list:
            return True
        else:
            return False

    # 鼠标右键创建文件夹(鼠标右键)
    def create_folder_right(self):
        text, ok = QInputDialog.getText(self, '创建文件夹', '请输入文件夹名称:')

        if not text:
            # 请输入文件夹名称
            QMessageBox.warning(self, "警告", "文件夹名称不能为空")
            return # 如果没有输入文件名称，则直接返回

        if self.__is_have_file(text, "folder"):
            QMessageBox.warning(self, "警告", "文件夹已存在")
            return

        if ok:
            if self.currentItem is None or self.currentItem.parent() is None: # 当前没有选中的节点
                if text in self.__structure_tree: # 判断最外层是否有该文件夹
                    QMessageBox.warning(self, "警告", "文件夹已存在")
                    return
                temp_item = self
            else:
                temp_item = self.currentItem.parent()
            # 判断当前选中的节点是文件还是文件夹
            if self.is_folder(self.currentItem):
                item = QTreeWidgetItem([text])
                item.setIcon(0, self.get_default_icon())
                self.currentItem.addChild(item)
                self.right_path_address(self.currentItem).append({text:[]})
                print(self.tree())
                return  # 如果是文件夹，则直接返回


            item = QTreeWidgetItem(temp_item)
            item.setIcon(0, self.get_default_icon())
            item.setText(0, text)
            self.addTopLevelItem(item)
            if temp_item is self: # 没有选择节点的情况
                self.tree()[text] = []
            else:# 新建文件夹
                self.right_path_address(temp_item).append({text: []})
            print(self.tree())

    # 关闭鼠标右键自带的功能,而改为用事件代替
    def setCloseMouseRight(self,close:bool):
        self.right_menu_createfile_bool = close

    def closeMouseRight(self)->bool:
        return self.right_menu_createfile_bool

    # 新建文件(鼠标右键)
    def create_file_right(self):
        if self.right_menu_createfile_bool:
            text, ok = QInputDialog.getText(self, '创建文件', '请输入文件名称:')
            if ok:
                self.create_file(text)
        else:
            self.rightClicked.emit()

    # 删除文件夹/文件(鼠标右键)
    def delete_right(self):
        if self.currentItem is None:
            print("没有选中的节点")
            return

        file_name = self.currentItem.text(0)
        if self.suffix in file_name: # 判断是否是文件
            file_name = self.fullPath(self.currentItem)+"/"+file_name
        # 顶级目录
        if self.currentItem.parent() is None:
            if self.suffix in file_name: # 如果是.qss文件
                self.tree()["default"].remove(file_name)
                self.takeTopLevelItem(self.currentIndex().row())
                self.delefile.emit(file_name)
                print(self.tree())
                return
            else:
                self.tree().pop(file_name)
                self.takeTopLevelItem(self.currentIndex().row())
                print(self.tree())
                self.delefolder.emit(file_name)
                return # 如果是文件夹，则直接返回

        # file_name = self.currentItem.text(0)
        if self.is_folder(self.currentItem):
            select = False
            if self.currentItem.childCount() > 0:
                select = QMessageBox.question(self, "警告", "该文件夹不为空,确认删除?", QMessageBox.Yes | QMessageBox.No)
            if select == QMessageBox.Yes:
                # 删除结构树中的文件夹/文件
                temp = self.right_path_address(self.currentItem.parent())
                for v in temp:
                    if isinstance(v,dict):
                        if list(v.keys())[0] == file_name:
                            temp.remove(v)
                            break
                self.currentItem.parent().removeChild(self.currentItem)
                self.delefolder.emit(file_name)
                print(self.tree())
            return
        else:
            # 文件的删除
            temp = self.right_path_address(self.currentItem.parent())
            temp.remove(file_name)
            self.currentItem.parent().removeChild(self.currentItem)
            self.delefile.emit(file_name)
        print(self.tree())

    # 完整路径
    def fullPath(self,item:QTreeWidgetItem):
        if self.currentItem is None:
            return ""
        else:
            path_list = self.right_path(item)
            # 判断是否为顶级文件xx.qss
            if len(path_list) == 1 and self.suffix in path_list[0]:
                return ""
            return "/".join(path_list)

    # 新建文件
    def create_file(self,ip:str,scope:str=None):
        if not ip:
            # 请输入文件名称
            QMessageBox.warning(self, "警告", "文件名称不能为空")
            return # 如果没有输入文件名称，则直接返回

        # 文件名
        qss_name = ip + self.suffix

        if self.__is_have_file(qss_name,"file"):
            QMessageBox.warning(self, "警告", "文件已存在")
            return

        if self.is_folder(self.currentItem):
            temp_item = self.currentItem
        elif self.currentItem is None:  # 当前没有选中的节点
            temp_item = self
        else:
            temp_item = self.currentItem.parent()
        item = QTreeWidgetItem(temp_item)
        item.setText(0, qss_name)
        if scope:
            item.setText(1, scope)
        self.addTopLevelItem(item)

        qss_name = self.fullPath(item) + "/" + qss_name

        if temp_item is self:
            if not self.tree().get("default", None):
                self.tree()["default"] = []
            self.tree()["default"].append(qss_name)
        else:
            self.right_path_address(temp_item).append(qss_name)

        # 发送信号
        self.rightClickFile.emit(qss_name)
        print(self.tree())
        return True

    # 鼠标右键的路径
    def right_path(self,currentItem:QTreeWidgetItem)->list:
        # 处理最外层
        if currentItem is None:
            return []
        if currentItem.parent() is None:
            return [currentItem.text(0)]

        # 路径跟踪列表
        path_track_list = []
        item = currentItem
        while item:
            p = item.parent()
            if p is not None:
                path_track_list.append(p.text(0))
            item = p
        # 反转
        path_track_list.reverse()

        # 如果点击的文件夹,则添加该文件夹名称
        if self.is_folder(currentItem):
            path_track_list.append(currentItem.text(0))
        return path_track_list

    # 根据右键路径,返回该空间的地址
    def right_path_address(self,currentItem:QTreeWidgetItem)->list:
        if currentItem is None:
            return []
        right_click_folder_name = currentItem.text(0)

        # --文件夹中添加文件夹有BUG
        path = self.right_path(currentItem)
        temp_tree = self.tree()
        temp = None
        if len(path) == 1:
            print(path)
            return self.tree()[path[0]]

        if self.is_folder(currentItem):
            for v in path:
                temp = temp_tree[v]
                for i in temp:
                    # 判断是否为文件夹,同时判断是否是右键所点击的文件夹
                    if isinstance(i,dict) and list(i.keys())[0] == right_click_folder_name:
                        temp_tree = i
                        break
                    else:
                        temp_tree = i
        else:
            for v in path:
                temp = temp_tree[v]
                break

        return temp

    # 获取文件夹下的文件列表
    def get_tree_list(self,currentItem:QTreeWidgetItem)->dict:

        file_names = {"file":[],"folder":[],"click":""} # 文件列表，文件夹列表，点击的节点名称
        if currentItem is None:
            return dict()

        # 文件
        if not self.is_folder(currentItem):
            if currentItem.parent() is None:
                return file_names
            else:
                currentItem = currentItem.parent()

        file_names["click"] = currentItem.text(0)

        for i in range(currentItem.childCount()):
            text = currentItem.child(i).text(0)
            if self.suffix in text:
                file_names["file"].append(text)
            else:
                file_names["folder"].append(text)
        return file_names

    def menu_Event(self, pos: QPoint):
        # 当前右键选中的节点
        self.currentItem = self.itemAt(pos)
        # 创建菜单
        menu = QMenu()
        # 添加菜单项
        # look_action = menu.addAction("重命名")
        # menu.addAction(look_action)
        #
        # c_file_action = menu.addAction("创建文件")
        # menu.addAction(look_action)
        # c_file_action.triggered.connect(self.create_file_right)
        #
        # c_folder_action = menu.addAction("创建文件夹")
        # menu.addAction(look_action)
        # c_folder_action.triggered.connect(self.create_folder_right)
        #
        # c_del_action = menu.addAction("删除")
        # menu.addAction(look_action)
        # c_del_action.triggered.connect(self.delete_right)
        #
        # look_action.setEnabled(False)
        # c_file_action.setEnabled(False)
        # c_folder_action.setEnabled(False)
        # c_del_action.setEnabled(False)

        # 显示菜单
        menu.exec_(QCursor.pos())

    # 双击节点事件
    def doubleClickedEvent(self, index: QModelIndex):
        # 双击对qss文件有效
        # 判断是否是纯数字
        text = index.data()
        full_path = self.fullPath(self.currentItem)+"/"+text
        if text.isdigit():
            # print(text)
            # 发送完整路径
            self.filenameedit.emit(full_path)

    # 单机节点事件
    def clickEvent(self, item, column):
        self.currentItem = item
        # 发现左键信号
        self.leftClicked.emit(item)

    # 获取所有文件的名称(有bug)
    def get_all_file_name(self,tree=None)->list:
        file_names = []
        if tree is None:
            tree = self.tree()

        for t in tree:
            for node in tree[t]:
                if self.suffix in node:
                    if t == "default":
                        file_names.append(node)
                    else:
                        file_names.append(t+"/"+node)
                if isinstance(node,dict):
                    file_names.extend(self.get_all_file_name(node))

        return file_names

    def myEvent(self):
        self.doubleClicked.connect(self.doubleClickedEvent)
        self.itemClicked.connect(self.clickEvent)


if __name__ == '__main__':
    # 测试
    app = QApplication(sys.argv)
    tree = Tree()
    tree.show()
    sys.exit(app.exec_())
