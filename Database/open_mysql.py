# -*- coding:utf-8 -*-
# @time:2022/8/2011:03
# @author:LX
# @file:open_mysql.py
# @software:PyCharm
# 操作mysql数据库
import copy
import pymysql

# 单利模式
class OperMysql:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, host="45.76.15.187", port=3306, user="root", password="HaiAn4242587_", db="AccuracyDB"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    # 连接数据库
    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)
            self.cursor = self.conn.cursor()
            print("连接数据库成功")
        except Exception as e:
            print(e)

    # 执行sql语句
    def execute(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    # 查询所有表
    def select_table(self):
        sql = "show tables"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 查询数据库
    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 关闭数据库
    def close(self):
        self.cursor.close()
        self.conn.close()


# 机器表
class Machine(OperMysql):
    TABLE_NAME = "machine"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.connect()

    # 机器数量
    def count_machine(self,is_delete:bool=None)->int:
        '''

        :param is_delete:
            None:返回所有机器数量
            True:返回删除的机器数量
            False:返回没有删除的机器数量
        :return:
        '''
        if is_delete is None:
            sql = "select count(*) from {}".format(Machine.TABLE_NAME)

        if is_delete == True:
            sql = "select count(*) from {} where is_delete=1".format(Machine.TABLE_NAME)

        if is_delete == False:
            sql = "select count(*) from {} where is_delete=0".format(Machine.TABLE_NAME)
        return self.select(sql)[0][0]

    # 返回所有机器的ip和范围
    def get_machine_addr_all(self,is_delete:bool=None,sort:bool=True)->list:
        '''

        :param is_delete:
            True:删除的机器
            Flase:没有删除的机器
        :param sort:
            True:降序
            False:升序
        :return:
        '''
        if is_delete is None:
            sql = "select machine_ip,scope,is_delete from {} ".format(Machine.TABLE_NAME)

        if is_delete == True:
            sql = "select machine_ip,scope from {} where is_delete=1".format(Machine.TABLE_NAME)

        if is_delete == False:
            sql = "select machine_ip,scope from {} where is_delete=0".format(Machine.TABLE_NAME)

        # 排序
        data = list(self.select(sql))
        data.sort(key=lambda x: int(x[1].split("-")[1]), reverse=sort)
        return data

if __name__ == '__main__':
    ma = Machine()
    print(ma.get_machine_addr_all(False))