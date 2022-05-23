# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
from ast import Del
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys
import pycharts_3D
from time import strftime
from time import gmtime
import LocalSearch as LS
from Logger import Logger
from mpl_toolkits.mplot3d import Axes3D
# pyecharts-0.1.9.4 版本也可以画


# 读取矩阵文件,两个目标函数，Q有两个矩阵,返回两个矩阵
def Read_Matrix_file(path):
    Q = []
    with open(path, 'r') as f:
        for line in f:
            w = line.split(" ")
            Q.append([int(w[0]), int(w[2]), int(w[4])])
    log.logger.info("成功加载矩阵文件")
    return Q

# 根据Q返回q1，q2


def ReturnMatrix(Q):
    q1 = []
    q2 = []
    q3 = []
    n = int(np.sqrt(len(Q)))
    for i in range(n):
        a = []
        b = []
        c = []
        for j in range(i, len(Q), n):
            a.append(Q[j][0])
            b.append(Q[j][1])
            c.append(Q[j][2])
        q1.append(a)
        q2.append(b)
        q3.append(c)
    return q1, q2, q3

# 读取权重文件，并返回


def Read_Weight(path):
    log.logger.info("成功读取权重文件")
    return np.loadtxt(path)

# 只有一个决策向量，随机生成n个决策变量，决策变量为{0,1},如[0,1,0,1,1,1......1]


def Create_Decision_Vector(n):
    return np.random.randint(0, 2, n)
# 矩阵乘以决策向量X


def Matrix_X(X, q1, q2, q3):
    sum1, sum2, sum3 = 0, 0, 0
    n = len(X)  # n*n的矩阵
    for i in range(n):
        for j in range(n):
            sum1 += q1[i][j] * X[i] * X[j]
            sum2 += q2[i][j] * X[i] * X[j]
            sum3 += q3[i][j] * X[i] * X[j]
    return sum1, sum2, sum3


class Individual():
    '''
    X  决策向量
    W  权重向量
    Q  两个矩阵的格式
    '''

    def __init__(self, X, W, q1, q2, q3):
        # 决策向量
        self.X = X
        self.W = W
        self.f1, self.f2, self.f3 = Matrix_X(X, q1, q2, q3)
        self.f = [self.f1, self.f2, self.f3]
        self.F = self.W[0] * self.f1 + self.W[1] * \
            self.f2 + self.W[2] * self.f3,


def Init(N, W, n, q1, q2, q3):
    '''
    初始化种群P,产生N个个体
    '''
    P = []
    for i in range(N):
        X = Create_Decision_Vector(n)
        P.append(Individual(X, W[i], q1, q2, q3))
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
                (weights[i][0] - weights[j][0]) ** 2 + (weights[i][1] - weights[j][1]) ** 2+(weights[i][2] - weights[j][2]) ** 2)
            temp.append(distance)
        l = np.argsort(temp)  # 将列表从小到大排序，并返回排序后的下标
        B.append(l[:T])  # 每个个体都有最近T(领域规模)个权重向量
    log.logger.info("成功计算出{}个邻居".format(T))
    return B


