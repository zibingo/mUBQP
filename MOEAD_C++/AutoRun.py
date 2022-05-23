# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
import time
import datetime
from DrawPhoto import Draw_2D, Draw_3D
import os
import sys
from Logger import Logger
import AnalysisData
# 分析结果输出文件
sys.stdout = open('results.txt', mode='w', encoding='utf-8')

Cleardir = 0                     # 是否清空目录
PyechartsDraw2 = False           # m=2画图,使用Pyechart画图
PyechartsDraw3 = True            # m=3画图,使用Pyechart画图
SearchMethod = [0,1,2]           # 0:不使用搜索方法、1:局部搜索、2:禁忌搜索
M = [2,3]                        # 目标数量
OCC = [-0.2,0.0,0.2,0.5]         # 相关系数
N = [20,50,100,200,400,600,800]  # 决策向量个数
Pm = [0.01]                      # 变异概率
Max_Gen = 10                     # 进化次数
Max_Run_Num = 10                 # 最大运行次数
timesleep = 1

CppLogPath = "./logs/"           # C++后台运行的日志目录
EPsPath = "./EPs/"               # 每次运行保存的精英目录
PhotoPath = './photos/'          # EP图片文件夹
HtmlPath = "./HTML/"             # EP_HTML文件夹
PyLogName = "AutoRun.log"


def NewFilePath(log, CppLogPath, EPsPath, PhotoPath, HtmlPath):
    if os.path.exists(CppLogPath) == False:
        os.makedirs(CppLogPath)
        log.logger.info("不存在logs目录,已创建")
    if os.path.exists(EPsPath) == False:
        os.makedirs(EPsPath)
        log.logger.info("不存在EPs目录,已创建")
    if os.path.exists(PhotoPath) == False:
        os.makedirs(PhotoPath)
        log.logger.info("不存在Photos目录,已创建")
    if os.path.exists(HtmlPath) == False and (PyechartsDraw2 == True and (2 in M) or PyechartsDraw3 == True and (3 in M)):
        os.makedirs(HtmlPath)
        log.logger.info("不存在HTML目录,已创建")


def Run():
    if Cleardir == 1:
        os.system("sh Cleardir.sh")
    time.sleep(2)
    log = Logger(PyLogName, level='info')
    NewFilePath(log, CppLogPath, EPsPath, PhotoPath, HtmlPath)
    for m in M:
        for occ in OCC:
            for n in N:
                for p in Pm:
                    for s in SearchMethod:
                        for i in range(1, Max_Run_Num+1):
                            CppVar = "{} {} {} {} {} {}".format(
                                occ, n, p, Max_Gen, s, i)
                            CppLogName = "{}{}_{}_{}_{}_{}_{}_{}.log".format(
                                CppLogPath, occ, m, n, p, Max_Gen, s, i)
                            EpName = "{}{}_{}_{}_{}_{}_{}_{}.txt".format(
                                EPsPath, occ, m, n, p, Max_Gen, s, i)
                            PhotoName = "{}{}_{}_{}_{}_{}_{}_{}.jpeg".format(
                                PhotoPath, occ, m, n, p, Max_Gen, s, i)
                            HtmlName = "{}{}_{}_{}_{}_{}_{}_{}.html".format(
                                HtmlPath, occ, m, n, p, Max_Gen, s, i)
                            Command = "g++ m={}.cpp && nohup ./a.out {} {} {} > /dev/null 2> /dev/null &".format(
                                m, CppVar, CppLogName, EpName)
                            ''' 判断C++程序是否结束,EP.txt是否生成'''
                            if os.path.exists(EpName) == True:
                                log.logger.info("已存在{},已删除".format(EpName))
                                os.remove(EpName)
                            '''shell 执行命令'''
                            os.system(Command)
                            log.logger.info("正在执行命令 -> {}".format(Command))
                            while(os.path.exists(EpName) == False):
                                time.sleep(timesleep)
                            '''画图'''
                            if m == 2:
                                Draw_2D(EpName, PhotoName, HtmlName,
                                        occ, m, n, p, Max_Gen, i, PyechartsDraw2)
                            else:
                                Draw_3D(EpName, PhotoName, HtmlName,
                                        occ, m, n, p, Max_Gen, i, PyechartsDraw3)


if __name__ == "__main__":
    start = time.time()
    Run()
    print("------------------------------脚本运行完毕------------------------------")
    print("进化次数:{}\t运行次数:{}\t".format(Max_Gen, Max_Run_Num))
    print("----------------------------------------------------------------------")
    print("{:<5}\t{:<5}\t{:<5}\t{:<5}\t{:<12}\t{:<6}\t{:<2}".format(
        "n", "occ", "m", "Pm", "SearchMethod", "MeanHV", "Rank"))
    AnalysisData.Run(EPsPath, N, OCC, M, Pm, Max_Gen,
                     Max_Run_Num, SearchMethod)
    end = time.time()
    print("----------------------------------------------------------------------")
    print("此脚本总耗时:", datetime.timedelta(seconds=(end-start)))
