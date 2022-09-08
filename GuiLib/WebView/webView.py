# -*- coding:utf-8 -*-
# @time:2022/8/2016:44
# @author:LX
# @file:webView.py
# @software:PyCharm
import os
import sys
import time
from PyQt5.QtCore import QUrl,pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMessageBox,QProgressBar
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

'''
    2022.9.7  在打开机器的同时点击映射BUG报告
    Bug1
    当前存在我进度条渲染Bug,这是一个多线程的渲染问题
    临时解决办法 暂时注释 self.__addProgress()[这是增加当前进度的方法] 可以
    解决在打开机器的同时,点击映射程序直接崩溃的情况.
    
    Bug2,在打开机器的同时,点击映射,由于没有触发登录,所有会导致映射失败.
    
    最好的映射方法:
    打开程序后,什么机器都不要打开,先去映射,映射完成后,在操作机器
'''
class WebView(QWebEngineView):
    loginSuccessfuled = pyqtSignal(bool)
    ipMapData = pyqtSignal(dict) # 映射成功发送结果
    ipMapFailure = pyqtSignal() # 映射失败
    DownJpgDate = pyqtSignal(dict) # 下载图片
    DownJpgFailure = pyqtSignal() # 下载失败
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        # 锁
        self.lock = {"state": True, "id": "0", "treeitem": None}
        # 自动登录检测
        self.autoLogin_ = {"state":None,"max_time":80,"interval":1,"cutime":80}
        # 读取配置
        self.config = ConfigSys()
        self.config.read(Config_Path)

        # 从外部接收进度条对象
        self.progress = None  # type:QProgressBar

        self.web = WebEnginePage()

    def setProgress(self,progress):
        self.progress = progress

    # 如果有进度条对象就执行
    def __addProgress(self):
        if self.progress is not None:
            self.progress.setValue(self.progress.value()+1)

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
                # self.__addProgress()
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
                self.ipMapData.emit(result) # 发送信息
                find_ip_result["state"]=False

        def find_ip(js,webView): # 点击函数
            while find_ip_result["state"]:
                webView.page().runJavaScript(js)
                webView.page().runJavaScript("getIpDict();", find_ipCallback)
                time.sleep(find_ip_result["interval"])
                find_ip_result["cu_count"]+=1
                # self.__addProgress()
                if find_ip_result["cu_count"] == find_ip_result["max_count"]:
                    print("ip映射失败")
                    self.ipMapFailure.emit()
                    break

        th_ip_map_click = threading.Thread(target=click,args=(js_click,webView))
        th_ip_map_click.start()
        th_ip = threading.Thread(target=find_ip, args=(js_find_ip, webView))
        th_ip.start()
        print("线程启动")

    # 下载图片功能,待实现
    def im_dowm_image(self,webView):
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

        # 图片下载函数
        js_find_image = '''
function getImage(){
    real_line = {};
    // 获取机器真实访问id
    var tb= document.getElementsByTagName("tbody");
    if(tb.length==0){
        return 0;
    }else{
        tb=tb[0];
    }
    var tb_childs = tb.childNodes;
    for(var i=0;i<tb_childs.length;i++){
        var tt = tb_childs[i].childNodes[1].childNodes[0];  // 编号行
        var checkcbox = tb_childs[i].childNodes[0];  // 多选框
        console.log(checkcbox);
        var title = tt.getAttribute("title");
        console.log(title);
        if(title!="pfsense"){
            var inp = checkcbox.childNodes[0];
            inp.click();  // 点击选中
            setTimeout(function(){ // 延时2秒
                console.log("--");
            }, 2000);
            // 寻找图片
            var vm = document.getElementsByClassName("vmScreenScrape")[0];
            var img = vm.childNodes[3];
            var link = img.getAttribute("img-http-src");  // 获取图片链接
            console.log(link);
            inp.click();  // 取消选中
            // 保存链接
            real_line[title]=link;
        }
    }
    return real_line;
}
        '''
        def find_ImagCallback(result): # 点击回调函数
            print("img Link:",result,type(result))
            if result:
                print("img Link successful:",result)
                self.DownJpgDate.emit(result) # 发送信息
                find_ip_result["state"]=False

        def find_img(js,webView): # 点击函数
            while find_ip_result["state"]:
                webView.page().runJavaScript(js)
                webView.page().runJavaScript("getImage();", find_ImagCallback)
                time.sleep(find_ip_result["interval"])
                find_ip_result["cu_count"]+=1
                if find_ip_result["cu_count"] == find_ip_result["max_count"]:
                    print("图片链接下载失败")
                    self.DownJpgFailure.emit()
                    break

        th_img_click = threading.Thread(target=click,args=(js_click,webView))
        th_img_click.start()
        th_img = threading.Thread(target=find_img, args=(js_find_image, webView))
        th_img.start()
        print("下载图片链接线程启动")

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
            # 进度条增加
            # self.__addProgress()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    webview = WebView()
    webview.setPage(webview.web)
    webview.load("https://198.204.247.82/ui/")
    print(webview.url().url())
    webview.show()
    sys.exit(app.exec_())
