# -*- coding:utf-8 -*-
# @time:2022/8/2415:35
# @author:LX
# @file:ConfigSys.py
# @software:PyCharm

'''
    配置系统
'''
from configparser import ConfigParser

class ConfigSys:
    def __init__(self):
        pass


if __name__ == '__main__':
    cf = ConfigParser()
    cf.read(r"D:\code\LookM\Config\machine.ini")
    print(cf.get("machine", "machine_name"))