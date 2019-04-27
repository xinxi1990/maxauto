#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess,sys,yaml
from monkey.getbasic import GetBasic
from monkey.monkey import Monkey
from lanuchtest.lanuchapp import LanuchApp
from Installtest.installapp import InstallApp
from logintest.logintest import LoginApp
from report.create import Create
from report.sendmail import *
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


def run(apk_path,device_name,runtime,mail_info,login_caseinfo):
    make_env()
    gb = GetBasic(apk_path,device_name)
    lanuch_activity = gb.get_app_activity()
    app_name = gb.get_app_name()
    app_version = gb.get_app_version()
    gb.get_all_activitys()
    InstallApp(device_name,app_name,apk_path,install_app_log,uninstall_app_log).install_app()
    LanuchApp(device_name,app_name,lanuch_activity,lanuch_app_log).lanuch_app()
    LoginApp(device_name, app_name, lanuch_activity,login_caseinfo).test_login()
    # Monkey(device_name,runtime,app_name).start_monkey()
    # report_path = Create(apk_path,device_name).create_html()
    # SendMail(mail_info, report_path).send_mail()


def load_config(config_path):
    with open(config_path,"r") as f_r:
        yaml_info = yaml.load(f_r)
        return yaml_info


def load_mail_config():
    return yaml_info['mailconfig']

def load_login_case():
    return yaml_info['logincase']



if __name__ == '__main__':

    config_path = sys.argv[1]
    # 配置config路径
    yaml_info = load_config(config_path)
    apk_path = yaml_info['commonconfig']['apkapth']
    device_name = yaml_info['commonconfig']['devicename']
    run_time = yaml_info['commonconfig']['runtime']
    mail_info  = load_mail_config()
    login_caseinfo = load_login_case()
    params = (apk_path + '\n' +
              device_name + '\n' +
              run_time )
    logger.info('参数:' + '\n' + '{}'.format(params))
    run(apk_path,device_name,run_time,mail_info,login_caseinfo)


