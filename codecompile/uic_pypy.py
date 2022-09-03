
from PyQt5.QtWidgets import QMainWindow,QWidget
import re
'''
    uic生成的代码重新构建为可执行代码
'''


class CodeCov:

    def __init__(self) -> None:
        pass

    @staticmethod
    def readCode(filepath:str,mode:str="r",encoding:str="utf8")->list:
        code = []
        temp_code = []
        print(filepath)
        with open(filepath,mode,encoding=encoding) as f:
            while True:
                data = f.readline()
                if data:
                    temp_code.append(data)
                elif data == "\n":
                    code.extend(temp_code)
                    temp_code.clear()
                else:
                    break
        code.extend(temp_code)
        return code

    # 打印代码
    @staticmethod
    def codeShow(list_code:list)->None:
        for c in list_code:
            print(c, end="")

    @staticmethod
    def toString(list_code)->str:
        return "".join(list_code)

# 处理qtUic的代码
def dealCode(str_code: str, c_name, inheritance_name) -> str:
    if not str_code:
        return ""

    # setupUi后的名字
    st = re.findall("setupUi\(self, (.*)\)", str_code)[0]

    demo = str_code.replace(st, "self")
    demo = demo.replace("    def setupUi(self, self):", "    def setupUi(self):")

    demo = demo.replace("from PyQt5 import QtCore, QtGui, QtWidgets", '''import sys
from PyQt5.QtWidgets import QApplication, {}
from PyQt5 import QtCore, QtGui, QtWidgets'''.format(inheritance_name))

    # 匹配类名
    class_name = re.findall("class.*:", demo)[0]
    demo = demo.replace(class_name, '''
class {}({}):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.setupUi()
    '''.format(c_name, inheritance_name))

    demo = demo.replace("        self.retranslateUi(self)", "        self.retranslateUi()")
    demo = demo.replace("    def retranslateUi(self, self):", "    def retranslateUi(self):")
    demo = demo.replace("Qself","{}".format(inheritance_name))
    # 加代码
    demo += '''
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = {}()
    win.show()

    sys.exit(app.exec_())
    '''.format(c_name)
    return demo

# 处理qtUic生成的代码
def deal_Code(filepath:str,c_name:str="UI",inheritance_name:str="QMainWindow",mode:str="r",encoding:str="utf8",outfile:str=""):
    c = CodeCov()
    code_list = c.readCode(filepath,mode,encoding)
    code_str = c.toString(code_list)
    code = dealCode(code_str,c_name,inheritance_name)
    if outfile:
        with open(outfile,"w",encoding=encoding) as f:
            f.write(code)
        return None
    return code


deal_Code(r"D:\code\LookM\UI\ip_map_UI.py",
          outfile=r"D:\code\LookM\UI\ip_map_UI.py", c_name="IpMap", inheritance_name="QWidget")
