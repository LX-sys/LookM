# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'ip_map_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import sys
import random
import json
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem,QPushButton,QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets
from GuiLib.WebView.webView import WebView
from core.ConfigSys import ConfigSys

# 顶级路径
def rootPath()->str:
    z_path= os.getcwd().split("LookM")
    return os.path.join(z_path[0],"LookM")

# 真实机器id映射文件
real_ip_path = os.path.join(rootPath(), "Config", "ip_map.json")


class Down:
    def __init__(self,ip,progressBar,button=None) -> None:
        self.ip = ip
        self.progressBar = progressBar
        self.button = button


class IpMap(QWidget):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        # 初始化配置类
        self.config = ConfigSys()
        self.config.read(real_ip_path)

        self.setupUi()
        self.Init()

    def Init(self):
        self.tableWidget.setColumnCount(3)
        # 分配列宽
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setHorizontalHeaderLabels(['IP', '操作', '进度'])
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.createTable(["xxx.xxa","djklas.xx","wsx"])

    # 开始映射
    def strat_ip_map(self,b,hide_webView):
        hide_webView.im_map(hide_webView)

    # 获取映射成功结果
    def ip_map_data(self,url,data):
        print("ip_map_data",data)
        self.textBrowser.append(json.dumps(data))
        self.config.set("IP",url,data)
        print("保存成功")

    # 获取映射失败
    def ip_map_failure(self,webView):
        self.textBrowser.append(
            '{}映射失败'.format(webView.url().url())
        )


    # 映射实现
    def ip_map(self,down_obj):
        ip = down_obj.ip.split("|")[0]
        print(ip)
        print(down_obj.progressBar)
        # 创建隐藏浏览器
        url = "https://{}/ui/".format(ip)
        print("开始映射",url)
        hide_webView = WebView()
        hide_webView.resize(1200,1000)   # 这里的创建必须设置大

        down_obj.progressBar.setValue(0)
        hide_webView.setProgress(down_obj.progressBar) # 传递进度条

        hide_webView.setPage(hide_webView.web)
        hide_webView.load(url)

        hide_webView.loginSuccessfuled.connect(lambda b:self.strat_ip_map(b,hide_webView))
        hide_webView.ipMapData.connect(lambda data:self.ip_map_data(ip,data))
        hide_webView.ipMapFailure.connect(lambda :self.ip_map_failure(hide_webView))
        # self.treeTab.testaddTab(hide_webView)

    def createTable(self,ip_list):
        for i,ip in enumerate(ip_list):
            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row + 1)

            item = QTableWidgetItem(ip)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row, 0, item)

            # 添加进度条
            progress = QProgressBar()
            progress.setObjectName("progressBar")
            progress.setAlignment(Qt.AlignCenter)
            progress.setMaximum(180)
            progress.setFormat("%p%/%m")
            progress.setValue(0)
            self.tableWidget.setCellWidget(row, 2, progress)

            # 添加下载按钮
            btn_down = QPushButton("映射")
            btn_down.setObjectName("btn_down")
            btn_down.setStyleSheet('''
#btn_down{
border:none;
background-color:rgb(124, 124, 186);
}
#btn_down:hover{
background-color: rgb(0, 66, 197);
}
#btn_down:pressed{
background-color:rgb(124, 124, 186);
}
                                ''')
            '''
                这里使用了偏函数，将ip和进度条对象传入到ip_map函数中
            '''
            btn_down.clicked.connect(partial(self.ip_map,Down(ip,progress)))
            self.tableWidget.setCellWidget(row, 1, btn_down)


    def setupUi(self):
        self.setObjectName("self")
        self.resize(1193, 807)
        self.setStyleSheet('''
*{
background-color: rgb(62, 62, 93);
font: 11pt "黑体";
color: rgb(247, 247, 247);
}
#view{
border-left:5px solid rgb(52, 52, 77);
}
#tableWidget{
border:none;
}
#textBrowser{
border:1px solid rgb(106, 106, 158);
}
#progressBar{
	color: rgb(0, 0, 0);
}    
''')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.gh_widget = QtWidgets.QWidget(self.splitter)
        self.gh_widget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.gh_widget.setObjectName("gh_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.gh_widget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.gh_widget)
        self.tableWidget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.tableWidget.setStyleSheet("QHeaderView{\n"
"    color: rgb(0, 0, 0);\n"
"}")
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.textBrowser = QtWidgets.QTextBrowser(self.gh_widget)
        self.textBrowser.setMaximumSize(QtCore.QSize(371, 150))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.view = QtWidgets.QWidget(self.splitter)
        self.view.setObjectName("view")
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.tableWidget.setSortingEnabled(False)
        self.textBrowser.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'黑体\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = IpMap()
    win.show()

    sys.exit(app.exec_())
    