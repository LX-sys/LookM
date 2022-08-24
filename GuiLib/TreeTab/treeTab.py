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
# from GuiLib.Tab.tab import Tab

from core.mchine import MachineDispose

def url(ip):
    return "https://{}/ui/".format(ip)

# 返回具体机器的访问url
def machineIDUrl(ip,id):
    return  "https://{}/ui/#/host/vms/{}".format(ip,id)

# 返回登录的Js
def loginJs(user,pwd):
    js_ = '''
    function isName(){
        var user=document.getElementById("username");
        if(user){
            var c = document.getElementsByName("loginForm");
            if(!c){
                return ""
            }
            c[0].setAttribute("class","ng-valid ng-dirty ng-valid-parse");
            var user=document.getElementById("username");
            user.value = "<user>";
            user.setAttribute("class","margeTextInput ng-valid ng-touched ng-dirty ng-valid-parse");
            let input = document.getElementById('username');
            let event = new Event('input', { bubbles: true });
            let tracker = input._valueTracker;
            if (tracker) {
                tracker.setValue('');
            }
            input.dispatchEvent(event);

            var pwd=document.getElementById("password");
            pwd.value = "<pwd>";
            pwd.setAttribute("class","margeTextInput ng-valid ng-dirty ng-valid-parse ng-touched");
            input = document.getElementById('password');
            event = new Event('input', { bubbles: true });
            tracker = input._valueTracker;
            if (tracker) {
                tracker.setValue('');
            }
            input.dispatchEvent(event);
            var btnsubmit = document.getElementById("submit");
            // 移除登录的不可见属性
            btnsubmit.removeAttribute("disabled");
            btnsubmit.click();
            return true;
        }else{
            return false;
        }
        return false;
    }
    isName();'''.replace("<user>", user)
    js_ = js_.replace("<pwd>", pwd)
    return js_

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

        # 机器
        self.machine = MachineDispose()

        self.myEvent()
        self.Init()

    def Init(self) -> None:
        # 调整布局
        tree_w = int(self.width() * 0.25)
        self.splitter.setSizes([tree_w, self.width() - tree_w])
        # self.tree.createTree({("69.30.245.162", "1-20", True): ["450", "123"]})


    def addTab(self,text:str,url:str) -> None:
        self.tab.addTab(number=text, url=url)

    def ip_Event(self,ip_scope) -> None:
        print("-->",ip_scope)
        number = ip_scope[1]
        url=self.machine.machineIDUrl(number)
        self.addTab(text=number,url=url)

    # 登录实现
    def login(self,info:dict):
        number = info["number"]
        user = info.get("user")
        pwd = info.get("pwd")
        browser = self.tab.get_machine(number)
        if browser:
            # 注入js登录
            browser.page().runJavaScript(loginJs(user,pwd))

    # 双击tab在tree节点上定位
    def tabDouble(self,number:str):
        self.tree.textExpanded(number)

    def myEvent(self):
        self.tree.ipScope.connect(self.ip_Event)
        self.tree.logined.connect(self.login)
        # -----
        self.tab.tabDoubleed.connect(self.tabDouble)
        # self.tree.filenameedit.connect(self.addTab)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeTab = TreeTab()
    treeTab.show()

    sys.exit(app.exec_())