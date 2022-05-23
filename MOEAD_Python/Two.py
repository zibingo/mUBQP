# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from time import strftime
from time import gmtime
import TabuSearch as TS
import LocalSearch as LS
from Logger import Logger

# 读取矩阵文件,两个目标函数，Q有两个矩阵,返回两个矩阵


def Read_Matrix_file(path):
    Q = []
    with open(path, 'r') as f:
        for line in f:
            w = line.split(" ")
            Q.append([int(w[0]), int(w[2])])
    log.logger.info("成功加载矩阵文件")
    return Q

# 根据Q返回q1，q2


def ReturnMatrix(Q):
    q1 = []
    q2 = []
    n = int(np.sqrt(len(Q)))
    for i in range(n):
        a = []
        b = []
        for j in range(i, len(Q), n):
            a.append(Q[j][0])
            b.append(Q[j][1])
        q1.append(a)
        q2.append(b)
    return q1, q2

# 读取权重文件，并返回


def Read_Weight(path):
    log.logger.info("成功读取权重文件")
    return np.loadtxt(path)

# 只有一个决策向量，随机生成n个决策变量，决策变量为{0,1},如[0,1,0,1,1,1......1]


def Create_Decision_Vector(n):
    return np.random.randint(0, 2, n)

# 矩阵乘以决策向量X


def Matrix_X(X, q1, q2):
    sum1, sum2 = 0, 0
    n = len(X)  # n*n的矩阵
    for i in range(n):
        for j in range(n):
            sum1 += q1[i][j] * X[i] * X[j]
            sum2 += q2[i][j] * X[i] * X[j]
    return sum1, sum2


class Individual():
    '''
    X  决策向量
    W  权重向量
    Q  两个矩阵的格式
    '''

    def __init__(self, X, W, q1, q2):
        # 决策向量
        self.X = X.copy()
        self.W = W
        self.f1, self.f2 = Matrix_X(X, q1, q2)
        self.f = [self.f1, self.f2]
        self.F = self.W[0] * self.f1 + self.W[1] * self.f2


def Init(N, W, n, q1, q2):
    '''
    初始化种群P,产生N个个体
    '''
    P = []
    for i in range(N):
        X = Create_Decision_Vector(n)
        P.append(Individual(X, W[i], q1, q2))
    log.logger.info("成功初始化种群")
    return P


def Neighbor(weights, T):
    '''
    返回权重向量最近的T个邻居
    '''
    B = []
    N = len(weights)
    for i in range(N):
        temp = []
        for j in range(N):
            distance = np.sqrt(
                (weights[i][0] - weights[j][0]) ** 2 + (weights[i][1] - weights[j][1]) ** 2)
            temp.append(distance)
        l = np.argsort(temp)  # 将列表从小到大排序，并返回排序后的下标
        B.append(l[:T])  # 每个个体都有最近T(领域规模)个权重向量
    log.logger.info("成功计算出{}个邻居".format(T))
    return B


def Draw(EP, name):
    plt.cla()
    x, y = [], []
    for i in range(len(EP)):
        x.append(EP[i].f1)
        y.append(EP[i].f2)
    plt.scatter(x, y, marker='o')
    plt.xlabel("f1")
    plt.ylabel("f2")
    plt.title(name)
    plt.pause(0.1)
    return x, y

# 比较y1，y2的支配关系


def Dominate(y1, y2):
    low, equal, high = 0, 0, 0
    m = len(y1.f)
    for i in range(m):
        if y1.f[i] < y2.f[i]:
            high += 1
        elif y1.f[i] == y2.f[i]:
            equal += 1
        else:
            low += 1
    if high == 0 and equal != m:       # y1.f 支配 y2.f
        return 1
    elif low == 0 and equal != m:  # y2.f 支配 y1.f
        return 0
    elif equal == m:
        return -2            # y1.f == y2.f
    else:
        return -1           # y2.f 、 y1.f都是非支配解


def cross_mutation(parent1, parent2, W, Pc, Pm, q1, q2):
    '''
    交叉变异,产生一个后代
    '''
    # 均匀交叉
    X = []
    n = len(parent1.X)
    if np.random.random() < Pc:
        model = Create_Decision_Vector(n)
        for i in range(n):
            if model[i] == 1:
                X.append(parent1.X[i])
            else:
                X.append(parent2.X[i])

    # 基因突变
    # 整个基因序列翻转
    for i in range(n):
        if np.random.random() < Pm:
            X[i] = 1 - X[i]
    return Individual(X, W, q1, q2)


