#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 创建报告
"""

import os,re,time,subprocess,sys,json
sys.path.append('..')
from tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from flask import Flask, request
from flask import render_template
from threading import Thread
from sendmail import *
from config import *
from predata import *
from monkey.getbasic import GetBasic
from getdata import GetData


app = Flask(__name__)

def run_server():
    '''
    启动Flask
    :return:
    '''
    # stop_server()
    logger.info("启动服务...")
    app.run(host=host, port=port, debug=True, threaded=False)


def stop_server():
    '''
    停止Flask
    :return:
    '''
    result = os.popen('lsof -i:{}'.format(port))
    for line in result.readlines():
        if 'Python' in line or 'python2.7' in line:
            pid = line.split()[1]
            logger.info("结束服务进程")
            subprocess.call('kill {}'.format(pid),shell=True)


@app.route('/getreport',methods=['POST'])
def html():
    '''
    拼接html报告
    '''
    tuples = ()
    data = read_mem()
    i = []
    j = []
    try:
        for index in range(len(data[0])):
            i.append(data[0][index])
            i.append(float(data[1][index]))
            j.append(i)
            i = []
    except Exception as e:
        logger.error(e)
    tuples = tuples + tuple(j)

    tuples1 = ()
    data1 = read_cpu()
    k = []
    H = []
    try:
        for index in range(len(data1[0])):
            k.append(data1[0][index])
            k.append(float(data1[1][index]))
            H.append(k)
            k = []
    except Exception as e:
        logger.error(e)
    tuples1 = tuples1 + tuple(H)

    tuples2 = ()
    data2 = get_page()
    m = []
    n = []
    try:
        for index in range(len(data2[0])):
            m.append(data2[0][index])
            m.append(float(data2[1][index]))
            n.append(m)
            m = []
    except Exception as e:
        logger.error(e)
    tuples2 = tuples2 + tuple(n)

    tuples3 = ()
    data3 = read_fps()
    m = []
    n = []
    try:
        for index in range(len(data3[0])):
            m.append(data3[0][index])
            m.append(float(data3[1][index]))
            n.append(m)
            m = []
    except Exception as e:
        logger.error(e)
    tuples3 = tuples3 + tuple(n)


    tuples4 = ()
    data4 = read_network()
    m = []
    n = []
    try:
        for index in range(len(data4[0])):
            m.append(data4[0][index])
            m.append(float(data4[1][index]))
            n.append(m)
            m = []
    except Exception as e:
        logger.error(e)
    tuples4 = tuples4 + tuple(n)
    print tuples4

    params = json.loads(request.get_data())
    apkpath = params['apk_path']
    device_name = params['device_name']
    gd = GetData()
    gb = GetBasic(apkpath,device_name)
    calculate_coverage = gd.get_calculate_coverage()
    return render_template("report_template.html",
                           appname=gb.get_app_name(),
                           appversion=gb.get_app_version(),
                           appsize=gb.get_app_size(),
                           devicesmodel=gb.get_devices_model(),
                           devicesversion=gb.get_devices_version(),
                           installtime=gd.get_install_time(),
                           coldtime=gd.get_lanuch_time(),
                           alreadycov=calculate_coverage[0],
                           notcov=calculate_coverage[1],
                           crashcount=gd.get_crash_count(),
                           data=tuples, memtime=data[0], meminfo=data[1], memactivity=data[2],
                           data1=tuples1, cputime=data1[0], cpuinfo=data1[1], cpuactivity=data1[2],
                           data2=tuples2,pagetime=data2[0], pageinfo=data2[1], pageactivity=data2[2],
                           data3=tuples3, fpstime=data3[0], fpsinfo=data3[1], fpsactivity=data3[2],
                           data4=tuples4, networktime=data4[0], networkinfo=data4[1], networkactivity=data4[2],
                           reporttime = time.strftime("%Y-%m-%d %H:%M:%S"),
                           runpages = gd.get_run_pages(),
                           runtime = gd.get_runtime(),
                           clickcount = gd.get_click_count(),
                           crashdetail = gd.get_crash_detail(),
                           crashimage = gd.get_crash_image(),
                           login = gd.get_login(),
                           )








