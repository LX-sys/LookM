# -*- coding:utf-8 -*-
# @time:2022/9/717:08
# @author:LX
# @file:down_jpg.py
# @software:PyCharm

import os
import random
import threading
import requests
from requests.auth import HTTPBasicAuth

from core.ConfigSys import ConfigSys

# 顶级路径
def rootPath()->str:
    z_path= os.getcwd().split("LookM")
    return os.path.join(z_path[0],"LookM")

# 图片保存路径
JPG_PATH = os.path.join(rootPath(),"down_jpg")

# 代理配置路径
PROXIES_PATH = os.path.join(rootPath(),"Config","proxies.json")

def _jpg(user,pwd,url_list,proxies=None):
    for url in url_list:  # url:(机器编号,图片链接)
        number,img_link = url[0],url[1]
        try:
            res = requests.get(img_link, auth=HTTPBasicAuth(user, pwd),verify=False)
        except requests.exceptions.SSLError:
            if proxies:
                proxies_ = proxies
            else:
                # 从配置文件读取代理
                con = ConfigSys()
                con.read(PROXIES_PATH)
                proxies_ = {
                    "http": con.get("Proxies", "http"),
                    "https": con.get("Proxies", "https")
                }
            res = requests.get(img_link, auth=HTTPBasicAuth(user, pwd),proxies=proxies_, verify=False)

        # ---------------------------
        if res.status_code == 200:
            # 随机挑选目录
            path_ = os.path.join(JPG_PATH, str(random.randint(1, 2)), "{}.jpg".format(number))
            with open(path_, "ab") as f:
                f.write(res.content)
                print("{}.jpg 下载成功".format(number))
        else:
            print("失败状态码:",res.status_code)


def downJpg(user,pwd,url_dict,th_number=2,proxies=None):
    # 字典转 列表元组
    url_list = list(zip(url_dict.keys(),url_dict.values()))
    print(url_list)

    # 最多开启线程不能超过5个
    if th_number>5:
        th_number = 5

    period_list = []
    const_period = len(url_list)//th_number
    s = 0
    e = const_period
    # 为每个线程划分出要操作部分
    while True:
        data = url_list[s:e]
        if data:
            period_list.append(data)
            s+=const_period
            e+=const_period
        else:
            break
    print(period_list)
    #  线程池
    th_list = []
    for pe in period_list:
        th_list.append(
            threading.Thread(target=_jpg,args=(user,pwd,pe,proxies))
        )

    # 全部启动
    for th in th_list:
        th.start()
#
if __name__ == '__main__':
    s= {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10}
    downJpg(1,2,s,3)
