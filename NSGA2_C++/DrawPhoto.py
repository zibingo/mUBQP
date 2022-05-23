# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pyecharts import Scatter, Scatter3D, Page


def Draw_2D(EpName, PhotoName, HtmlName, occ, m, n, Pm, Max_Gen, RunNum,PyechartsDraw):
    with open(EpName, 'r') as f:
        x, y = [], []
        for line in f.readlines():
            l = line.strip("\n").split(" ")
            x.append(int(l[0]))
            y.append(int(l[1]))
        points = []
        for i in range(len(x)):
            points.append([x[i], y[i]])
        plt.scatter(x, y, marker='o', s=10)
        plt.xlabel("f1")
        plt.ylabel("f2")
        plt.title("occ: {} m: {} n: {} Pm: {}  Max_Gen: {} EP: {} run: {}".format(
            occ, m, n, Pm, Max_Gen,  len(x), RunNum))
        plt.savefig(PhotoName)
        plt.cla()
        if PyechartsDraw == True:
            # ----------------------------------------------------
            scatter = Scatter("散点图", "f1与f2")
            scatter._width = 500
            scatter._height = 500
            # xais_name是设置横坐标名称，这里由于显示问题，还需要将y轴名称与y轴的距离进行设置
            scatter.add(HtmlName, x, y, xaxis_name="f1", yaxis_name="f2")
            scatter.render(HtmlName)


def Draw_3D(EpName, PhotoName, HtmlName, occ, m, n, Pm, Max_Gen, RunNum,PyechartsDraw):
    with open(EpName, 'r') as f:
        x, y, z = [], [], []
        for line in f.readlines():
            l = line.strip("\n").split(" ")
            x.append(int(l[0]))
            y.append(int(l[1]))
            z.append(int(l[2]))
        points = []
        for i in range(len(x)):
            points.append([x[i], y[i], z[i]])
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(x, y, z, marker='o', s=10)
        ax.set_zlabel('f3', fontdict={'size': 14, 'color': 'red'})
        ax.set_ylabel('f2', fontdict={'size': 14, 'color': 'red'})
        ax.set_xlabel('f1', fontdict={'size': 14, 'color': 'red'})
        ax.set_title("occ: {} m: {} n: {} Pm: {}  Max_Gen: {} EP: {} run: {}".format(
            occ, m, n, Pm, Max_Gen,  len(x), RunNum))
        plt.savefig(PhotoName)
        plt.cla()  # 不清除的话，后续运行会覆盖
        if PyechartsDraw == True:
            # ----------------------------------------------------
            page = Page()
            data = []
            for i in range(len(x)):
                data.append([x[i], y[i], z[i]])
            range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
                        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            scatter3D = Scatter3D("occ : {}  Pm : {}  Max_Gen : {}".format(
                occ,  Pm, Max_Gen), width=1400,
                height=600)  # 设置图表的高和宽
            scatter3D.add("", data, is_visualmap=True,
                        visual_range_color=range_color)  # 视觉映射和颜色选择
            page.add(scatter3D)
            page.render(HtmlName)
