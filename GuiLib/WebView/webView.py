# -*- coding:utf-8 -*-
# @time:2022/8/2016:44
# @author:LX
# @file:webView.py
# @software:PyCharm
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMessageBox


class WebEnginePage(QWebEnginePage):

    # 忽略证书
    def certificateError(self, QWebEngineCertificateError):
        return True


class WebView(QWebEngineView):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        # 锁
        self.lock = {"state": True, "id": "0", "treeitem": None}
        # 缓存设置
        # self.profile = QWebEngineProfile("s",self)
        # self.profile.defaultProfile().persistentStoragePath()
        # 从缓存中读取网页
        # self.settings = QWebEngineSettings.globalSettings()
        # 这个证书一定要放在这里,放在其他地方网页无法显示
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
            super().load(QUrl(url))
            self.locked()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    webview = WebView()
    webview.setPage(webview.web)
    webview.load("https://198.204.247.82/ui/")
    webview.show()
    sys.exit(app.exec_())