def UpdateEP(off, EP):
    # 从EP中移除被p支配的解和相同的解
    flag = True
    for p in EP[::-1]:
        res = Dominate(off, p)
        if res == 1 or res == -2:
            EP.remove(p)
        if res == 0:
            flag = False
    if flag == True:
        EP.append(off)


def UpdateDomain(y, i, T, P):
    # 更新领域解
    for j in range(T):
        '''
        如果产生的后代个体的F大于当前个体的邻居的F,则更新
        '''
        F = P[B[i][j]].W[0] * y.f1 + P[B[i][j]].W[1] * y.f2
        if F > P[B[i][j]].F:
            # 用y的决策向量更新邻居的决策向量
            P[B[i][j]].F = F
            P[B[i][j]].X = y.X


def Evolution(Max_Gen, SearchMethod, SearchDepth, P, B, N, T, Pc, Pm, EP, PhotoName, T1, q1, q2):
    gen = 1
    while(gen <= Max_Gen):
        for i in range(N):
            # 交叉变异
            k = np.random.randint(T)
            l = np.random.randint(T)
            '''产生一个后代的后续处理方法'''
            y = cross_mutation(P[B[i][k]], P[B[i][l]],
                               P[i].W, Pc, Pm, q1, q2)
            if SearchMethod == 0:
                UpdateEP(y, EP)
                UpdateDomain(y, i, T, P)
            elif SearchMethod == 1:
                y1 = LS.LocalSearch(y, SearchDepth, q1, q2)
                UpdateEP(y1, EP)
                UpdateDomain(y1, i, T, P)
            else:
                y1 = TS.TabuSearch(y, SearchDepth, int(SearchDepth/5), q1, q2)
                UpdateEP(y1, EP)
                UpdateDomain(y1, i, T, P)
        Draw(EP, "Number {} Gen , EP Size {}".format(
            str(gen), len(EP)))
        log.logger.info("已耗时:{} 已进化{}代".format(
            strftime("%H:%M:%S", gmtime(round(time.time()-T1))), gen))
        if gen == Max_Gen:
            x, y = Draw(EP, "Number {} Gen , EP Size {}".format(
                str(gen), len(EP)))
            points = []
            for i in range(len(x)):
                points.append([x[i], y[i]])
            log.logger.info(points)
            plt.savefig(PhotoName+".jpeg", dpi=500, bbox_inches='tight')
        gen += 1


if __name__ == "__main__":
    '''---------------------------------------------------------------'''
    n = 50                  # 决策向量个数
    occ = "-0.2"            # 相关系数
    m = 2                   # 目标数量
    Pc = 1                  # 交叉概率
    Pm = 0.01               # 变异概率
    Max_Gen = 100           # 最大进化代数
    T = 5                   # 邻居个数
    EP = []                 # 精英群体
    SearchMethod = 0        # 0:不使用搜索方法 1:使用局部搜索 2:使用禁忌搜索
    SearchDepth = 10        # 搜索深度
    '''---------------------------------------------------------------'''
    QName = "../instances/mubqp_{}_2_{}_0.8_0.dat".format(occ,n)
    WName = "../instances/weight_m=2.txt"

    PhotoName = "{}{}_{}_{}_{}_{}_{}".format(
        "./", occ, m, n, Pm, Max_Gen, SearchMethod)
    LogName = "{}{}_{}_{}_{}_{}_{}.log".format(
        "./", occ, m, n, Pm, Max_Gen, SearchMethod)
    if os.path.exists(LogName):
        # 日志模块,默认模式为追加写入，所以需要删除
        os.remove(LogName)
        print("存在{},已删除".format(LogName))
    log = Logger(LogName, level='info')
    T1 = time.time()
    Q = Read_Matrix_file(QName)
    q1, q2 = ReturnMatrix(Q)
    Weights = Read_Weight(WName)
    N = len(Weights)  # 种群大小
    P = Init(N, Weights, n, q1, q2)
    B = Neighbor(Weights, T)
    Evolution(Max_Gen, SearchMethod, SearchDepth, P, B, N, T, Pc, Pm, EP,
              PhotoName, T1, q1, q2)
    T2 = time.time()
    log.logger.info("耗时:{}".format(
        strftime("%H:%M:%S", gmtime(round(T2-T1)))))
    log.logger.info("交叉概率:{} 变异概率:{} 最大进化代数:{} 邻居个数:{} 精英个数:{}".format(
        Pc, Pm, Max_Gen, T, len(EP)))
