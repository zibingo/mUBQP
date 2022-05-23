# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
import Two
import TabuSearch as TS
import convergence


def Dominate(f1, f2):
    low, equal, high = 0, 0, 0
    m = len(f1)
    for i in range(m):
        if f1[i] < f2[i]:
            high += 1
        elif f1[i] == f2[i]:
            equal += 1
        else:
            low += 1
    if high == 0 and equal != m:       # y1.f 支配 y2.f
        return 1
    elif low == 0 and equal != m:  # y2.f 不支配 y1.f
        return 0
    elif equal == m:
        return -2            # y1.f == y2.f
    else:
        return -1           # y2.f 、 y1.f都是非支配解


def LocalSearch(parent, MaxDepth, q1, q2):
    depth = 0
    curf = parent.f
    tempX = parent.X
    bestX = parent.X
    DeltaC1, DeltaC2 = TS.InitDeltaC(parent.X, q1, q2)
    F = []
    while(depth < MaxDepth):
        flipindex = 0
        '''直到找到一个好邻居为止'''
        while(flipindex < len(tempX)):
            '''通过公式计算翻转后的F,降低时间复杂度,temp并还没有修改'''
            off_f1 = curf[0] + DeltaC1[flipindex]
            off_f2 = curf[1] + DeltaC2[flipindex]
            off_f = [off_f1, off_f2]
            if Dominate(off_f, curf) == 1:
                curf = off_f
                tempX[flipindex] = 1 - tempX[flipindex]
                bestX = tempX
                TS.UpdateDeltaC(tempX, flipindex, q1, q2, DeltaC1, DeltaC2)
                F.append(off_f)
                break
            flipindex += 1
        depth += 1
    # convergence.Draw(F)
    return Two.Individual(bestX, q1, q2)
