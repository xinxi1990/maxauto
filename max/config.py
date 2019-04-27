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
logintest_app_log= os.path.join(project_path,'report/tmp/login_app.log')
# 测试app登录log日志
uninstall_app_log= os.path.join(project_path,'report/tmp/uninstall_app.log')
# aappium的log日志
appium_log= os.path.join(project_path,'report/tmp/appium.log')
sdcard_path = "/sdcard/"
crash_savepath = os.path.join(project_path,"report/tmp/crash.log")
monkey_log = os.path.join(project_path,"report/tmp/monkey.log")
monkey_jar = os.path.join(project_path,"monkey/libs/monkey.jar")
framework_jar = os.path.join(project_path, "monkey/libs/framework.jar")
device_crash_path = '/sdcard/crash-dump.log'
get_performance_path = os.path.join(project_path, "monkey/getper.sh")
report = os.path.join(project_path, "report")
performance_out = os.path.join(project_path, "report/tmp/")
performance_folder = os.path.join(project_path, "report/tmp/")
max_path = os.path.join(project_path,"monkey/config/max.config")
device_crash_image = '/sdcard/Crash_*'
image_key = '*Crash_*'
local_images_path = os.path.join(project_path,"monkey/images")
images_zip = os.path.join(project_path,"monkey/images.zip")
run_activity_path = os.path.join(project_path,"report/tmp/runactivity.log")
run_activity_path_back = os.path.join(project_path,"report/tmp/runactivity_back.log")
cpu_path = os.path.join(project_path,'report/tmp/cpu.log')
mem_path = os.path.join(project_path,'report/tmp/mem.log')
page_path = os.path.join(project_path,"report/tmp/page.log")
network_path = os.path.join(project_path,"report/tmp/network.log")
fps_path = os.path.join(project_path,"report/tmp/fps.log")
all_activity_path = os.path.join(project_path,'report/tmp/allactivity.log')
run_model = "uiautomatordfs" #uiautomatormix
throttle = 200
sleep_time = 3
gunicorn_port = '3031'
gunicorn_address = '127.0.0.1' + ':' + gunicorn_port
host = '127.0.0.1'
port = '3031'
api = 'http://{}:{}/getreport'.format(host, gunicorn_port)