def Draw(EP, name):
    plt.cla()
    x, y, z = [], [], []
    for i in range(len(EP)):
        x.append(EP[i].f1)
        y.append(EP[i].f2)
        z.append(EP[i].f3)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, marker='o')
    ax.set_zlabel('f3', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('f2', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('f1', fontdict={'size': 15, 'color': 'red'})
    ax.set_title(name)
    plt.pause(0.1)
    return x, y, z


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


# def UpdateEP(off, EP):
#     # 从EP中移除被y支配的解和相同的解
#     for p in EP[::-1]:
#         if Dominate(off, p) == 1 or off.f == p.f:
#             EP.remove(p)
#     # 如果y都不被EP中的解支配，则加入EP
#     flag = True
#     for k in range(len(EP)):
#         if Dominate(EP[k], off) == True:
#             flag = False
#             break
#     if flag == True:
#         EP.append(off)
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
        F = P[B[i][j]].W[0] * y.f1 + P[B[i][j]].W[1] * \
            y.f2 + P[B[i][j]].W[2] * y.f3
        if F > P[B[i][j]].F:
            # 用y的决策向量更新邻居的决策向量
            P[B[i][j]].F = F
            P[B[i][j]].X = y.X


def cross_mutation(parent1, parent2, W, Pc, Pm, q1, q2, q3):
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
    return Individual(X, W, q1, q2, q3)


def Formula(FlipIndex, X, q):
    sum = 0
    n = len(X)
    for j in range(n):
        if j != FlipIndex:
            sum += (q[FlipIndex][j] + q[j][FlipIndex]) * X[j]
    return (1 - 2 * X[FlipIndex]) * (sum + q[FlipIndex][FlipIndex])


def InitDeltaC(X, q1, q2, q3):
    DeltaC1, DeltaC2, DeltaC3 = [], [], []
    n = len(X)
    for j in range(n):
        DeltaC1.append(Formula(j, X, q1))
        DeltaC2.append(Formula(j, X, q2))
        DeltaC3.append(Formula(j, X, q3))
    return DeltaC1, DeltaC2, DeltaC3


def UpdateDeltaC(X, j, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3):
    n = len(X)
    for i in range(n):
        if i == j:
            DeltaC1[i] = - DeltaC1[i]
            DeltaC2[i] = - DeltaC2[i]
            DeltaC3[i] = - DeltaC3[i]
        else:
            DeltaC1[i] -= (q1[i][j] + q1[j][i]) * \
                (1 - 2 * X[i]) * (1 - 2 * X[j])
            DeltaC2[i] -= (q2[i][j] + q2[j][i]) * \
                (1 - 2 * X[i]) * (1 - 2 * X[j])
            DeltaC3[i] -= (q3[i][j] + q3[j][i]) * \
                (1 - 2 * X[i]) * (1 - 2 * X[j])


def JudgeTaboo(TaboList, i):
    # 变量对应禁忌表位置的禁忌时间==0时赦免
    if TaboList[i] == 0:
        return False
    else:
        return True


def JoinTaboList(TaboList, r, Length):
    '''将Xr加入禁忌表'''
    TaboList[r] = Length


def UpdateTaboList(TaboList):
    for i in range(len(TaboList)):
        '''禁忌长度不为0,则为被禁忌对象,更新禁忌长度'''
        if TaboList[i] != 0:
            TaboList[i] -= 1


def TabuSearch(parent, Maxdepth, Length, q1, q2, q3):
    n = len(parent.X)
    TaboList = np.zeros(n)  # 初始化时禁忌长度为0
    DeltaC1, DeltaC2, DeltaC3 = InitDeltaC(parent.X, q1, q2, q3)
    bestF = parent.F
    bestX = parent.X.copy()
    curX = parent.X.copy()
    curf = parent.f
    depth = 1
    F = []

    while(depth <= Maxdepth):
        flipindex = n
        DeltaC = sys.maxsize * -1
        for i in range(n):
            off_f1 = curf[0] + DeltaC1[i]
            off_f2 = curf[1] + DeltaC2[i]
            off_f3 = curf[2] + DeltaC3[i]
            offF = off_f1 * parent.W[0] + off_f2 * \
                parent.W[1] + off_f3 * parent.W[2]
            # 找到邻域内最好解(不管是否禁忌)或未被禁忌次优解的索引
            if(JudgeTaboo(TaboList, i) == False):
                if offF > DeltaC:
                    DeltaC = offF
                    flipindex = i
            else:
                if offF > bestF:
                    flipindex = i
                    break
        off_f1 = curf[0] + DeltaC1[flipindex]
        off_f2 = curf[1] + DeltaC2[flipindex]
        off_f3 = curf[2] + DeltaC3[flipindex]
        offF = off_f1 * parent.W[0] + off_f2 * \
            parent.W[1] + off_f3 * parent.W[2]
        curf = [off_f1, off_f2, off_f3]
        curX[flipindex] = 1 - curX[flipindex]
        UpdateTaboList(TaboList)
        JoinTaboList(TaboList, flipindex, Length)
        UpdateDeltaC(curX, flipindex, q1, q2, q3, DeltaC1, DeltaC2, DeltaC3)
        F.append(offF)
        if offF > bestF:
            bestF = offF
            bestX = curX.copy()
        depth += 1
    return Individual(bestX, parent.W, q1, q2, q3)


def LocalSearch(parent, MaxDepth, q1, q2, q3):
    depth = 0
    curF = parent.F
    curf = parent.f
    tempX = parent.X
    bestX = parent.X
    DeltaC1, DeltaC2, DeltaC3 = InitDeltaC(parent.X, q1, q2, q3)
    while(depth < MaxDepth):
        flipindex = 0
        '''直到找到一个好邻居为止'''
        while(flipindex < len(tempX)):
            '''通过公式计算翻转后的F,降低时间复杂度,temp并还没有修改'''
            off_f1 = curf[0] + DeltaC1[flipindex]
            off_f2 = curf[1] + DeltaC2[flipindex]
            off_f3 = curf[2] + DeltaC3[flipindex]
            offF = off_f1 * parent.W[0] + off_f2 * \
                parent.W[1] + off_f3 * parent.W[2]
            if offF > curF:
                curF = offF
                curf = [off_f1, off_f2, off_f3]
                tempX[flipindex] = 1 - tempX[flipindex]
                UpdateDeltaC(tempX, flipindex, q1, q2, q3,
                             DeltaC1, DeltaC2, DeltaC3)
                bestX = tempX
                break
            flipindex += 1
        depth += 1
    return Individual(bestX, parent.W, q1, q2, q3)


def Evolution(Max_Gen, SearchMethod, SearchDepth, P, B, N, T, Pc, Pm, EP, PhotoName, T1, q1, q2, q3):
    gen = 1
    while(gen <= Max_Gen):
        for i in range(N):
            # 交叉变异
            k = np.random.randint(T)
            l = np.random.randint(T)
            '''产生一个后代的后续处理方法'''
            y = cross_mutation(P[B[i][k]], P[B[i][l]],
                               P[i].W, Pc, Pm, q1, q2, q3)

            if SearchMethod == 0:
                UpdateEP(y, EP)
                UpdateDomain(y, i, T, P)
            elif SearchMethod == 1:
                y1 = LocalSearch(y, SearchDepth, q1, q2, q3)
                UpdateEP(y1, EP)
                UpdateDomain(y1, i, T, P)
            else:
                y1 = TabuSearch(y, SearchDepth, int(SearchDepth/5), q1, q2, q3)
                UpdateEP(y1, EP)
                UpdateDomain(y1, i, T, P)

        Draw(EP, "Number {} Gen , EP Size {}".format(
            str(gen), len(EP)))
        log.logger.info("已耗时:{} 已进化{}代".format(
            strftime("%H:%M:%S", gmtime(round(time.time()-T1))), gen))
        if gen == Max_Gen:
            plt.cla()
            x, y, z = Draw(EP, "Number {} Gen , EP Size {}".format(
                str(gen), len(EP)))
            plt.pause(0.1)
            points = []
            for i in range(len(x)):
                points.append([x[i], y[i], z[i]])
            log.logger.info(points)
            pycharts_3D.PychartsDraw(x, y, z, PhotoName)
            plt.savefig(PhotoName)
        gen += 1


if __name__ == "__main__":
    try:
        n = 50                 # 决策向量个数
        occ = "-0.2"            # 相关系数
        m = 3                   # 目标数量
        Pc = 1                  # 交叉概率
        Pm = 0.01               # 变异概率
        Max_Gen = 100           # 最大进化代数
        T = 5                   # 邻居个数
        EP = []                 # 精英群体
        SearchMethod = 2        # 0:不使用搜索方法 1:使用局部搜索 2:使用禁忌搜索
        SearchDepth = 10        # 搜索深度
        '''-------------------------------------------------------------------'''
        QName = "../../instances/mubqp_-0.2_3_{}_0.8_0.dat".format(n)
        WName = "../../instances/weight_m=3.txt"
        PhotoName = "{}{}_{}_{}_{}_{}_{}".format(
            "./", occ, m, n, Pm, Max_Gen, SearchMethod)
        LogName = "{}{}_{}_{}_{}_{}_{}.log".format(
            "./", occ, m, n, Pm, Max_Gen, SearchMethod)
        if os.path.exists(LogName):
            # 日志模块,默认模式为追加写入，所以需要删除
            os.remove(LogName)
            print("存在{},已删除".format(LogName))
        log = Logger(LogName, level='info')
        EP = []             # 精英群体
        T1 = time.time()
        Q = Read_Matrix_file(QName)
        q1, q2, q3 = ReturnMatrix(Q)
        Weights = Read_Weight(WName)
        N = len(Weights)  # 种群大小
        P = Init(N, Weights, n, q1, q2, q3)
        B = Neighbor(Weights, T)
        Evolution(Max_Gen, SearchMethod, SearchDepth, P, B, N, T, Pc, Pm, EP,
                PhotoName, T1, q1, q2, q3)
        T2 = time.time()
        log.logger.info("耗时:{}".format(
            strftime("%H:%M:%S", gmtime(round(T2-T1)))))
        log.logger.info("交叉概率:{} 变异概率:{} 最大进化代数:{} 邻居个数:{} 精英个数:{}".format(
            Pc, Pm, Max_Gen, T, len(EP)))
    except Exception as err:
        log.logger.error(err)
