#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re,time,subprocess,sys
sys.path.append('..')
from server import *
from client import *
from config import *
from findapp import *


if __name__ == '__main__':
    app_folder = sys.argv[1]
    apkpath = find_app(app_folder)
    devices = sys.argv[2]
    android_project = sys.argv[3]
    receive_list = sys.argv[4]
    env = sys.argv[5]
    version = sys.argv[6]
    logger.info('apk路径:{}'.format(apkpath))
    logger.info('设备名称:{}'.format(devices))
    logger.info('android工程路径:{}'.format(android_project))
    logger.info('邮件收件人列表:{}'.format(receive_list))
    logger.info('环境:{}'.format(env))
    logger.info('版本:{}'.format(version))

    def task(**kwargs):
        '''
        定义两个线程,用来做异步操作
        :return:
        '''

        try:
            def async(f):
                def wrapper(*args, **kwargs):
                    thr = Thread(target=f, args=args, kwargs=kwargs)
                    thr.start()
                return wrapper

            @async
            def async_gethtml():
                #find_flask()
                time.sleep(5)
                get_html(kwargs['apkpath'],kwargs['devices'],
                        kwargs['android_project'],kwargs['receive_list']
                         ,kwargs['env'],kwargs['version'])

            def async_runflask():
                stop_flask()
                run_flask()
            async_gethtml()
            async_runflask()
        except Exception as e:
            logger.error('task异常!{}'.format(e))

    task(apkpath=apkpath,devices=devices,
         android_project=android_project,
         receive_list=receive_list,env=env,
         version=version)


