#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,subprocess,sys
from checkapp import CheckApp
from client import get_html
from getdata import GetData
from loggers import JFMlogging
from findapp import *
from config import *
logger = JFMlogging().getloger()


def kill_pid(port):
    '''
    结束appium进程
    :return:
    '''
    if os.popen('lsof -i:{}'.format(port)).read() == '':
        logger.info('未查询到进程')
    else:
        result = os.popen('lsof -i:{}'.format(gunicorn_port)).readlines()
        for line in result:
            if 'Python' in line or 'python2.7' in line:
                pid = line.split()[1]
                subprocess.call('kill -9 {}'.format(pid),shell=True)
                logger.info('kill进程{}'.format(pid))

def start_gunicorn():
    kill_pid(gunicorn_port)
    cmd = 'gunicorn -D -w 1 -b {} server:app'.format(gunicorn_address) # -D 后台运行
    #cmd = 'gunicorn -w 1 -b {} server:app'.format(gunicorn_address)
    subprocess.call(cmd, shell=True)
    time.sleep(3)
    logger.info('启动gunicorn服务!')



def run(apk_path,mail_list):
    try:
        logger.info("开始检查apk")
        CheckApp(apk_path).check_app()
        logger.info("开始生成报告")
        start_gunicorn()
        report_path = get_html(mail_list)
        response_filepath = UPLoad().upload_local_report(report_path)
        total_size = GetData().get_base()['apksize']
        version = GetData().get_pkg_info()['versionName']
    except Exception as e:
        logger.error("运行异常:{}".format(e))



if __name__ == '__main__':
    try:
        apk_path = sys.argv[1]
        mail_list = sys.argv[2]
        apk_path  = find_app(apk_path)
        logger.info("apk路径:{}".format(apk_path))
        run(apk_path,mail_list)
    except Exception as e:
        logger.error("运行失败!{}".format(e))
