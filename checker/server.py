#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 创建报告
"""

import os,re,time,subprocess,sys,json
# from ..loggers import JFMlogging
# logger = JFMlogging().getloger()
from flask import Flask, request
from flask import render_template
from config import *
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


@app.route('/getreport',methods=['GET'])
def html():
    '''
    拼接html报告
    '''
    gd = GetData()
    base_info = gd.get_base()
    pkg_info = gd.get_pkg_info()
    apk_info = gd.make_entries()
    apk_detail = gd.get_html_table()
    return render_template("report_template.html",
                           appname=pkg_info['package'],
                           appversion=pkg_info['versionName'],
                           appsize=base_info['apksize'],
                           minSdkVersion=pkg_info['minSdkVersion'],
                           targetSdkVersion=pkg_info['targetSdkVersion'],
                           appinfo = apk_info,
                           appdetail=apk_detail,
                           reporttime = time.strftime("%Y-%m-%d %H:%M:%S"),
                           )





