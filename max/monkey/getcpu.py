#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 获取设备cpu
"""

import time,os,re,subprocess
from ..tools.loggers import JFMlogging
from ..tools.filetools import write_file
logger = JFMlogging().getloger()
from ..config import cpu_path

class GetCPU():

    def __init__(self, device_name,activity,pck_name):
        self.device_name = device_name
        self.pck_name = pck_name
        self.activity = activity

    def get_cpu_kel(self):
        ''''
        # 得到几核cpu
        '''
        cmd = "adb -s " + self.dev + " shell cat /proc/cpuinfo"
        process = (os.popen(cmd))
        output = process.read()
        res = output.split()
        num = re.findall("processor", str(res))
        return len(num)


    def get_cpu(self):
        '''
        统计cpu的占用率
        :return:
        '''
        cpu = 0
        try:
            cmd = "adb -s {} shell dumpsys cpuinfo | grep {}".format(self.device_name,self.pck_name)
            result = subprocess.Popen(cmd, shell=True,
                                           stdout=subprocess.PIPE).stdout.readlines()
            for line in result:
                if re.findall(self.pck_name,line):
                    cpu = line.split()[0].replace('%', '')
                    break
        except Exception, e:
            logger.error("获取cpu失败:{}".format(e))
        finally:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            info = current_time + ',' + str(cpu) + ',' + self.activity  + '\n'
            write_file(cpu_path, info, is_cover=False)


if __name__ == '__main__':
    GetCPU('192.168.56.101:5555','xxxx','com.tencent.news').get_cpu()



