#! /bin/python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,request,Response,redirect,url_for,send_from_directory,g
from random import randrange
from flask.json import jsonify
from pyecharts import options as opts
from pyecharts.charts import Bar,Line,Timeline,Grid
from pyecharts.options.global_options import ToolboxOpts
from pyecharts.types import Toolbox
from data_collection import meminfo_query,sql_opera,android_adb
from pyecharts.commons.utils import JsCode
import datetime,string,os

adb = android_adb.ADB()
meminfo = meminfo_query.meminfo()
app = Flask(__name__, template_folder='templates', static_folder="static")

class DataStore():
    device_ip1 = None
    device_ip2 = None
    apps_names = []

data = DataStore()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/js/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)


@app.route("/index/appmem") 
def lines():
    return render_template("appmem.html")

@app.route("/device", methods=["POST", "GET"])
def connect_device():
    if request.method == "GET":
        data.device_ip1 = request.args['device']
        try:
            adb.adb_connect(str(data.device_ip1))
            process_infos = adb.adb_dev_output(data.device_ip1, "dumpsys meminfo |grep -A 2000 'PSS by process' |grep -B 2000 'PSS by OOM adjustment' |grep -v PSS|grep -v grep |grep : |cut -d':' -f2")
            process_list = list(filter(None,process_infos.split(" ")))
            data.apps_names = [ i for i in process_list if i.find('pid')!=1 ]
            return render_template("appmem.html")
        except Exception as e:
            return render_template("appmem.html") 

@app.route("/appsnames")
def apps_names():
    return jsonify(data.apps_names)

def line_area_stacks() -> Line:
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
                linestyle_opts=opts.LineStyleOpts(width=0)
                )
        .add_yaxis('native_mem',
                [],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0)
                )

        .add_yaxis('code_mem',
                [],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0)
                )

        .add_yaxis('stack_mem',
                    [],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0)
                )

        .add_yaxis('graph_mem',
                [],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                )

        .add_yaxis('others_mem',
                [],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0)
                )
        .add_yaxis('system_mem',
                [],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0)
                )
        .add_yaxis('total_mem',[],is_symbol_show=True)
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
    line.set_colors(colors=['rgba(0,255,255)', 'rgba(0,191,255)', 'rgba(100,149,237)', 'rgba(0,128,128)', 'rgba(255,140,0)', 'rgba(70,130,180)', 'rgba(119,136,153)'])
    line.set_global_opts(datazoom_opts=opts.DataZoomOpts(orient="horizontal"))
    grid = Grid(init_opts=opts.InitOpts(theme='white',width='980px', height='600px'))
    grid.add(line, grid_opts=opts.GridOpts(pos_left='3%', pos_right='4%', pos_bottom='3%'))
    grid.render_notebook()
    return line

def bar_bases() -> Bar:
    c = (
        Bar()
        .add_xaxis(['java_mem', 'native_mem', 'code_mem', 'stack_mem', 'graph_mem', 'others_mem', 'system_mem', 'total_mem'])
        .add_yaxis("java_mem",color='pink')
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
    c = line_area_stacks()
    return c.dump_options_with_quotes() 

@app.route("/lineDynamicDatas")
def update_line_datas():
    current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    if data.device_ip1:
        try:
            info = meminfo.get_app_meminfo(data.device_ip1, "com.rokid.ai.turen")
            info = [ round(float(i)/1024,2) for i in info ]
            return jsonify({'name':current_time,'value':{'java_mem': info[0], 'native_mem': info[1], 'code_mem': info[2], 'stack_mem': info[3], 'graph_mem': info[4], 'others_mem': info[5], 'system_mem': info[6], 'total_mem': info[7]}})
        except Exception as e:
            return  jsonify({}) 
    else:
        return  jsonify({})

@app.route("/linkdevice", methods=["POST", "GET"])
def link_device():
    device_message = {}
    if request.method == "GET":
        data.device_ip2 = request.args['device']
        try:
            adb.adb_connect(str(data.device_ip2))
            device_sn = adb.adb_dev_output(data.device_ip2, 'getprop persist.rokid.glass.sn')
            device_os_version = adb.adb_dev_output(data.device_ip2, 'getprop ro.build.version.incremental')
            device_message["sn"]=device_sn if device_sn else None
            device_message["os_version"]=device_os_version if device_os_version else None
            return render_template("phymem.html")
        except Exception as e:
            return render_template("phymem.html") 

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
        .add_yaxis('total_mem',
                [],
                is_symbol_show=True,
                areastyle_opts=opts.AreaStyleOpts(
                opacity=0.8
                )
                )
        .add_yaxis('used_mem',
                [],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                opacity=0.8
                )
                )
        .add_yaxis('free_mem',
                [],
                stack='stack',
                is_smooth=True,
                is_symbol_show=False,
                linestyle_opts=opts.LineStyleOpts(width=0),
                areastyle_opts=opts.AreaStyleOpts(
                opacity=0.8
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
    line.set_colors(colors=['#5B00AE', '#FF8000', '#CCFF80'])
    line.set_global_opts(datazoom_opts=opts.DataZoomOpts(orient="horizontal"))
    grid = Grid(init_opts=opts.InitOpts(theme='white',width='980px', height='600px'))
    grid.add(line, grid_opts=opts.GridOpts(pos_left='3%', pos_right='4%', pos_bottom='3%'))
    grid.render_notebook()
    return line

@app.route("/lineChart")
def get_line_chart():
    c = line_area_stack()
    return c.dump_options_with_quotes() 

@app.route("/lineDynamicData")
def update_line_data():
    if data.device_ip2:
        try:
            info = meminfo.get_device_meminfo(data.device_ip2)
            info = [ round(float(i)/1024,2) for i in info ]
            current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            return jsonify({'name':current_time,'value':{'total_mem': info[0], 'used_mem': info[1], 'free_mem': info[2]}})
        except Exception as e:
            return  jsonify({}) 
    else:
        return  jsonify({})


@app.route("/index/phymem") 
def liness():
    return render_template("phymem.html")


@app.route("/index/history")
def history():
    return render_template("historyperfmancedata.html")   


if __name__ == '__main__':
    app._static_folder = os.path.abspath("static/")
    app.run(host='0.0.0.0', port=8003,debug=True)

