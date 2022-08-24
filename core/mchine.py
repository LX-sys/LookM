

'''

    处理机器的类
'''

import os
import datetime
from datetime import datetime as dt
import json
from Database.open_mysql import Machine
from core.ssh_reset_machine import reset_machine,off_machine,on_machine,state_machine,is_ssl_machine

# 缓存文件的目录
RootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
cache_folder = os.path.join(RootPath, "cache")
cache_file = "machine_ip.json"
# 存储机器的缓存文件
cache_path = os.path.join(cache_folder, cache_file)
print(cache_path)

# 当前时间
def get_now_time()->str:
    return dt.now().strftime("%Y-%m-%d")

# 7天之后的时间
def time_after_7(day=7)->str:
    data=dt.strptime(get_now_time(), "%Y-%m-%d") + datetime.timedelta(days=day)
    return data.strftime("%Y-%m-%d")


# 检查时间过期
def is_exceed(date_str:str):
    if dt.strptime(date_str,"%Y-%m-%d") < dt.strptime(get_now_time(),"%Y-%m-%d"):
        return True
    else:
        return False

# 缓存ip
def write_cache_ip(data:dict)->None:
    print("缓存中...")
    with open(cache_path, "w") as f:
        json.dump(data, f)
    print("缓存完成...")

# 读取缓存ip
def read_cache_ip()->dict:
    with open(cache_path, "r") as f:
         data = json.load(f)
    return data

URL=IP=str

class MachineDispose:
    def __init__(self):
        # 连接数据库
        self.__machine = Machine()
        # 初始化自动调用一次(只返回可用的机器)
        self.__usable_machine = self.get_machine_addr_all(sort=True)

    def machine(self) -> Machine:
        return self.__machine

    # 获取所有可用的机器
    def usableMachine(self)->list:
        u_m = []
        for m in self.__usable_machine:
            if m[2] == 0:
                u_m.append(m)
        return u_m

    # 刷新
    def refresh(self,is_delete:bool=None,sort:bool=True)->list:
        data = self.__machine.get_machine_addr_all(is_delete=is_delete, sort=sort)
        info = {
            "cache": data,
            "start_time": get_now_time(),
            "end_time": time_after_7()
        }
        write_cache_ip(info)
        # 更新可用机器
        self.__mchine_ip = self.get_machine_addr_all(is_delete=False,sort=True)
        return data

    # 获取所有机器的ip和范围
    def get_machine_addr_all(self,is_delete:bool=None,sort:bool=True)->list:
        temp = False
        if not os.path.isfile(cache_path):
            open(cache_path, "w").close()  # 创建文件
            temp = True
        else:
            data = read_cache_ip()
            if is_exceed(data["end_time"]):
                temp = True
            else:
                # 读取缓存
                return data["cache"]
        if temp:
            data = self.refresh(is_delete=is_delete,sort=sort)
        return data

    # 通过机器编号获取对应ip
    def number_to_ip(self,number:str)->list:
        for m in self.usableMachine():
            s,e = m[1].split("-")
            if int(s) <= int(number) <= int(e):
                return m

    # 通过机器编号获取对应ip的总访问地址
    def url(self,number:str)->URL:
        return "https://{}/ui/".format(self.number_to_ip(number[0]))

    # 通过编号返回具体机器的访问url
    def machineIDUrl(self,number)->URL:
        m = self.number_to_ip(number)
        ip = m[0]
        s, e = m[1].split("-")
        s,e= int(s),int(e)
        scope = e-s+1
        number = int(number)%scope
        if number > 1:
            number+=1
        return "https://{}/ui/#/host/vms/{}".format(ip,number)

if __name__ == '__main__':
    m = MachineDispose()
    while True:
        s = input("请输入机器编号:")
        m.refresh()