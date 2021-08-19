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

@app.route("/")
def index():
    return render_template("index.html")


def line_area_stack() -> Line:
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
                [],
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
                [],
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
                [],
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
                    [],
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
                [],
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
                [],
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
                [],
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
                [],
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
                        title_opts=opts.TitleOpts(title="AR Glass设备性能监控")
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
    current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    return jsonify({'name':current_time,'value':{'java_mem': randrange(50, 80), 'native_mem': randrange(50, 80), 'code_mem': randrange(50, 80), 'stack_mem': randrange(50, 80), 'graph_mem': randrange(50, 80), 'others_mem': randrange(50, 80), 'system_mem': randrange(50, 80), 'total_mem': randrange(50, 80)}})


@app.route("/index/lines") 
def lines():
    return render_template("area-stack.html")



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)

