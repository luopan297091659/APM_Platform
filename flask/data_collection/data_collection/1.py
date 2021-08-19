#! /bin/python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,request,Response,redirect,url_for
from random import randrange
from flask import Flask, render_template
from flask.json import jsonify
from pyecharts import options as opts
from pyecharts.charts import Bar,Line,Timeline,Grid
from data_collection import device_meminfo,sql_opera
from pyecharts.commons.utils import JsCode
import datetime,string

app = Flask(__name__, static_folder="templates")

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello Flask!'

@app.route("/area-stack")
def area():
    return render_template("area-stack.html")


@app.route("/index")
def ind():
    return render_template("area-stack-gradient.html")

def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "耐克", "阿迪达斯", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

def line_base() -> Line:
    line = (
        Line()
        .add_xaxis(["{}".format(i) for i in range(10)])
        .add_yaxis(
            series_name="",
            y_axis=[randrange(50, 80) for _ in range(10)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="动态数据"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    line.set_global_opts(datazoom_opts=opts.DataZoomOpts(orient="horizontal"))
    return line

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()



@app.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()

idx = 9

@app.route("/lineDynamicData")
def update_line_data():
    global idx
    idx = idx + 1
    return jsonify({"name": idx, "value": randrange(50, 80)})

@app.route("/index/line")
def line():
    return render_template("line_on.html")

def line_area_stack() -> Line:
#def line_area_stack(x_value, y_value1, y_value2, y_value3, y_value4, y_value5, y_value6, y_value7) -> Line:
    line = (
        Line()
        .add_xaxis(["{}".format(i) for i in range(10)])
        .add_yaxis(
            series_name="",
            y_axis=[randrange(50, 80) for _ in range(10)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="动态数据"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    line.set_global_opts(datazoom_opts=opts.DataZoomOpts(orient="horizontal"))

    line = (
        Line()
        .add_xaxis([])
        .add_yaxis('java_mem',
                [140, 232, 101, 264, 90, 340, 250],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.8,
                    color=JsCode("""
                                    new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [{offset: 0, color: 'rgba(128, 255, 165)'},
                                        {offset: 1, color: 'rgba(1, 191, 236)'}],
                                        false)
                                    """)
                )
                )
        .add_yaxis('native_mem',
                [120, 282, 111, 234, 220, 340, 310],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.8,
                    color=JsCode("""
                                    new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [{offset: 0, color: 'rgba(0, 221, 255)'},
                                        {offset: 1, color: 'rgba(77, 119, 255)'}],
                                        false)
                                    """)
                )
                )

        .add_yaxis('code_mem',
                [320, 132, 201, 334, 190, 130, 220],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.8,
                    color=JsCode("""
                                    new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [{offset: 0, color: 'rgba(55, 162, 255)'},
                                        {offset: 1, color: 'rgba(116, 21, 219)'}],
                                        false)
                                    """)
                )
                )

        .add_yaxis('stack_mem',
                    [220, 402, 231, 134, 190, 230, 120],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.8,
                    color=JsCode("""
                                    new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [{offset: 0, color: 'rgba(255, 0, 135)'},
                                        {offset: 1, color: 'rgba(135, 0, 157)'}],
                                        false)
                                    """)
                )
                )

        .add_yaxis('graph_mem',
                [220, 302, 181, 234, 210, 290, 150],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.8,
                    color=JsCode("""
                                    new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [{offset: 0, color: 'rgba(255, 191, 0)'},
                                        {offset: 1, color: 'rgba(224, 62, 76)'}],
                                        false)
                                    """)
                )
                )

        .add_yaxis('others_mem',
                [220, 302, 181, 234, 210, 290, 150],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.8,
                    color=JsCode("""
                                    new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [{offset: 0, color: 'rgba(255, 191, 100)'},
                                        {offset: 1, color: 'rgba(224, 62, 76)'}],
                                        false)
                                    """)
                )
                )
        .add_yaxis('system_mem',
                [220, 302, 181, 234, 210, 290, 150],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.8,
                    color=JsCode("""
                                    new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [{offset: 0, color: 'rgba(255, 151, 0)'},
                                        {offset: 1, color: 'rgba(221, 62, 76)'}],
                                        false)
                                    """)
                )
                )
        .add_yaxis('total_mem',
                [220, 302, 181, 234, 210, 290, 150],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.8,
                    color=JsCode("""
                                    new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [{offset: 0, color: 'rgba(255, 191, 80)'},
                                        {offset: 1, color: 'rgba(224, 62, 176)'}],
                                        false)
                                    """)
                )
                )    
            )
    line.set_global_opts(xaxis_opts=opts.AxisOpts(boundary_gap=False),
                        yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=False),
                                                axistick_opts=opts.AxisTickOpts(is_show=False),
                                                splitline_opts=opts.SplitLineOpts(is_show=True,
                                                                                    linestyle_opts=opts.LineStyleOpts(color='#E0E6F1'))
                                                                                    ),
                        tooltip_opts=opts.TooltipOpts(is_show=True, trigger='axis', axis_pointer_type='cross'),
                        title_opts=opts.TitleOpts(title="渐变堆叠面积图")
                        ) 

    line.set_series_opts(opts.LabelOpts(is_show=False))
    line.set_colors(colors=['#80FFA5', '#00DDFF', '#37A2FF', '#FF0087', '#FFBF00'])
    line.set_global_opts(datazoom_opts=opts.DataZoomOpts(orient="horizontal"))
    grid = Grid(init_opts=opts.InitOpts(theme='white',width='980px', height='600px'))
    grid.add(line, grid_opts=opts.GridOpts(pos_left='3%', pos_right='4%', pos_bottom='3%'))
    grid.render_notebook()
    return line

def bar_bases() -> Bar:
    c = (
        Bar()
        .add_xaxis(['java_mem', 'native_mem', 'code_mem', 'stack_mem', 'graph_mem', 'others_mem', 'system_mem', 'total_mem'])
        # .add_yaxis("java_mem", [randrange(0, 100) for _ in range(8)])
        .add_yaxis("java_mem",color='pink')
        # .add_yaxis("商家B", [randrange(0, 100) for _ in range(8)])
        .add_yaxis("native_mem",color='palevioletred')
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

@app.route("/barCharts")
def get_bar_charts():
    c = bar_bases()
    return c.dump_options_with_quotes()

@app.route("/lineCharts")
def get_line_charts():
    c = line_area_stack()
    return c.dump_options_with_quotes() 

@app.route("/lineDynamicDatas")
def update_line_datas():
    global idx
    idx = idx + 1
    current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    return jsonify({'name':current_time,'value':{'java_mem': randrange(50, 80), 'native_mem': randrange(50, 80), 'code_mem': randrange(50, 80), 'stack_mem': randrange(50, 80), 'graph_mem': randrange(50, 80), 'others_mem': randrange(50, 80), 'system_mem': randrange(50, 80), 'total_mem': randrange(50, 80)}})


@app.route("/luopan")
def luopan():
    line = line_area_stack()
    line.render(path='templates/first_bar.html')
    return render_template('first_bar.html')

@app.route("/index/lines") 
def lines():
    return render_template("area-stack.html")

@app.route("/index/bake") 
def liness():
    return render_template("area-stack-gradient.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)

