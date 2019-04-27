#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 安装app测试
"""

import os,re,sys,time,subprocess,json
sys.path.append('..')
reload(sys)
from ..tools.filetools import write_file
from ..tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from findapp import *

class InstallApp():
    def __init__(self,device_name,pck_name,app_path,install_app_log,uninstall_app_log):
        self.device_name = device_name
        self.pck_name = pck_name
        self.app_path = app_path
        self.install_app_log = install_app_log
        self.uninstall_app_log = uninstall_app_log
        self.max_time = 30


    def install_app(self):
        """
        先卸载旧app,再安装新app
        :return:
        """
        install_result = 'fail'
        try:
            uninstall_cmd = 'adb -s {} uninstall {}'.format(self.device_name,self.pck_name)
            subprocess.call(uninstall_cmd,shell=True)
            logger.info('卸载app命令:{}'.format(uninstall_cmd))
            install_cmd = 'adb -s {} install {}'.format(self.device_name,self.app_path)
            subprocess.Popen(install_cmd, shell=True)
            logger.info('安装app命令:{}'.format(install_cmd))
            starttime = self.record_time()
            endtime = 0
            no_install = True
            install_recordtime = 0
            while no_install:
                find_cmd = 'adb -s {} shell pm list packages | grep {}'.format(self.device_name,self.pck_name)
                #logger.info('查询app安装命令:{}'.format(find_cmd))
                result = subprocess.Popen(find_cmd, shell=True,stdout=subprocess.PIPE).stdout.readlines()
                time.sleep(1)
                if re.findall(self.pck_name,str(result)):
                    logger.info('app安装成功!')
                    no_install = False
                    endtime = self.record_time()
                    install_time = str(endtime - starttime)
                    logger.info('app安装耗时:{}s'.format(install_time))
                    install_result = "{}".format(install_time)
                else:
                    logger.info('app安装中!')
                    install_recordtime +=1
                    if install_recordtime >= self.max_time:
                        logger.info('app安装超过最长时间:{}!'.format(self.max_time))
                        no_install = False
        except Exception as e:
            logger.info('app安装异常:{}'.format(e))
        finally:
            write_file(self.install_app_log, install_result, is_cover=True)


    def uninstall_app(self):
        """
        仅卸载app
        :return:
        """
        uninstall_result = 'fail'
        try:
            uninstall_cmd = 'adb -s {} uninstall {}'.format(self.device_name, self.pck_name)
            subprocess.call(uninstall_cmd, shell=True)
            no_uninstall = True
            uninstall_recordtime = 0
            while no_uninstall:
                find_cmd = 'adb -s {} shell pm list packages | grep {}'.format(self.device_name, self.pck_name)
                #logger.info('查询app安装命令:{}'.format(find_cmd))
                result = subprocess.Popen(find_cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
                if not re.findall(self.pck_name, str(result)):
                    logger.info('app卸载成功!')
                    no_uninstall = False
                    uninstall_result = 'success'
                else:
                    logger.info('app卸载中!')
                    uninstall_recordtime +=1
                    if uninstall_recordtime >= self.max_time:
                        logger.info('app卸载超过最长时间:!'.format(self.max_time))
                        no_uninstall = False
        except Exception as e:
            logger.info('app卸载异常!'.format(e))
        finally:
            write_file(self.uninstall_app_log, uninstall_result, is_cover=True)


    def record_time(self):
        '''
        时间戳记时
        :return:
        '''
        record_time = int(abs(round(time.time(), 0)))
        return record_time





