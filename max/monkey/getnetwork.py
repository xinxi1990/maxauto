#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 统计消耗流量
上行+下行
模拟和真机获取方式不一样
'''

import subprocess,time,re,sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")
from ..tools.loggers import JFMlogging
from ..config import *
from common import get_app_uid
from common import get_app_pid
logger = JFMlogging().getloger()
from ..tools.filetools import write_file


class GetNetWork():

    def __init__(self, device_name,activity,pck_name):
        self.device_name = device_name
        self.activity = activity
        self.pck_name = pck_name

    def real_network(self):
        '''
        获取真机的流量
        获取上传和下载的流量
        :return:
        '''
        total = ''
        try:
            uid = get_app_uid(self.device_name, self.pck_name)
            # 获取uid
            cmd = 'adb -s %s shell  cat /proc/uid_stat/%s/tcp_snd' % (self.device_name, uid)
            # 上传流量
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
            updata = int(pipe.read().split('/')[0])
            cmd = 'adb -s %s shell cat /proc/uid_stat/%s/tcp_rcv' % (self.device_name, uid)
            # 下载流量
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
            downdata = int(pipe.read().split('/')[0])
            total = (format(float(updata + downdata) / float(1024 * 1024), '.3f'))
        except  Exception, e:
            logger.error('获取真机流量失败:%s' + str(e))
        finally:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 发生时间
            info = current_time + ',' + str(total)  + ',' + self.activity + ',' + '\n'
            write_file(network_path, info, is_cover=False)



    def simu_network(self):
        '''
        获取模拟器的流量
        获取上传和下载的流量
        :return:
        '''
        total = ''
        try:
            pid = get_app_pid(self.device_name,self.pck_name)
            cmd = 'adb -s %s shell cat /proc/%s/net/dev' % (self.device_name, pid)
            # 获取流量命令
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
            for index in pipe.readlines():
                # if index.startswith(' wlan0'): # 真机
                if 'eth0' in index:  # 模拟器
                    down = index.split()[1]
                    # 下载
                    send = index.split()[9]
                    # 上传
                    total = (int(down) + int(send)) / (1024 * 1024)
                    # 上传和下载
        except  Exception, e:
            logger.error('获取模拟器流量失败:{}'.format(e))
        finally:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 发生时间
            info = current_time + ',' + str(total) + ',' + self.activity + ',' + '\n'
            write_file(network_path, info, is_cover=False)


    def get_network(self):
        if re.findall(':',self.device_name):
            self.simu_network()
        else:
            self.real_network()





