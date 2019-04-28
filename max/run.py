#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess,sys,yaml
import argparse,os
from monkey.getbasic import GetBasic
from monkey.monkey import Monkey
from lanuchtest.lanuchapp import LanuchApp
from Installtest.installapp import InstallApp
from logintest.logintest import LoginApp
from create import Create
from report.sendmail import *
from config import *




def make_env():
    if os.path.exists(android_tmp):
        shutil.rmtree(android_tmp)
        logger.info('删除缓存目录:{}'.format(android_tmp))
    os.makedirs(android_tmp)
    logger.info('创建缓存目录:{}'.format(android_tmp))


def run(apk_path,device_name,runtime,mail_info,login_caseinfo,report_path):
    '''
    运行任务
    :param apk_path:
    :param device_name:
    :param runtime:
    :param mail_info:
    :param login_caseinfo:
    :param report_path:
    :return:
    '''
    make_env()
    gb = GetBasic(apk_path,device_name)
    lanuch_activity = gb.get_app_activity()
    app_name = gb.get_app_name()
    app_version = gb.get_app_version()
    gb.get_all_activitys()
    InstallApp(device_name,app_name,apk_path,install_app_log,uninstall_app_log).install_app()
    LanuchApp(device_name,app_name,lanuch_activity,lanuch_app_log).lanuch_app()
    LoginApp(device_name, app_name, lanuch_activity,login_caseinfo).test_login()
    Monkey(device_name,runtime,app_name).start_monkey()
    report_path = Create(apk_path,device_name,report_path).create_html()
    SendMail(mail_info, report_path).send_mail()


def load_config(config_path):
    with open(config_path,"r") as f_r:
        yaml_info = yaml.load(f_r)
        return yaml_info


def load_mail_config(yaml_info):
    return yaml_info['mailconfig']

def load_login_case(yaml_info):
    return yaml_info['logincase']



def main_run():
    logger.debug("*****************************************************************")
    parser = argparse.ArgumentParser(
        description='config path')
    parser.add_argument(
        '--config_path',
        help="config路径")

    args = parser.parse_args()
    config_path = str(args.config_path)

    # 配置config路径
    yaml_info = load_config(config_path)
    apk_path = yaml_info['commonconfig']['apkapth']
    device_name = yaml_info['commonconfig']['devicename']
    run_time = yaml_info['commonconfig']['runtime']
    report_path = yaml_info['commonconfig']['reportpath']

    mail_info = load_mail_config(yaml_info)
    login_caseinfo = load_login_case(yaml_info)
    params = (apk_path + '\n' +
              device_name + '\n' +
              run_time)
    logger.info('参数:' + '\n' + '{}'.format(params))
    run(apk_path, device_name, run_time, mail_info, login_caseinfo,report_path)
    logger.debug("*****************************************************************")







