#!/usr/bin/env python
# -*- coding: utf-8 -*-

from monkey.getbasic import GetBasic
from monkey.monkey import Monkey
from lanuchtest.lanuchapp import LanuchApp
from Installtest.installapp import InstallApp
from config import *

def run(apk_path,device_name,runtime):

    if os.path.exists(android_tmp):
        shutil.rmtree(android_tmp)
        logger.info('删除缓存目录:{}'.format(android_tmp))
    os.makedirs(android_tmp)
    logger.info('创建缓存目录:{}'.format(android_tmp))

    gb = GetBasic(apk_path,device_name)
    lanuch_activity = gb.get_app_activity()
    app_name = gb.get_app_name()
    app_version = gb.get_app_version()
    # InstallApp(device_name,app_name,apk_path,install_app_log,uninstall_app_log).install_app()
    # LanuchApp(device_name,app_name,lanuch_activity,lanuch_app_log).lanuch_app()
    Monkey(device_name,runtime,app_name).start_monkey()



if __name__ == '__main__':
    apk_path = "/Users/xinxi/Downloads/app_debug_5.2.0_20181120201645.apk"
    device_name = "192.168.56.101:5555"
    run_time = 1
    run(apk_path,device_name,run_time)

