#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,shutil,time,sys
reload(sys)
sys.setdefaultencoding("utf-8")
project_path = os.path.abspath(os.path.dirname(__file__))
out_path = project_path + "/out"
out_name = project_path + "/out/check"
config_path = project_path + "/check.json"
matrix_path = project_path + "/matrix-apk-canary-0.4.7.jar"
out_json_path = out_path + "/check.json"
out_html_path = out_path + "/check.html"
gunicorn_port = '3031'
gunicorn_address = '127.0.0.1' + ':' + gunicorn_port
host = '127.0.0.1'
port = '3031'
api = 'http://{}:{}/getreport'.format(host, gunicorn_port)
report_folder = os.path.join(project_path, "report")
report_path = os.path.join(report_folder,"report_{}.html".format(time.strftime("%Y%m%d%H%M%S")))


DEBUG = True
if DEBUG:
    domain = 'http://localhost:5000/'
else:
    domain = 'https://backend.luojilab.com/'
upload_result_api = domain + 'performance/creatchecker'
# 上传结果
upload_report_api = 'https://backend.luojilab.com/report/uploadreport'
# 上传报告

env = 'test'

taskDescription = "Unzip the apk file to dest path."
zn_taskDescription = u"解压文件"

taskDescription1 = "Read package info from the AndroidManifest.xml."
zn_taskDescription1 = u"读取AndroidManifest.xml文件"

taskDescription2 = "Find out the non-alpha png-format files whose size exceed limit size in desc order."
zn_taskDescription2 = u"找出大小超过限制大小的非alpha png格式文件"

taskDescription3 = "Show uncompressed file types."
zn_taskDescription3 = u"显示未压缩的文件类型"

taskDescription4 = "Find out the duplicated files."
zn_taskDescription4 = u"找出重复的文件"

taskDescription5 = "Find out the unused assets."
zn_taskDescription5 = u"找出未使用的资产"

taskDescription6 = "Show files whose size exceed limit size in order."
zn_taskDescription6 = u"按顺序显示大小超过限制大小的文件"

taskDescription7 = "Count methods in dex file, output results group by class name or package name."
zn_taskDescription7 = "计算dex文件中的方法，按类名或包名输出结果"

taskDescription8 = "Check if there are more than one library dir in the 'lib'."
zn_taskDescription8 = u"检查'lib'中是否有多个库目录"

taskDescription9 = "Count the R class."
zn_taskDescription9 = u"统计R class"

taskDescription10 = "Check if the apk handled by resguard."
zn_taskDescription10 = u"检查apk是否由resguard处理"