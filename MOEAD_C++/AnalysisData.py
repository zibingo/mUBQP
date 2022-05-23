# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
'''同一算法比较'''
import numpy as np
import hvwfg

Method = {
    0:"NonSearch",
    1:"LocalSearch",
    2:"TabuSearch"
}


def Normalization(data,Max_X_Y_Z,Min_X_Y_Z):
    '''归一化处理'''
    temp = []
    if len(data[0]) == 2:
        for d in data:
            '''最大化问题需要乘-1'''
            d = d*-1
            x = (d[0] - Min_X_Y_Z[0]) / (Max_X_Y_Z[0] - Min_X_Y_Z[0])
            y = (d[1] - Min_X_Y_Z[1]) / (Max_X_Y_Z[1] - Min_X_Y_Z[1])
            temp.append([x,y])
    else:
        for d in data:
            d = d*-1
            x = (d[0] - Min_X_Y_Z[0]) / (Max_X_Y_Z[0] - Min_X_Y_Z[0])
            y = (d[1] - Min_X_Y_Z[1]) / (Max_X_Y_Z[1] - Min_X_Y_Z[1])
            z = (d[2] - Min_X_Y_Z[2]) / (Max_X_Y_Z[2] - Min_X_Y_Z[2])
            temp.append([x,y,z])
    return temp

def Run(EPsPath,N,OCC,M,Pm,Max_Gen,Max_Run_Num,SearchMethod):
    MOEAD_path = EPsPath
    for n in N:
        for occ in OCC:
            for m in M:
                for p in Pm:
                    MOEAD_Sum = []
                    ref = [1.1,1.1] if m == 2 else [1.1,1.1,1.1]
                    #合并不同搜索方法运行求得解
                    for s in SearchMethod:
                        for i in range(1, Max_Run_Num+1):
                            MOEAD_Name = "{}{}_{}_{}_{}_{}_{}_{}.txt".format(
                                MOEAD_path, occ, m, n, p, Max_Gen, s,i)
                            a = np.loadtxt(MOEAD_Name)
                            for l in a:
                                MOEAD_Sum.append(l*-1)
                    #计算出不同搜索方法运行求得最大最小解
                    Max_X_Y_Z = list(np.amax(MOEAD_Sum,axis = 0))
                    Min_X_Y_Z = list(np.amin(MOEAD_Sum,axis = 0))
                    #存放所有运行结果的HV
                    MeanHV = []
                    for s in SearchMethod:
                        MOEAD_HV = []
                        for i in range(1, Max_Run_Num+1):
                            MOEAD_Name = "{}{}_{}_{}_{}_{}_{}_{}.txt".format(
                                MOEAD_path, occ, m, n, p, Max_Gen, s,i)
                            MOEAD_Sum_Nor = Normalization(np.loadtxt(MOEAD_Name),Max_X_Y_Z,Min_X_Y_Z)
                            MOEAD_HV.append(hvwfg.wfg(np.array(MOEAD_Sum_Nor),np.array(ref)))
                        MeanHV.append(np.mean(MOEAD_HV))
                    MeanHV = list(np.around(MeanHV,5))
                    temp = MeanHV.copy()
                    MeanHV.sort(reverse=True)
                    Rank = {}
                    for i in range(len(MeanHV)):
                        Rank[MeanHV[i]] = i + 1
                    print("----------------------------------------------------------------------")
                    for s in SearchMethod:
                        print("{:<5}\t{:<5}\t{:<5}\t{:<5}\t{:<12}\t{:<6}\t{:<2}".format(n,occ,m,p,Method[s],temp[s],Rank[temp[s]]))


                