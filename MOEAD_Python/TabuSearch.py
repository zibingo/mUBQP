# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
import numpy as np
import Two
import sys
import F_g
import convergence


def Formula(FlipIndex, X, q):
    sum = 0
    n = len(X)
    for j in range(n):
        if j != FlipIndex:
            sum += (q[FlipIndex][j] + q[j][FlipIndex]) * X[j]
    return (1 - 2 * X[FlipIndex]) * (sum + q[FlipIndex][FlipIndex])


def InitDeltaC(X, q1, q2):
    DeltaC1, DeltaC2 = [], []
    n = len(X)
    for j in range(n):
        DeltaC1.append(Formula(j, X, q1))
        DeltaC2.append(Formula(j, X, q2))
    return DeltaC1, DeltaC2


def UpdateDeltaC(X, j, q1, q2, DeltaC1, DeltaC2):
    n = len(X)
    for i in range(n):
        if i == j:
            DeltaC1[i] = - DeltaC1[i]
            DeltaC2[i] = - DeltaC2[i]
        else:
            DeltaC1[i] -= (q1[i][j] + q1[j][i]) * \
                (1 - 2 * X[i]) * (1 - 2 * X[j])
            DeltaC2[i] -= (q2[i][j] + q2[j][i]) * \
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


def TabuSearch(parent, Maxdepth, Length, q1, q2):
    n = len(parent.X)
    TaboList = np.zeros(n)  # 初始化时禁忌长度为0
    DeltaC1, DeltaC2 = InitDeltaC(parent.X, q1, q2)
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
            offF = off_f1 * parent.W[0] + off_f2 * parent.W[1]
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
        offF = off_f1 * parent.W[0] + off_f2 * parent.W[1]
        curf = [off_f1, off_f2]
        curX[flipindex] = 1 - curX[flipindex]
        UpdateTaboList(TaboList)
        JoinTaboList(TaboList, flipindex, Length)
        UpdateDeltaC(curX, flipindex, q1, q2, DeltaC1, DeltaC2)
        F.append(offF)
        if offF > bestF:
            bestF = offF
            bestX = curX.copy()
        depth += 1
    # F_g.Draw(Maxdepth, F)
    # convergence.Draw(F)
    return Two.Individual(bestX, parent.W, q1, q2)
