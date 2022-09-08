# -*- coding:utf-8 -*-
# @time:2022/9/515:51
# @author:LX
# @file:open_xls.py
# @software:PyCharm
'''
    # 该类适用于python3.x+
    读取xls,xlsx,csv文件
'''


import typing
from typing import TypeVar
import xlrd2 as xlrd
from xlrd2 import Book
from xlrd2.sheet import Sheet
import csv

# int或者list
I_List = TypeVar("I_List",int,list)

class Xls:
    SUFFIX_XLS = "xls"
    SUFFIX_XLSX = "xlsx"
    SUFFIX_CSV = "csv"

    def __init__(self,xls_path:str=None):
        self.__xls_path = None
        self.__work_book = None  # type:Book
        self.__table = None # type:Sheet

        # 后缀
        self.suffix = ""

        if xls_path:
            self.setPath(xls_path)

    def setPath(self,xls_path:str):
        self.__xls_path = xls_path
        suffix = xls_path.split(".")[-1]

        if suffix == self.SUFFIX_XLS:
            self.suffix = self.SUFFIX_XLS
        elif suffix == self.SUFFIX_XLSX:
            self.suffix = self.SUFFIX_XLSX
        elif suffix == self.SUFFIX_CSV:
            self.suffix = self.SUFFIX_CSV
        else:
            raise Exception("File format error,support xls,xlsx,csv")

        if self.suffix in [Xls.SUFFIX_XLS,Xls.SUFFIX_XLSX]:
            self.__work_book = xlrd.open_workbook(self.path()) # type:Book
            self.__table = self.__work_book.sheet_by_index(0) # type:Sheet

    def path(self)->str:
        return self.__xls_path

    def read(self,encoding="utf-8",limit:I_List=10,sheet_index=0)->list:
        '''
            读取xls,xlsx,csv文件
        :param encoding:
        :param limit:
        :param sheet_index: 这个参数只对xls,xlsx有效
        :return:
        '''
        temp = []
        if self.suffix in [Xls.SUFFIX_XLS,Xls.SUFFIX_XLSX]:
            if sheet_index !=0:
                # 定位到sheet,默认第一个
                self.__table = self.__work_book.sheet_by_index(sheet_index) # type:Sheet

            if isinstance(limit,int):
                range_ = range(limit)
            elif isinstance(limit,list):
                range_ = range(limit[0],limit[1])
            else:
                raise Exception("limit type error,int,list")

            for i in range_:
                temp.append(self.__table.row_values(i))

        if self.suffix == Xls.SUFFIX_CSV:
            with open(self.path(),"r",encoding=encoding) as f:
                f_csv=csv.reader(f)

                if isinstance(limit, int):
                    range_ = range(limit)
                elif isinstance(limit, list):
                    for _ in range(limit[0]):
                        next(f_csv)
                    range_ = range(limit[1]-limit[0])
                else:
                    raise Exception("limit type error,int,list")

                for _ in range_:
                    temp.append(next(f_csv))
        return temp

    # 行,该方法只支持xls,xlsx
    def rows(self)->int:
        if self.suffix == Xls.SUFFIX_CSV:
            raise Exception("The method only supports xls,xlsx")
        if self.suffix in [Xls.SUFFIX_XLS,Xls.SUFFIX_XLSX]:
            return self.__table.nrows

    # 返回数据表中的第一行
    def headers(self,encoding="utf-8")->list:
        if self.suffix == Xls.SUFFIX_CSV:
            data = self.read(encoding,1)
            if data:
                return data[0]

        if self.suffix in [Xls.SUFFIX_XLS,Xls.SUFFIX_XLSX]:
            return self.__table.row_values(0)

        return []

    def write(self,encoding="utf-8"):
        pass

    # 该方法只支持xls,xlsx
    def sheets(self) -> list:
        if self.suffix == Xls.SUFFIX_CSV:
            raise Exception("The method only supports xls,xlsx")
        return self.__work_book.sheet_names()

    # 数据字典化
    def dataTodict(self,data:list):
        headers = self.headers()
        headers_len = len(headers)
        return {headers[i]:data[i] for i in range(headers_len)}

    def __str__(self)->str:
        return "[{}] {}".format(self.suffix,super(Xls, self).__str__())

if __name__ == '__main__':
    import random
    # xls = Xls(r"C:\Users\Administrator\Desktop\DE_table\2022_05_16_E_commerce_DE.csv")
    xls = Xls(r"C:\Users\Administrator\Desktop\DE_table\DE_22JUNE.csv")
    # xls = Xls(r"C:\Users\Administrator\Desktop\DE_table\test.xlsx")
    data = xls.read(limit=10,encoding="gbk")
    random_data = data[:2]
    print(xls.dataTodict(random_data[1]))
    # print(xls.headers())