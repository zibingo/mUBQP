# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
import numpy as np
import matplotlib.pyplot as plt
import time
import logging
import os
from logging import handlers
from time import strftime
from time import gmtime
import LocalSearch as LS
import TabuSearch as TS


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(levelname)s: %(message)s'):
        # def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(
            filename=filename, when=when, backupCount=backCount, encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

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

    def __init__(self, X, q1, q2):
        # 决策向量
        self.X = X
        self.nnd = 0
        self.paretorank = 0
        self.f1, self.f2 = Matrix_X(X, q1, q2)
        self.f = [self.f1, self.f2]
        self.F = self.f1 + self.f2


def Init(N, n, q1, q2):
    '''
    初始化种群P,产生N个个体
    '''
    P = []
    for i in range(N):
        X = Create_Decision_Vector(n)
        P.append(Individual(X, q1, q2))
    log.logger.info("成功初始化种群")
    return P


def Fast_NonDominate_Sort(N, P):
    F = {}
    pareto_rank = 1
    F[pareto_rank] = []
    Pn = {}
    Ps = {}
    for i in range(N):
        Pn[i] = 0  # 被支配个人数目
        Ps[i] = []  # 支配解得集合
        # 计算Pn,Ps
        for j in range(N):
            l, e, h = 0, 0, 0
            for k in range(2):
                if P[i].f[k] < P[j].f[k]:
                    h += 1
                elif P[i].f[k] == P[j].f[k]:
                    e += 1
                else:
                    l += 1
            if h == 0 and e != 2:
                Ps[i].append(j)
            elif l == 0 and e != 2:
                Pn[i] += 1
        if Pn[i] == 0:  # 如果它不被任何人支配，则为第一前沿面的个体
            P[i].paretorank = 1
            F[pareto_rank].append(i)
    # 求pareto等级为pareto_rank+1的个体
    while (len(F[pareto_rank]) != 0):
        temp = []  # pareto等级为pareto_rank的集合
        for i in range(len(F[pareto_rank])):
            if (len(Ps[F[pareto_rank][i]]) != 0):
                for j in range(len(Ps[F[pareto_rank][i]])):
                    Pn[Ps[F[pareto_rank][i]][j]] -= 1  # nl=nl-1
                    if Pn[Ps[F[pareto_rank][i]][j]] == 0:
                        P[Ps[F[pareto_rank][i]][j]
                          ].paretorank = pareto_rank+1  # 储存个体的等级信息
                        temp.append(Ps[F[pareto_rank][i]][j])
        pareto_rank = pareto_rank+1
        F[pareto_rank] = temp
    return F, P


def Crowding_Distance_Sort(F, Non_P):
    # 计算拥挤度
    ppp = []
    # 按照pareto等级对种群中的个体进行排序
    # 按照pareto等级排序后种群
    temp = sorted(Non_P, key=lambda Individual: Individual.paretorank)
    index1 = []
    # 保存temp中个体在chromo_non中的索引
    for i in range(len(temp)):
        index1.append(Non_P.index(temp[i]))
    # 对于每个等级的个体开始计算拥挤度
    current_index = 0
    for pareto_rank in range(len(F)-1):  # 计算F的循环时多了一次空，所以减掉,由于pareto从1开始，再减一次
        nd = np.zeros(len(F[pareto_rank+1]))  # 拥挤度初始化为0
        y = []  # 储存当前处理的等级的个体
        yF = np.zeros((len(F[pareto_rank+1]), 2))  # len()行f_num列的二维矩阵
        for i in range(len(F[pareto_rank+1])):
            y.append(temp[current_index + i])
        current_index += i
        # 对于每一个目标函数fm
        for i in range(2):
            # 根据该目标函数值对该等级的个体进行排序
            index_objective = []  # 通过目标函数排序后的个体索引
            objective_sort = sorted(
                y, key=lambda Individual: Individual.f[i])  # 通过目标函数排序后的个体
            for j in range(len(objective_sort)):
                index_objective.append(y.index(objective_sort[j]))
            # 记fmax为最大值，fmin为最小值
            fmin = objective_sort[0].f[i]
            fmax = objective_sort[len(objective_sort)-1].f[i]
            # 对排序后的两个边界拥挤度设为1d和nd设为无穷
            yF[index_objective[0]][i] = float("inf")
            yF[index_objective[len(index_objective)-1]][i] = float("inf")
            # 计算nd=nd+(fm(i+1)-fm(i-1))/(fmax-fmin)
            j = 1
            # 计算除了边界两点的拥挤度
            while (j <= (len(index_objective)-2)):
                pre_f = objective_sort[j-1].f[i]
                next_f = objective_sort[j+1].f[i]
                if (fmax-fmin == 0):
                    yF[index_objective[j]][i] = float("inf")
                else:
                    yF[index_objective[j]][i] = float(
                        (next_f-pre_f)/(fmax-fmin))
                j = j+1
        # 多个目标函数拥挤度求和
        nd = np.sum(yF, axis=1)  # 每行相加
        for i in range(len(y)):
            y[i].nnd = nd[i]
            ppp.append(y[i])
    return ppp


