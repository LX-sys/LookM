# -*- coding:utf-8 -*-
# @time:2022/8/2313:59
# @author:LX
# @file:readJpg.py
# @software:PyCharm

import re
import os
from PIL import Image,ImageChops
import cv2
import threading

# 图片处理
# Hash值对比
def cmpHash(hash1, hash2,shape=(10,10)):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 相等则n计数+1，n最终为相似度
        if hash1[i] == hash2[i]:
            n = n + 1
    return n/(shape[0]*shape[1])

# 均值哈希算法
def aHash(img,shape=(10,10)):
    # 缩放为10*10
    img = cv2.resize(img, shape)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(shape[0]):
        for j in range(shape[1]):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 100
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(shape[0]):
        for j in range(shape[1]):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

# 图片类
class Jpg:
    def __init__(self):
        # 图片目录路径列表,图片路径
        self.__image_folder_path = []
        self.__image_path = dict()
        # 统计图片数量
        self.__count = dict()
        self.__counts = 0

    # 添加图片读取目录
    def addImageReadFolder(self, path:list):
        self.__image_folder_path.extend(path)

    # 加载图片
    def loadImage(self):
        def thImage(self,img):
            for root, dirs, files in os.walk(img, topdown=False):
                self.__image_path[root] = files

        for img in self.__image_folder_path:
            th = threading.Thread(target=thImage,args=(self,img))
            th.start()
            th.join()

    # 获取目录数量
    def getFolderCount(self)->int:
        return len(self.__image_path)

    # 图片数量
    def imageCount(self)->int:
        if self.__counts !=0:
            return self.__counts

        count = 0
        for img in self.__image_path:
            self.__count[img] = len(self.__image_path[img])
            count += self.__count[img]
        return count

    # 获取图片数量字典形式
    def ImageCountDict(self)->dict:
        return self.__count

    # 从图片路径中获取编号
    def imageToNumber(self,img_path:str)->str:
        n = re.findall(r'\d+_',img_path)[0]
        return str(int(n.replace("_","")))

    # 通过编号获取图片路径
    def numberToImage(self,number:str)->str:
        for v,k in self.__image_path.items():
            for img in k:
                if self.imageToNumber(img) == number:
                    return os.path.join(v,img)
        return ""

    def getImageALl(self):
        for v,k in self.__image_path.items():
            for img in k:
                yield os.path.join(v,img)

    # 显示图片
    def showImage(self,number:str):
        n =self.numberToImage(number)
        if n:
            img = Image.open(n)
            img.show()
        else:
            raise Exception("编号不存在")


# 比较图片类
class CompareImage:
    def __init__(self):
        pass

    def compare(self,img:Jpg,err_template_img:Jpg):
        for img_path in img.getImageALl():
            img = cv2.imread(img_path)
            acq_list = [] # 相识值列表
            for t in err_template_img.getImageALl():
                # 具体比较图片相识算法
                pass

if __name__ == '__main__':
    # err_img = cv2.imread(r"D:\code\LookM\core\Jpg\error_template\7.jpg")
    # 读入原始图像
    origineImage = cv2.imread(r"D:\code\LookM\core\Jpg\error_template\7.jpg")
    # 图像灰度化
    image = cv2.cvtColor(origineImage, cv2.COLOR_BGR2GRAY)
    # 将图片二值化
    retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    print(retval)
    cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('binary', img)

    cv2.waitKey()



    # j = CompareImage()
    #
    # jpg = Jpg()
    # err_jpg = Jpg()
    # # 添加图片读取目录
    # jpg.addImageReadFolder([r"D:\lookm\1",r"D:\lookm\2"])
    # err_jpg.addImageReadFolder([r"D:\code\LookM\core\Jpg\error_template"])
    # # 加载图片
    # jpg.loadImage()
    # err_jpg.loadImage()
    #
    # j.compare(jpg, err_jpg)

    r'''
        D:\lookm\1\067_41-80.jpg  --> 错误图片
        D:\lookm\1\046_41-80.jpg  --> 正常图片
        (4, 26, 1868, 1078) # 不同
        
        D:\lookm\1\067_41-80.jpg  --> 相同错误图片
        D:\lookm\1\067_41-80.jpg  --> 相同错误图片
        None # 相同
        
        D:\lookm\1\067_41-80.jpg  --> 不同错误图片
        D:\lookm\2\133_121-160.jpg  --> 不同错误图片
        (3, 7, 1881, 1054)
    '''
    # while True:
    #     pass