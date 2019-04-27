#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 查询app路径
"""

import os,re
from loggers import JFMlogging
logger = JFMlogging().getloger()


def find_app(folder_path):
    app_path = ''
    if str(folder_path).endswith("apk"):
        app_path= folder_path
    else:
        for file in os.listdir(folder_path):
            if file.startswith('app_'):
                app_path = os.path.join(folder_path,file)
                logger.info('app路径:{}'.format(app_path))
                break
    return app_path


def find_device():
    '''
    查询运行的设备号
    :return:
    '''
    device_name = ''
    result = os.popen('adb devices').readlines()
    for line in result:
        if re.findall('device',line) and not re.findall('List of devices attached',line):
            device_name = line.split()[0]
            logger.info('查询到设备号:{}'.format(device_name))
            break
    return device_name



