# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QTableWidgetItem, QPushButton, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets

from GuiLib.TreeTab.treeTab import TreeTab
from core.menusys.menuSys import MenuSys
from GuiLib.WebView.webView import WebView

import threading


class Main(QMainWindow):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.setupUi()
        self.myMenu()
        self.Init()
        self.myEvent()

    def Init(self):
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.widget_main.setLayout(self.hbox)

        self.treeTab = TreeTab()
        self.hbox.addWidget(self.treeTab)

        # 添加
        for ip in self.treeTab.usableMachine():
            ip = ip[0]
            self.addTable(ip)

    # 隐藏/显示左侧树
    def visLeft(self,vis:bool):
        if vis:
            self.treeTab.visTree(vis)
        else:
            self.treeTab.visTree(vis)

    # 隐藏/显示右侧
    def visRight(self,vis:bool):
        if vis:
            self.splitter.setSizes([self.width(),0])
        else:
            width = int(self.width()*0.25)
            self.splitter.setSizes([self.width()-width,width])

    # 隐藏左右
    def hideLeftRigth(self):
        self.visLeft(True)
        self.visRight(True)

    # 默认视图
    def defaultView(self):
        self.visLeft(False)
        self.visRight(False)

    # tableWidget
    def myTableWidget(self):
        self.tableWidget = QtWidgets.QTableWidget(self.widget_jpg_down_show)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.tableWidget)

    def down_jpg(self,ip):
        print("ip->",ip)

    # 添加table,下载图片的
    def addTable(self,ip:str):
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row+1)

        item = QTableWidgetItem(ip)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(row, 0, item)
        # 添加下载按钮
        btn_down = QPushButton("下载图片")
        btn_down.setStyleSheet('''
        border:none;
        ''')
        btn_down.clicked.connect(lambda :self.down_jpg(ip))
        self.tableWidget.setCellWidget(row, 1, btn_down)

    def login_success_event(self,b,hide_webView):
        hide_webView.im_map(hide_webView)
        # 结果
