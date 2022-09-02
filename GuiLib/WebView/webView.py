# -*- coding:utf-8 -*-
# @time:2022/8/2016:44
# @author:LX
# @file:webView.py
# @software:PyCharm
import os
import sys
import time
from PyQt5.QtCore import QUrl,pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEnginePage,QWebEngineScript
from PyQt5.QtWidgets import QApplication, QMessageBox
import threading

from core.ConfigSys import ConfigSys
'''
# 点击右侧虚拟机的时候，显示虚拟机的信息
var e = document.getElementsByClassName("inline");
e[3].click()
'''
'''
    // 获取机器真实访问id
function getIpDict(){
    real_id = {};
    // 获取机器真实访问id
    var tb= document.getElementsByTagName("tbody")[0];
    var tb_childs = tb.childNodes;
    for(var i=0;i<tb_childs.length;i++){
        var tt = tb_childs[i].childNodes[1].childNodes[0];
        var title = tt.getAttribute("title");
        if(title!="pfsense"){
            var real_t = tt.getAttribute("data-moid");
            real_id[title]=real_t;
        }
    }
    console.log(real_id);
    return real_id;
}
'''


# 顶级路径
def rootPath()->str:
    z_path= os.getcwd().split("LookM")
    return os.path.join(z_path[0],"LookM")


# 配置文件路径
Config_Path = os.path.join(rootPath(),"Config","machine.json")
print(Config_Path)


class WebEnginePage(QWebEnginePage):
    # 忽略证书
    def certificateError(self, QWebEngineCertificateError):
        return True


class WebView(QWebEngineView):
    loginSuccessfuled = pyqtSignal(bool)
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        # 锁
        self.lock = {"state": True, "id": "0", "treeitem": None}
        # 自动登录检测
        self.autoLogin_ = {"state":None,"max_time":80,"interval":1,"cutime":80}
        # 读取配置
        self.config = ConfigSys()
        self.config.read(Config_Path)

        self.web = WebEnginePage()

    # 跳转功能
    def createWindow(self, QWebEnginePage_WebWindowType):
        return self

    def islock(self):
        return self.lock["state"]

    # 加锁
    def locked(self):
        self.lock["state"] = False

    # 解锁
    def unlock(self):
        self.lock["state"] = True

    def load(self, url:str) -> None:
        if not self.islock():
            yes = QMessageBox.information(self, "切换机器", "切换到{}".format(url),
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if yes == QMessageBox.Yes:
                self.unlock()

        if self.islock():
            url = QUrl(url)
            self.setUrl(url)
            super().load(url)
            # 自动登录线程
            self.page().runJavaScript(self.js())  # 这里必须先注入一次才行
            th = threading.Thread(target=self.autoLogin)
            th.start()
            self.locked()


    def js(self)->str:
        user = self.config.get("Machine", "user")
        pwd = self.config.get("Machine", "pwd")
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
            '''.replace("<user>", user)
        js_ = js_.replace("<pwd>", pwd)
        return js_

    # 检测,回调
    def detection(self,b):
        self.autoLogin_["state"]=b


    def im_map(self,webView):
        js_click = '''
        function clickVM(){
            var e = document.getElementsByClassName("inline");
            if(e==null){
                return 0;
            }else{
                e[3].click();
                return 1;
            }
        }
        '''

        # 局部 全局变量,检测是否点击虚拟机
        click_result = {"state":True,"max_count":60,"interval":1,"cu_count":0}
        find_ip_result = {"state":True,"max_count":100,"interval":1,"cu_count":0}
        def clickCallback(result): # 点击回调函数
            if result:
                print("点击虚拟机成功")
                click_result["state"]=False

        def click(js,webView): # 点击函数
            while click_result["state"]:
                webView.page().runJavaScript(js)
                webView.page().runJavaScript("clickVM();", clickCallback)
                time.sleep(click_result["interval"])
                click_result["cu_count"]+=1
                if click_result["cu_count"] == click_result["max_count"]:
                    print("失败")
                    break

        # ip映射函数
        js_find_ip = '''
        function getIpDict(){
            real_id = {};
            // 获取机器真实访问id
            var tb= document.getElementsByTagName("tbody");
            if(tb.length==0){
                return 0;
            }else{
                tb=tb[0];
            }
            var tb_childs = tb.childNodes;
            for(var i=0;i<tb_childs.length;i++){
                var tt = tb_childs[i].childNodes[1].childNodes[0];
                var title = tt.getAttribute("title");
                if(title!="pfsense"){
                    var real_t = tt.getAttribute("data-moid");
                    real_id[title]=real_t;
                }
            }
            return real_id;
        }
        '''
        def find_ipCallback(result): # 点击回调函数
            print("ip映射结果:",result,type(result))
            if result:
                print("ip映射成功:",result)
                find_ip_result["state"]=False

        def find_ip(js,webView): # 点击函数
            while find_ip_result["state"]:
                webView.page().runJavaScript(js)
                webView.page().runJavaScript("getIpDict();", find_ipCallback)
                time.sleep(find_ip_result["interval"])
                find_ip_result["cu_count"]+=1
                if find_ip_result["cu_count"] == find_ip_result["max_count"]:
                    print("ip映射失败")
                    break

        th = threading.Thread(target=click,args=(js_click,webView))
        th.start()
        th_ip = threading.Thread(target=find_ip, args=(js_find_ip, webView))
        th_ip.start()


    # 自动登录
    def autoLogin(self):
        while self.autoLogin_["cutime"]:
            if self.autoLogin_["state"]:
                print("自动登录成功")
                print(self.url())
                self.loginSuccessfuled.emit(True) # 自动登录成功触发信号
                break
            self.page().runJavaScript(self.js())
            self.page().runJavaScript('isName();', self.detection)
            time.sleep(self.autoLogin_["interval"])
            self.autoLogin_["cutime"] -= 1





if __name__ == '__main__':
    app = QApplication(sys.argv)
    webview = WebView()
    webview.setPage(webview.web)
    webview.load("https://198.204.247.82/ui/")
    print(webview.url().url())
    webview.show()
    sys.exit(app.exec_())
