# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
'''解的收敛图'''
import hvwfg
import numpy as np
import matplotlib.pyplot as plt


def Normalization(d, Max_X_Y_Z, Min_X_Y_Z):
    x = (d[0] - Min_X_Y_Z[0]) / (Max_X_Y_Z[0] - Min_X_Y_Z[0])
    y = (d[1] - Min_X_Y_Z[1]) / (Max_X_Y_Z[1] - Min_X_Y_Z[1])
    return [x, y]


def Draw(data):
    plt.cla()
    x, y = [], []
    for i in data:
        x.append(i[0])
        y.append(i[1])
    plt.scatter(x, y, s=5, color='black')
    plt.xlabel("f1")
    plt.ylabel("f2")
    plt.savefig("convergence.jpeg")
    plt.pause(1)
