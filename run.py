#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from monkey.getbasic import GetBasic
from monkey.monkey import Monkey
from lanuchtest.lanuchapp import LanuchApp
from Installtest.installapp import InstallApp
from logintest.logintest import LoginApp
from report.client import get_html
from config import *



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
    os.chdir(report)
    kill_pid(gunicorn_port)
    cmd = 'gunicorn -D -w 1 -b {} server:app'.format(gunicorn_address)
    subprocess.call(cmd, shell=True)
    time.sleep(3)
    logger.info('启动gunicorn服务!')

def make_env():
    if os.path.exists(android_tmp):
        shutil.rmtree(android_tmp)
        logger.info('删除缓存目录:{}'.format(android_tmp))
    os.makedirs(android_tmp)
    logger.info('创建缓存目录:{}'.format(android_tmp))


def run(apk_path,device_name,runtime,mail_list):
    make_env()
    gb = GetBasic(apk_path,device_name)
    lanuch_activity = gb.get_app_activity()
    app_name = gb.get_app_name()
    app_version = gb.get_app_version()
    gb.get_all_activitys()
    InstallApp(device_name,app_name,apk_path,install_app_log,uninstall_app_log).install_app()
    LanuchApp(device_name,app_name,lanuch_activity,lanuch_app_log).lanuch_app()
    LoginApp(device_name, app_name, lanuch_activity).test_login()
    Monkey(device_name,runtime,app_name).start_monkey()
    start_gunicorn()
    get_html(apk_path,device_name,mail_list)

if __name__ == '__main__':
    # apk_path = sys.argv[1]
    # device_name = sys.argv[2]
    # mailist = sys.argv[3]
    # params = (apk_path + '\n' +
    #           device_name + '\n' +
    #           mailist)
    # logger.info('参数:' + '\n' + '{}'.format(params))
    apk_path = "/Users/xinxi/Downloads/TencentNews_63_v5710.apk"
    device_name = "192.168.56.101:5555"
    run_time = 3
    mail_list = 'xxxx'
    run(apk_path,device_name,run_time,mail_list)