def cross_mutation(parent1, parent2, Pc, Pm, q1, q2):
    '''
    交叉变异
    '''
    X = []
    n = len(parent1.X)
    # 均匀交叉
    if np.random.random() < Pc:
        for i in range(n):
            model = Create_Decision_Vector(n)
            if model[i] == 1:
                X.append(parent1.X[i])
            else:
                X.append(parent2.X[i])

    # 基因突变
    # 整个基因序列翻转
    for i in range(n):
        if np.random.random() < Pm:
            X[i] = 1 - X[i]

    return Individual(X, q1, q2)


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
    plt.pause(0.5)
    return x, y


def elitism(N, combine_chromo2):
    chromo = []
    index1 = 0
    index2 = 0
    # 根据pareto等级从高到低进行排序
    chromo_rank = sorted(
        combine_chromo2, key=lambda Individual: Individual.paretorank)
    flag = chromo_rank[N-1].paretorank
    # 取paretorank为1到flag-1的个体进种群
    for i in range(len(chromo_rank)):
        if (chromo_rank[i].paretorank == (flag)):
            index1 = i
            break
        else:
            chromo.append(chromo_rank[i])
    # 计算paretorank为flag+1的第一个个体位置
    for i in range(len(chromo_rank)):
        if (chromo_rank[i].paretorank == (flag+1)):
            index2 = i
            break
    c = 0
    for p in chromo_rank:
        if p.paretorank == 1:
            c += 1
    temp = []
    aaa = index1
    if (index2 == 0):
        index2 = len(chromo_rank)
    # index1到index2的个体根据拥挤度从大到小排序，取前N-index1数量的个体加入种群
    while (aaa < index2):
        temp.append(chromo_rank[aaa])
        aaa = aaa+1
    # 从小到大排序
    temp_crowd = sorted(
        temp, key=lambda Individual: Individual.nnd, reverse=True)
    remainN = N-index1
    for i in range(remainN):
        chromo.append(temp_crowd[i])
    return chromo


def Evolution(Max_Gen, SearchMethod, SearchDepth, chromo, N, Pc, Pm, q1, q2, T1, PhotoName):
    gen = 1
    while(gen <= Max_Gen):
        chromo_offspring = []

        for i in range(N):
            parent1 = np.random.choice(chromo)
            parent2 = np.random.choice(chromo)
            off = cross_mutation(parent1, parent2, Pc, Pm, q1, q2)
            if SearchMethod == 0:
                chromo_offspring.append(off)
            elif SearchMethod == 1:
                off1 = LS.LocalSearch(off, SearchDepth, q1, q2)
                chromo_offspring.append(off1)
            else:
                off1 = TS.TabuSearch(
                    off, SearchDepth, int(SearchDepth/5), q1, q2)
                chromo_offspring.append(off1)
        '''
        精英保留策略
        '''
        # 将父代和子代合并
        combine_chromo = chromo + chromo_offspring
        # 快速非支配排序
        F2, combine_chromo1 = Fast_NonDominate_Sort(
            len(combine_chromo), combine_chromo)
        # 计算拥挤度进行排序
        combine_chromo2 = Crowding_Distance_Sort(F2, combine_chromo1)
        # 精英保留产生下一代种群
        chromo = elitism(N, combine_chromo2)

        log.logger.info("已耗时:{} 已进化{}代".format(
            strftime("%H:%M:%S", gmtime(round(time.time()-T1))), gen))
        Draw(chromo, "Number {} Gen , EP Size {}".format(
            str(gen), len(chromo)))

        if gen == Max_Gen:
            x, y = Draw(chromo, "Number {} Gen , EP Size {}".format(
                str(gen), len(chromo)))
            points = []
            for i in range(len(x)):
                points.append([x[i], y[i]])
            log.logger.info(points)
            plt.savefig(PhotoName+".jpeg")
        gen += 1
    return chromo


if __name__ == "__main__":
    n = 50                  # 决策向量个数
    occ = "-0.2"            # 相关系数
    m = 2                   # 目标数量
    Pc = 1                  # 交叉概率
    Pm = 0.01               # 变异概率
    Max_Gen = 100            # 最大进化代数
    N = 100                 # 种群数量
    EP = []                 # 精英群体
    SearchMethod = 0        # 0:不使用搜索方法 1:使用局部搜索 2:使用禁忌搜索
    SearchDepth = 10        # 搜索深度
    '''---------------------------------------------------------------'''
    QName = "../instances/mubqp_-0.2_2_{}_0.8_0.dat".format(n)
    PhotoName = "{}{}_{}_{}_{}_{}_{}".format(
        "./", occ, m, n, Pm, Max_Gen, SearchMethod)
    LogName = "{}{}_{}_{}_{}_{}_{}.log".format(
        "./", occ, m, n, Pm, Max_Gen, SearchMethod)
    if os.path.exists(LogName):
        # 日志模块,默认模式为追加写入，所以需要删除
        os.remove(LogName)
        print("存在{}，已删除".format(LogName))
    log = Logger(LogName, level='info')
    T1 = time.time()
    Q = Read_Matrix_file(QName)
    q1, q2 = ReturnMatrix(Q)
    P = Init(N, n, q1, q2)
    F1, Non_P = Fast_NonDominate_Sort(N, P)
    chromo = Crowding_Distance_Sort(F1, Non_P)
    EP = Evolution(Max_Gen, SearchMethod, SearchDepth, chromo, N, Pc,
                   Pm, q1, q2, T1, PhotoName)
