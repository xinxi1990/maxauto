#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 获取报告
"""

import os,re,time,subprocess,sys,requests
sys.path.append('..')
from config import *
from tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from sendmail import SendMail

def make_env():
    '''
    初始化环境
    :return:
    '''
    if not os.path.exists(report_folder):
        os.mkdir(report_folder)

def get_html(apk_path,device_name,mail_list):
    '''
    获取报告
    :return:
    '''
    try:
        logger.info("开始获取报告!")
        make_env()
        data = {'apk_path': apk_path,'device_name': device_name}
        print api
        r = requests.post(api,json=data,timeout=3)
        logger.info("服务端状态码:{}".format(r.status_code))
        if r.status_code == 200:
            with open(report_path, 'wb+') as f:
                f.write(r.content)
            logger.info('报告路径:{}'.format(report_path))
            SendMail(mail_list, report_path).send_mail()
            logger.info('发送完成报告!')
        else:
            logger.info('报告获取失败!服务端状态码{}'.format(r.status_code))
    except Exception as e:
        logger.error('报告获取失败!' + '\n' + str(e))

