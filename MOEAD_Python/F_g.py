# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
'''领域解选择图像'''
import matplotlib.pyplot as plt
import numpy as np


def Draw(Maxdepth, Y):
    X = np.arange(0, Maxdepth, 1)
    plt.cla()
    plt.scatter(X, Y, marker='.', s=5)
    plt.xlabel("gen")
    plt.ylabel("F")
    plt.title("F-gen")
    plt.pause(0.1)
    plt.savefig("F-g.jpeg", dpi=500, bbox_inches='tight')
