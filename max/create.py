#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 创建报告
"""

import os,re,time,subprocess,sys,json
sys.path.append('..')
import jinja2
from jinja2 import Environment, PackageLoader
from tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from report.predata import *
from monkey.getbasic import GetBasic
from report.getdata import GetData



class Create():

    def __init__(self,apk_path,device_name,report_path):
        self.apk_path = apk_path
        self.device_name = device_name
        self.report_path = report_path


    def create_html(self):
        '''
        生成html报告
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

        apkpath = self.apk_path
        device_name = self.device_name
        gd = GetData()
        gb = GetBasic(apkpath, device_name)
        calculate_coverage = gd.get_calculate_coverage()

        report_folder = os.path.join(self.report_path, 'reports')
        if not os.path.exists(report_folder):
           os.makedirs(report_folder)
           logger.info("创建报告存储文件夹:{}".format(report_folder))
        report_path = os.path.join(report_folder, "report_{}.html".format(time.strftime("%Y%m%d%H%M%S")))
        try:
            env = Environment(loader=PackageLoader('max', 'templates'))
            template = env.get_template("template.html")
            html_content = template.render( appname=gb.get_app_name(),
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
                               data2=tuples2, pagetime=data2[0], pageinfo=data2[1], pageactivity=data2[2],
                               data3=tuples3, fpstime=data3[0], fpsinfo=data3[1], fpsactivity=data3[2],
                               data4=tuples4, networktime=data4[0], networkinfo=data4[1], networkactivity=data4[2],
                               reporttime=time.strftime("%Y-%m-%d %H:%M:%S"),
                               runpages=gd.get_run_pages(),
                               runtime=gd.get_runtime(),
                               clickcount=gd.get_click_count(),
                               crashdetail=gd.get_crash_detail(),
                               crashimage=gd.get_crash_image(),
                               login=gd.get_login(),)
            with open(report_path, "wb") as f:
                f.write(html_content.encode("utf-8"))
                logger.info('报告地址:\n{}'.format(report_path))
        except Exception as e:
            logger.error('生成报告异常!{}'.format(e))
        finally:
            return report_path