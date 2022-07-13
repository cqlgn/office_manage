from django.shortcuts import render, get_object_or_404
from .models import cmdb, fine, back_money
import time
from jinja2 import Environment, FileSystemLoader
from django.http import HttpResponse
from django.http import JsonResponse

from pyecharts import options as opts
from pyecharts.charts import Line, Bar
from pyecharts.globals import ThemeType
# 图表的布局, Page垂直布局，Grid水平布局
from pyecharts.charts import Page, Grid

from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
import requests
import json
# today = time.strftime("%Y-%m-%d", time.localtime())

def home(request):
    messages = cmdb.objects.all()
    fines = fine.objects.all()
    back_moneys = back_money.objects.all()
    #罚款
    penalty = 0
    for money in fines:
        penalty += money.金额
    #入账
    summary = 0
    for money in back_moneys:
        summary += money.入账
    #消费
    use = 0
    for money in messages:
        use += money.金额
    #结余
    remain = summary-use
    #返回
    return render(request, 'home.html',context={
        'summary':summary,
        'use':use,
        'remain':remain,
        'penalty':penalty
    }
                  )
def total_table(request):
    messages = cmdb.objects.all()
    for date in messages:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'total_table.html', context={
        'cmdbs': messages})

def fine_table(request):
    messages = fine.objects.all()
    for date in messages:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'fine_table.html', context={
        'fine_table': messages})

def back_money_table(request):
    messages = back_money.objects.all()
    for date in messages:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'back_money_table.html', context={
        'back_money_table': messages})

def office(request):
    objs = cmdb.objects.filter(小类别='日常办公')
    for date in objs:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'office.html',context={
        'objs': objs,
    }
                  )
def card(request):
    objs = cmdb.objects.filter(小类别='名片印制')
    for date in objs:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'card.html',context={
        'objs': objs,
    }
                  )

def benefit(request):
    objs = cmdb.objects.filter(小类别='员工福利')
    for date in objs:
        date.日期 = date.日期.strftime("%Y-%m-%d")
    return render(request, 'benefit.html',context={
        'objs': objs,
    }
                  )
def consume(req):
    if req.method == "POST":
        日期 = req.POST.get("日期", None)
        月份 = req.POST.get("月份", None)
        花费地 = req.POST.get("花费地", None)
        小类别 = req.POST.get("小类别", None)
        购买渠道 = req.POST.get("购买渠道", None)
        明细 = req.POST.get("明细", None)
        金额 = req.POST.get("金额", None)
        发票类型 = req.POST.get("发票类型", None)


        cmdb.objects.create(
            日期=日期,
            月份=月份,
            花费地=花费地,
            小类别=小类别,
            购买渠道=购买渠道,
            明细=明细,
            金额=金额,
            发票类型=发票类型
        )
        #
        # info_list = cmdb.objects.all()
        #
        # return render(req, "home.html", {"info_list": info_list})

    return render(req, "consume.html")

def fakuan(req):
    if req.method == "POST":
        日期 = req.POST.get("日期")
        明细 = req.POST.get("明细")
        金额 = req.POST.get("金额")
        fine.objects.create(
            日期=日期,
            明细=明细,
            金额=金额
        )
    return render(req, "fine.html")


def back(req):
    if req.method == "POST":
        日期 = req.POST.get("日期")
        入账 = req.POST.get("入账")
        back_money.objects.create(
            日期=日期,
            入账=入账
        )
    return render(req, "back_money.html")

def statistic(request):
    # 设置行名
    columns = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    # 设置数据
    data1 = []
    data2 = []
    for i in range(1,13):
        pay = 0
        objs = cmdb.objects.filter(月份=i)
        for money in objs:
            pay +=money.金额
        data1.append(pay)
        data2.append(pay)

    """初始化时Page()中是可以指定参数的，比如layout，DraggablePageLayout是令每个模块可以被任意拖动、
    缩放，便于人工布局；SimplePageLayout是令每个模块自动水平居中对齐。不指定的话，所有模块就会靠左对齐。"""
    page_1 = Page(layout=Page.SimplePageLayout)
    # 初始化grid对象
    grid1_1 = Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='1600px'))

    # 折线图
    line = (
        # 创建折线图
        Line()
            # 增加主标题与副标题
            #.set_global_opts(title_opts=opts.TitleOpts(title="折线图", subtitle="一年的降水量与蒸发量"))
            # X轴标签
            .add_xaxis(columns)
            # 增加折线图数据, symbol_size:圆点的大小，is_smooth:是否圆滑曲线,color:曲线的颜色
            # 注意：当上面的init_opts设置了主题样式后，color就不起作用了
            .add_yaxis("消费金", data1, symbol_size=10, is_smooth=True, color="write",
                       markpoint_opts=opts.MarkPointOpts(data=[
                           opts.MarkPointItem(name="最大值", type_="max"),
                           opts.MarkPointItem(name="最小值", type_="min")]))
    )

    # 柱状图
    # 创建柱状图
    bar = Bar()
    # 增加主题和副标题
    bar.set_global_opts(title_opts=opts.TitleOpts(title="消费金", subtitle="一年的全量展示"))
    # 添加柱状图的数据
    bar.add_xaxis(columns)
    bar.add_yaxis("消费金", data2)
    # 增加平均线
    bar.set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="平均值", type_="average")]))
    # 增加最大值,最小值
    bar.set_series_opts(markpoint_opts=opts.MarkPointOpts(data=[
        opts.MarkPointItem(name="最大值", type_="max"),
        opts.MarkPointItem(name="最小值", type_="min")
    ]))

    # 将两个图表分别添加到grid对象里面去
    # 对grid的pos参数而言，pos_left是显示在靠右的位置 pos_right同理
    grid1_1.add(line, grid_opts=opts.GridOpts(pos_right="55%"))
    grid1_1.add(bar, grid_opts=opts.GridOpts(pos_left="55%"))
    # page里可以add多种元素，grid chart image等等
    page_1.add(grid1_1)
    return HttpResponse(page_1.render_embed())












