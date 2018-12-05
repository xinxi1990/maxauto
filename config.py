#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,shutil,time
from tools.loggers import JFMlogging
logger = JFMlogging().getloger()

project_path = os.path.abspath(os.path.dirname(__file__))
android_tmp = os.path.join(project_path,'report/tmp/')
# 主缓存目录



install_app_log= os.path.join(project_path,'report/tmp/install_app.log')
# 安装app耗时log日志
lanuch_app_log= os.path.join(project_path,'report/tmp/lanuch_app.log')
# 启动app耗时log日志
logintest_app_log= os.path.join(project_path,'report/tmp/logintest_app.log')
# 测试app登录log日志
uninstall_app_log= os.path.join(project_path,'report/tmp/uninstall_app.log')


sdcard_path = "/sdcard/"
crash_savepath = os.path.join(project_path,"report/tmp/crash.log")
monkey_log = os.path.join(project_path,"report/tmp/monkey.log")
page_log = os.path.join(project_path,"report/tmp/page.log")
monkey_jar = os.path.join(project_path,"monkey/libs/monkey.jar")
framework_jar = os.path.join(project_path, "monkey/libs/framework.jar")
device_crash_path = '/sdcard/crash-dump.log'
get_performance_path = os.path.join(project_path, "monkey/getper.sh")
performanc_out = os.path.join(project_path, "report/tmp/")
performance_folder = os.path.join(project_path, "report/tmp/")
max_path = os.path.join(os.getcwd(),"monkey/config/max.config")
device_crash_image = '/sdcard/Crash_*'
image_key = '*Crash_*'
local_images_path = os.path.join(project_path,"report/tmp/images")
local_image_folder = "images"
images_zip = os.path.join(project_path,"report/tmp/images.zip")
acts_path = os.path.join(project_path,"report/tmp/acts.log")
cpu_path = os.path.join(project_path,'report/tmp/cpu.log')
mem_path = os.path.join(project_path,'report/tmp/mem.log')
all_activity_path = os.path.join(project_path,'report/tmp/allactivity.log')
run_model = "uiautomatordfs" #uiautomatormix
throttle = 500
sleep_time = 3


host = '0.0.0.0'
port = 7777
api = 'http://{}:{}/report'.format(host, port)
report_folder = os.path.join(project_path,'report')
report_path = os.path.join(report_folder,"report_{}.html".format(time.strftime("%Y%m%d%H%M%S")))