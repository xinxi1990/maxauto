#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 启动app测试
"""
from __future__ import division
import re,json,subprocess,time,sys,os
sys.path.append('..')
from ..tools.loggers import JFMlogging
from ..tools.filetools import write_file
logger = JFMlogging().getloger()
from ..config import *

class LanuchApp():
    def __init__(self,device_name,pck_name,lanuch_activity,lanuch_app_log):
        self.device_name = device_name
        self.pck_name = pck_name
        self.lanuch_activity = lanuch_activity
        self.lanuch_loop = 1
        self.lanuch_timelist = []
        self.lanuch_app_log = lanuch_app_log


    def clear_app(self):
        '''
        清除数据缓存
        :return:
        '''
        try:
            clear_cmd = 'adb -s {} shell pm clear {}'.format(self.device_name,self.pck_name)
            subprocess.call(clear_cmd,shell=True)
            logger.info('清除数据缓存命令:{}'.format(clear_cmd))
        except Exception as e:
            logger.info('清除数据缓存异常:{}'.format(e))


    def lanuch_app(self):
        '''
        冷启动多次计算平均时间
        :return:
        '''
        lanuch_result = 'fail'
        try:
            while self.lanuch_loop > 0:
                self.clear_app()
                lanuch_cmd = 'adb -s {} shell am start -W {}/{}'.\
                    format(self.device_name,self.pck_name,self.lanuch_activity)
                lanuch_info = subprocess.Popen(lanuch_cmd,shell=True,
                                               stdout=subprocess.PIPE).stdout.readlines()
                logger.info('启动app命令:{}'.format(lanuch_cmd))
                for line in lanuch_info:
                    if re.findall('TotalTime',line):
                        lanuch_time = str(line).split(':')[1].strip()
                        logger.info('本次冷启动时间:{}'.format(lanuch_time))
                        self.lanuch_timelist.append(lanuch_time)
                self.lanuch_loop -=1
                time.sleep(3)
            lanuch_time = self.get_avg_time(self.lanuch_timelist)
            lanuch_result = "{}".format(round(lanuch_time/1000,2))
        except Exception as e:
            logger.info('启动时间计算异常!:{}'.format(e))
        finally:
            write_file(self.lanuch_app_log, lanuch_result, is_cover=True)



    def get_avg_time(self,list):
        '''
        计算平均时间
        :param list:
        :return:
        '''
        try:
            list_length = len(list)
            sum = 0
            for i in list:
                sum = sum + int(i)
            avg = sum/list_length
            logger.info("均值为:{}".format(avg))
            return avg
        except Exception as e:
            return '0'


if __name__ == '__main__':
    device = sys.argv[1]
    LanuchApp(device,lanuch_app_log).lanuch_app()