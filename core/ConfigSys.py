# -*- coding:utf-8 -*-
# @time:2022/8/2415:35
# @author:LX
# @file:ConfigSys.py
# @software:PyCharm

'''
    配置系统
'''
import os
import json


# 顶级路径
def rootPath()->str:
    z_path= os.getcwd().split("LookM")
    return os.path.join(z_path[0],"LookM")


# 配置文件路径
Config_Path = os.path.join(rootPath(),"Config","machine.json")


# 写入配置文件
def writeConfig(path,data:dict,encoding="utf-8")->None:
    with open(path, "w",encoding=encoding) as f:
        json.dump(data, f)


# 读取配置文件
def readConfig(path,encoding="utf-8")->dict:
    with open(path, "r",encoding=encoding) as f:
        return json.load(f)


class ConfigSys:
    def __init__(self):
        self._config = dict()
        self.__path = ""

    def path(self)->str:
        return self.__path

    def read(self,path,encoding="utf-8"):
        self.__path = path
        self._config=readConfig(path,encoding=encoding)

    def write(self,path,data,encoding="utf-8"):
        writeConfig(path,data,encoding=encoding)
        self.read(self.__path,encoding=encoding)

    def get(self,section,key)->str:
        if section in self._config:
            return self._config[section].get(key)

    def set(self,section,key,data,encoding="utf-8"):
        if self._config[section].get(key,None) is None:
            self._config[section][key] = dict()
        self._config[section][key]=data
        writeConfig(self.path(),self._config,encoding=encoding)

    def section(self)->list:
        return list(self._config.keys())

    def __str__(self):
        return "<{}>".format(self.__path)

if __name__ == '__main__':
    con = ConfigSys()
    con.read(Config_Path)
    print(con.get("Machine","user"))