#         def re_(d):
#             print("d:",d)
#         # 这里有问题
#         print("隐藏浏览器登录成功",b)
#         js_click='''
# function clickVM(){
#     var e = document.getElementsByClassName("inline");
#     e[3].click();
# }
#         '''
#         hide_webView.page().runJavaScript(js_click)
#         hide_webView.page().runJavaScript("clickVM();")
#         print("--><<>")
#         js_find_ip='''
# function getIpDict(){
#     real_id = {};
#     // 获取机器真实访问id
#     var tb= document.getElementsByTagName("tbody")[0];
#     var tb_childs = tb.childNodes;
#     for(var i=0;i<tb_childs.length;i++){
#         var tt = tb_childs[i].childNodes[1].childNodes[0];
#         var title = tt.getAttribute("title");
#         if(title!="pfsense"){
#             var real_t = tt.getAttribute("data-moid");
#             real_id[title]=real_t;
#         }
#     }
#     console.log(real_id);
#     return 10;
# }
#         '''
#         hide_webView.page().runJavaScript(js_find_ip)
#         hide_webView.page().runJavaScript("getIpDict();",re_)


    # ip映射事件
    def ip_map_event(self):
        print("ip_map_event")
        ip = self.treeTab.usableMachine()[1][0]
        # for ip in self.treeTab.usableMachine():
        #     ip = ip[0]
        # 创建隐藏浏览器
        url = "https://{}/ui/".format(ip)
        print(url)
        hide_webView = WebView()
        hide_webView.setPage(hide_webView.web)
        hide_webView.load(url)
        hide_webView.loginSuccessfuled.connect(lambda b:self.login_success_event(b,hide_webView))
        self.treeTab.testaddTab(hide_webView)

    def myMenu(self):
        self.menu = MenuSys(self)
        self.menu.addMenuHeader(["视图", "设置"])
        self.menu.addMenuChild("视图", ["默认视图", "隐藏左","隐藏右","隐藏左右"])
        self.menu.addMenuChild("设置", ["Ip映射","进入配置页面","回主页"])
        self.menu.connect("视图", "默认视图", lambda: self.defaultView())
        self.menu.connect("视图", "隐藏左", lambda :self.visLeft(True))
        self.menu.connect("视图", "隐藏右", lambda :self.visRight(True))
        self.menu.connect("视图", "隐藏左右", lambda :self.hideLeftRigth())
        self.menu.connect("设置", "Ip映射", lambda :self.ip_map_event())
        self.menu.connect("设置","进入配置页面",lambda :self.stackedWidget.setCurrentIndex(1))
        self.menu.connect("设置","回主页",lambda :self.stackedWidget.setCurrentIndex(0))

    def setupUi(self):
        self.setObjectName("self")
        self.resize(1072, 739)
        self.setStyleSheet('''
*{
background-color: rgb(62, 62, 93);
font: 11pt "黑体";
color: rgb(247, 247, 247);
}
#widget_main{
background-color: rgb(84, 84, 125);
border-right:4px solid rgb(50, 50, 74);
}
#widget_right,#btn_search{
background-color: rgb(118, 64, 127);
}
#btn_search{
background-color:rgb(85, 85, 255);
}
#btn_search:hover{
background-color:rgb(64, 64, 191);
}
#btn_search:pressed{
	background-color: rgb(85, 85, 255);
}
#btn_search,#lineEdit_search{
border:1px solid rgb(0, 0, 0);
}
#lineEdit_search{
border-right:none;
}
#btn_search{
border-left:none;
}
#btn_jpg{
border-radius:40px;
}
#widget_right{
border-radius:5px;
}

#btn_m_update,#btn_db_update{
	background-color: rgb(85, 170, 127);
border:1px solid rgb(33, 67, 50);
border-radius:5px;
}
#btn_m_update:pressed,#btn_db_update:pressed{
background-color: rgb(60, 121, 90);
}
#tableWidget{
border:1px solid rgb(113, 113, 113);
}
#widget{
	border-left:5px solid rgb(82, 82, 122);
}
        ''')
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(2, 0, 2, 0)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_main = QtWidgets.QWidget()
        self.page_main.setObjectName("page_main")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_main)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.page_main)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget_main = QtWidgets.QWidget(self.splitter)
        self.widget_main.setStyleSheet("")
        self.widget_main.setObjectName("widget_main")

        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setMaximumSize(QtCore.QSize(291, 16777215))
        self.widget.setObjectName("widget")
        self.widget.setContentsMargins(9,9,9,9)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        # self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_right = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_right.sizePolicy().hasHeightForWidth())
        self.widget_right.setSizePolicy(sizePolicy)
        self.widget_right.setMaximumSize(QtCore.QSize(301, 170))
        self.widget_right.setStyleSheet("")
        self.widget_right.setObjectName("widget_right")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_right)
        self.verticalLayout.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(self.widget_right)
        self.lineEdit_search.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lineEdit_search.setStyleSheet("")
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.btn_search = QtWidgets.QPushButton(self.widget_right)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_search.sizePolicy().hasHeightForWidth())
        self.btn_search.setSizePolicy(sizePolicy)
        self.btn_search.setMinimumSize(QtCore.QSize(41, 41))
        self.btn_search.setMaximumSize(QtCore.QSize(41, 41))
        self.btn_search.setStyleSheet("")
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout.addWidget(self.btn_search)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btn_jpg = QtWidgets.QPushButton(self.widget_right)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_jpg.sizePolicy().hasHeightForWidth())
        self.btn_jpg.setSizePolicy(sizePolicy)
        self.btn_jpg.setMinimumSize(QtCore.QSize(80, 80))
        self.btn_jpg.setMaximumSize(QtCore.QSize(80, 16777215))
        self.btn_jpg.setObjectName("btn_jpg")
        self.verticalLayout.addWidget(self.btn_jpg, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.widget_right)
        self.widget_jpg_down_show = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_jpg_down_show.sizePolicy().hasHeightForWidth())
        self.widget_jpg_down_show.setSizePolicy(sizePolicy)
        self.widget_jpg_down_show.setObjectName("widget_jpg_down_show")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_jpg_down_show)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.myTableWidget()  # 添加表格
        self.verticalLayout_2.addWidget(self.widget_jpg_down_show)
        self.horizontalLayout_2.addWidget(self.splitter)
        self.stackedWidget.addWidget(self.page_main)
        self.page_setting = QtWidgets.QWidget()
        self.page_setting.setObjectName("page_setting")
        self.groupBox_ip_tree = QtWidgets.QGroupBox(self.page_setting)
        self.groupBox_ip_tree.setGeometry(QtCore.QRect(10, 20, 210, 150))
        self.groupBox_ip_tree.setObjectName("groupBox_ip_tree")
        self.radiobtn_all = QtWidgets.QRadioButton(self.groupBox_ip_tree)
        self.radiobtn_all.setGeometry(QtCore.QRect(40, 20, 151, 31))
        self.radiobtn_all.setObjectName("radiobtn_all")
        self.radiobtn_usable = QtWidgets.QRadioButton(self.groupBox_ip_tree)
        self.radiobtn_usable.setGeometry(QtCore.QRect(40, 70, 151, 31))
        self.radiobtn_usable.setObjectName("radiobtn_usable")
        self.groupBox_machine = QtWidgets.QGroupBox(self.page_setting)
        self.groupBox_machine.setGeometry(QtCore.QRect(270, 20, 210, 150))
        self.groupBox_machine.setObjectName("groupBox_machine")
        self.label_m_use = QtWidgets.QLabel(self.groupBox_machine)
        self.label_m_use.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.label_m_use.setObjectName("label_m_use")
        self.lineEdit_m_use = QtWidgets.QLineEdit(self.groupBox_machine)
        self.lineEdit_m_use.setGeometry(QtCore.QRect(20, 45, 113, 20))
        self.lineEdit_m_use.setObjectName("lineEdit_m_use")
        self.label_m_pwd = QtWidgets.QLabel(self.groupBox_machine)
        self.label_m_pwd.setGeometry(QtCore.QRect(20, 85, 54, 12))
        self.label_m_pwd.setObjectName("label_m_pwd")
        self.lineEdit_m_pwd = QtWidgets.QLineEdit(self.groupBox_machine)
        self.lineEdit_m_pwd.setGeometry(QtCore.QRect(20, 100, 113, 20))
        self.lineEdit_m_pwd.setObjectName("lineEdit_m_pwd")
        self.btn_m_update = QtWidgets.QPushButton(self.groupBox_machine)
        self.btn_m_update.setGeometry(QtCore.QRect(150, 110, 51, 31))
        self.btn_m_update.setObjectName("btn_m_update")
        self.groupBox_DB = QtWidgets.QGroupBox(self.page_setting)
        self.groupBox_DB.setGeometry(QtCore.QRect(10, 200, 210, 150))
        self.groupBox_DB.setObjectName("groupBox_DB")
        self.label_db_use = QtWidgets.QLabel(self.groupBox_DB)
        self.label_db_use.setGeometry(QtCore.QRect(23, 35, 54, 12))
        self.label_db_use.setObjectName("label_db_use")
        self.lineEdit_db_use = QtWidgets.QLineEdit(self.groupBox_DB)
        self.lineEdit_db_use.setGeometry(QtCore.QRect(23, 50, 113, 20))
        self.lineEdit_db_use.setObjectName("lineEdit_db_use")
        self.label_db_pwd = QtWidgets.QLabel(self.groupBox_DB)
        self.label_db_pwd.setGeometry(QtCore.QRect(23, 95, 54, 12))
        self.label_db_pwd.setObjectName("label_db_pwd")
        self.lineEdit_db_pwd = QtWidgets.QLineEdit(self.groupBox_DB)
        self.lineEdit_db_pwd.setGeometry(QtCore.QRect(23, 110, 113, 20))
        self.lineEdit_db_pwd.setObjectName("lineEdit_db_pwd")
        self.btn_db_update = QtWidgets.QPushButton(self.groupBox_DB)
        self.btn_db_update.setGeometry(QtCore.QRect(151, 114, 51, 31))
        self.btn_db_update.setObjectName("btn_db_update")
        self.groupBox_ip_right = QtWidgets.QGroupBox(self.page_setting)
        self.groupBox_ip_right.setGeometry(QtCore.QRect(272, 200, 210, 150))
        self.groupBox_ip_right.setObjectName("groupBox_ip_right")
        self.checkBox_restart = QtWidgets.QCheckBox(self.groupBox_ip_right)
        self.checkBox_restart.setGeometry(QtCore.QRect(20, 28, 101, 21))
        self.checkBox_restart.setObjectName("checkBox_restart")
        self.checkBox_off = QtWidgets.QCheckBox(self.groupBox_ip_right)
        self.checkBox_off.setGeometry(QtCore.QRect(20, 60, 101, 21))
        self.checkBox_off.setObjectName("checkBox_off")
        self.checkBox_on = QtWidgets.QCheckBox(self.groupBox_ip_right)
        self.checkBox_on.setGeometry(QtCore.QRect(20, 90, 101, 21))
        self.checkBox_on.setObjectName("checkBox_on")
        self.checkBox_state = QtWidgets.QCheckBox(self.groupBox_ip_right)
        self.checkBox_state.setGeometry(QtCore.QRect(20, 120, 101, 21))
        self.checkBox_state.setObjectName("checkBox_state")
        self.groupBox_downJPG = QtWidgets.QGroupBox(self.page_setting)
        self.groupBox_downJPG.setGeometry(QtCore.QRect(510, 24, 210, 150))
        self.groupBox_downJPG.setObjectName("groupBox_downJPG")
        self.label_browser = QtWidgets.QLabel(self.groupBox_downJPG)
        self.label_browser.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.label_browser.setObjectName("label_browser")
        self.lineEdit_browser_path = QtWidgets.QLineEdit(self.groupBox_downJPG)
        self.lineEdit_browser_path.setGeometry(QtCore.QRect(10, 50, 113, 20))
        self.lineEdit_browser_path.setObjectName("lineEdit_browser_path")
        self.btn_browser = QtWidgets.QPushButton(self.groupBox_downJPG)
        self.btn_browser.setGeometry(QtCore.QRect(122, 49, 41, 23))
        self.btn_browser.setObjectName("btn_browser")
        self.stackedWidget.addWidget(self.page_setting)
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1072, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "机器"))
        self.lineEdit_search.setPlaceholderText(_translate("self", "机器编号"))
        self.btn_search.setText(_translate("self", "搜索"))
        self.btn_jpg.setText(_translate("self", "JPG"))
        self.groupBox_ip_tree.setTitle(_translate("self", "IP树"))
        self.radiobtn_all.setText(_translate("self", "显示全部IP地址"))
        self.radiobtn_usable.setText(_translate("self", "只显示可用IP地址"))
        self.groupBox_machine.setTitle(_translate("self", "机器登录账号"))
        self.label_m_use.setText(_translate("self", "账号"))
        self.label_m_pwd.setText(_translate("self", "密码"))
        self.btn_m_update.setText(_translate("self", "更新"))
        self.groupBox_DB.setTitle(_translate("self", "数据库账号密码"))
        self.label_db_use.setText(_translate("self", "账号"))
        self.label_db_pwd.setText(_translate("self", "密码"))
        self.btn_db_update.setText(_translate("self", "更新"))
        self.groupBox_ip_right.setTitle(_translate("self", "IP树右键服务功能"))
        self.checkBox_restart.setText(_translate("self", "重启功能"))
        self.checkBox_off.setText(_translate("self", "关机"))
        self.checkBox_on.setText(_translate("self", "开机"))
        self.checkBox_state.setText(_translate("self", "查看状态"))
        self.groupBox_downJPG.setTitle(_translate("self", "下载图片服务"))
        self.label_browser.setText(_translate("self", "浏览器驱动"))
        self.btn_browser.setText(_translate("self", "..."))

    # 搜索事件
    def search_Event(self):
        number = self.lineEdit_search.text()
        if number.isdigit():
            if self.treeTab.openMachine(number) is None:
                # 提示没有该机器
                QMessageBox.information(self, "提示", "没有该机器")
        else:
            QMessageBox.information(self, "提示", "请输入正确的机器编号")
        self.lineEdit_search.setText("")

    # 事件
    def myEvent(self):
        self.lineEdit_search.returnPressed.connect(self.search_Event)
        self.btn_search.clicked.connect(self.search_Event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Main()
    win.show()

    sys.exit(app.exec_())
    