# -*- coding: utf-8 -*-
import random
import copy
import time
import sys
import math
import threading
import numpy as np
from functools import reduce
from numpy import *

# 参数
'''
ALPHA:信息启发因子，值越大，则蚂蚁选择之前走过的路径可能性就越大
      ，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
BETA:Beta值越大，蚁群越就容易选择局部较短路径，这时算法收敛速度会
     加快，但是随机性不高，容易得到局部的相对最优
'''
(ALPHA, BETA, RHO, Q) = (1.0,2.0,0.5,100.0)

#边界
l1 = 10
parfum = [[1 for i in range(10)] for i in range(10)]
_Amap = []

#----------- 蚂蚁 -----------
class Ant(object):
    # 初始化
    def __init__(self):
        self.pStart = [0,0]
        self.pEnd = [5,9]
        self.pNow = [0,0]
        self._pNextNumber = 0
        self._next_step = [[0 for i in range(10)] for i in range(10)]
        self.path_x = []
        self.path_y = []
        self.tabooTable = [[0 for i in range(10)] for i in range(10)]
        self.walkLength = 0
        self.stateFlag = 0
    
    def _FindNext(self):                                            #找到下一步可能的格点
        x = self.pNow[0]                                          #取出蚂蚁当前坐标坐标
        y = self.pNow[1]
        self.tabooTable[x][y] = 1                                   #设置当前坐标已经走过
        for i in [x-1,x,x+1]:                                       #枚举周围的格点
            for j in [y-1,y,y+1]:
                if ((i>=0) and (i<10) and (j>=0) and (j<10)):         #边界判定
                    if self.tabooTable[i][j] == 0:                  #通路判定
                        self._next_step[self._pNextNumber][0] = i   #_pNext数组保存转移格点坐标
                        self._next_step[self._pNextNumber][1] = j 
                        self._pNextNumber = self._pNextNumber + 1   #_pNextNumber+1
    
    def _MoveToNext(self):
        pcum = []
        sum_pcum = 0
        for i in range(0,self._pNextNumber):                        #枚举下一步可以走的格点，用公式计算概率
            x1 = float(self._next_step[i][0])
            y1 = float(self._next_step[i][1])
            x2 = float(self.pEnd[0])
            y2 = float(self.pEnd[1])
            xx = parfum[self._next_step[i][0]][self._next_step[i][1]] / _distance(x1,y1,x2,y2)**8
            pcum.append(xx)
            sum_pcum = sum_pcum + xx

        temp_pcum = random.uniform(0.0,sum_pcum)
        picked = 0
        for i in range(0,self._pNextNumber):
            temp_pcum = temp_pcum - pcum[i]
            if temp_pcum < 0:
                picked = i
                break
        
        self.walkLength = self.walkLength + 1
        self.path_x.append(self.pNow[0])
        self.path_y.append(self.pNow[1])
        self.pNow[0] = self._next_step[picked][0]
        self.pNow[1] = self._next_step[picked][1]
        self._pNextNumber = 0
        self._pNext = [0,0]
        self._FindNext()
        if (self.pNow[0] == self.pEnd[0]) and (self.pNow[1] == self.pEnd[1]):
            self.stateFlag = 1
        if self._pNextNumber == 0:
            self.stateFlag = -1
    
#----------------距离公式-------------------
def _distance(x1,y1,x2,y2):
    _dis = math.sqrt((x1-x2)**2 + (y1 - y2)**2) + 0.1
    return _dis

#----------------计算最短路-------------------
#txt_path = 'E:\oppo杯\oppo杯\智慧安全疏散算法\2.txt'
#f = open(txt_path)
#data_lists = f.readlines()
#dataset = []

#for data in data_lists:
#    data1 = data.strip('\n')	# 去掉开头和结尾的换行符
#    data2 = data1.split('\t')	# 把tab作为间隔符
#    dataset.append(data2)	# 把这一行的结果作为元素加入列表dataset
#dataset = np.array(dataset)
#print(dataset)

#----------------计算最短路-------------------
for i in range(1,500):
    ant = Ant()
    ant._FindNext()
    while ant.stateFlag == 0:
        ant._MoveToNext()

    if ant.stateFlag == 1:
        for k in range(0,10):
            for j in range(0,10):
                parfum[k][j] = parfum[k][j] * 0.1

        for j in range(0,ant.walkLength):
            parfum[ant.path_x[j]][ant.path_y[j]] = parfum[ant.path_x[j]][ant.path_y[j]] + 1/ant.walkLength

        parfum[ant.pEnd[0]][ant.pEnd[1]] = parfum[ant.pEnd[0]][ant.pEnd[1]] + 1/ant.walkLength

for i in range(0,10):
    for j in range(0,10):
        print('%.2f'%parfum[i][j],end=' ')
    print('\n')