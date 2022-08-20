import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets



class LookMachine(QMainWindow):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.setupUi()
    
    def setupUi(self):
        self.setObjectName("self")
        self.resize(1072, 739)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget_main = QtWidgets.QWidget(self.splitter)
        self.widget_main.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.widget_main.setObjectName("widget_main")
        self.widget_right = QtWidgets.QWidget(self.splitter)
        self.widget_right.setMaximumSize(QtCore.QSize(301, 16777215))
        self.widget_right.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.widget_right.setObjectName("widget_right")
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1072, 23))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = LookMachine()
    win.show()

    sys.exit(app.exec_())
    