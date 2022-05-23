# -*- encoding: utf-8 -*-
'''
@Author                :   zibin
@Last Modified time    :   2022/05/10 19:43:35
@Contact               :   zibingo@qq.com
'''
from pyecharts import Scatter3D, Page


def PychartsDraw(x, y, z, name):
    page = Page()  # st
    data = []
    for i in range(len(x)):
        data.append([x[i], y[i], z[i]])
    range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
                   '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D("3D 散点图示例", width=1450, height=900)  # 设置图表的高和宽
    scatter3D.add("", data, is_visualmap=True,
                  visual_range_color=range_color)  # 视觉映射和颜色选择
    page.add(scatter3D)
    page.render(name+".html")
