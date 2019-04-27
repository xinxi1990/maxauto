# coding=utf-8



#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 获取设备内存
Naitve Heap Size 代表最大总共分配空间
Native Heap Alloc 已使用的内存
Native Heap Free  剩余内存
Naitve Heap Size约等于Native Heap Alloc + Native Heap Free
"""

import time,os,sys,subprocess,re
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")
from ..tools.loggers import JFMlogging
from ..tools.filetools import write_file
logger = JFMlogging().getloger()
from ..config import mem_path

class GetMem():

    def __init__(self, device_name,activity,pck_name):
        self.device_name = device_name
        self.pck_name = pck_name
        self.activity = activity

    def get_mem(self):
        '''
        获取内存
        :return:
        '''
        mem = ''
        try:
            cmd = "adb -s {} shell dumpsys meminfo {}".format(self.device_name, self.pck_name)

            result = subprocess.Popen(cmd, shell=True,
                                      stdout=subprocess.PIPE).stdout.readlines()
            for line in result:
                if line.startswith('  Dalvik Heap'):
                    mem =  float(line.split()[3])/ 1024
                    mem = round(mem,2)
        except Exception, e:
            logger.error("获取内存失败:{}".format(e))

        finally:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            info =  current_time + ',' + str(mem) + ',' + self.activity + '\n'
            write_file(mem_path,info,is_cover=False)


