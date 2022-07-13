from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.conf import settings

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("{}/templates".format(settings.BASE_DIR)))

from django.http import HttpResponse
from pyecharts import options as opts
from pyecharts.charts import Line, Bar
from pyecharts.globals import ThemeType

# 图表的布局, Page垂直布局，Grid水平布局
from pyecharts.charts import Page, Grid


def index(request):
    # pyecharts 支持链式调用
    # // 设置行名
    columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # // 设置数据
    data1 = []
    for i in range(1,13):
        pay = 0
        objs = cmdb.objects.filter(月份=i)
        for money in objs:
            pay +=money.金额
        data1.append(pay)
    data2 = []
    for i in range(1,13):
        pay = 0
        objs = fine.objects.filter(月份=i)
        for money in objs:
            pay +=money.金额
        data2.append(pay)

    """初始化时Page()中是可以指定参数的，比如layout，DraggablePageLayout是令每个模块可以被任意拖动、
    缩放，便于人工布局；SimplePageLayout是令每个模块自动水平居中对齐。不指定的话，所有模块就会靠左对齐。"""
    page_1 = Page(layout=Page.SimplePageLayout)
    # 初始化grid对象
    grid1_1 = Grid(init_opts=opts.InitOpts(theme=ThemeType.ROMA, width='1600px'))

    # 折线图
    line = (
        # 创建折线图
        Line()
            # 增加主标题与副标题
            .set_global_opts(title_opts=opts.TitleOpts(title="折线图", subtitle="一年的降水量与蒸发量"))
            # X轴标签
            .add_xaxis(columns)
            # 增加折线图数据, symbol_size:圆点的大小，is_smooth:是否圆滑曲线,color:曲线的颜色
            # 注意：当上面的init_opts设置了主题样式后，color就不起作用了
            .add_yaxis("降水量", data1, symbol_size=10, is_smooth=True, color="green",
                       markpoint_opts=opts.MarkPointOpts(data=[
                           opts.MarkPointItem(name="最大值", type_="max"),
                           opts.MarkPointItem(name="最小值", type_="min")]))
    )

    # 柱状图
    # 创建柱状图
    bar = Bar()
    # 增加主题和副标题
    bar.set_global_opts(title_opts=opts.TitleOpts(title="柱状图", subtitle="一年的降水量与蒸发量"))
    # 添加柱状图的数据
    bar.add_xaxis(columns)
    bar.add_yaxis("降水量", data1)
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