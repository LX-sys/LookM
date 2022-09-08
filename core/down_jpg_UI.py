# -*- coding:utf-8 -*-
# @time:2022/9/713:47
# @author:LX
# @file:down_jpg_UI.py
# @software:PyCharm
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


class DownJpgTable:
    pass