# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
import Two
import TabuSearch as TS
import convergence


def LocalSearch(parent, MaxDepth, q1, q2):
    depth = 0
    curF = parent.F
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
            offF = off_f1 * parent.W[0] + off_f2 * parent.W[1]
            if offF > curF:
                curF = offF
                curf = [off_f1, off_f2]
                tempX[flipindex] = 1 - tempX[flipindex]
                TS.UpdateDeltaC(tempX, flipindex, q1, q2, DeltaC1, DeltaC2)
                bestX = tempX
                F.append(offF)
                break
            flipindex += 1
        depth += 1
    # convergence.Draw(F)
    return Two.Individual(bestX, parent.W, q1, q2)
