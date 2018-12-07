# coding=utf-8


'''

获取设备流量
上行+下行
模拟和真机获取方式不一样
@author xinxi

'''
from AdbCommon import AdbCommon
import subprocess
from DateBean import DateBean
import logger
import time

total = 0


class GetNetWork():

    def __init__(self, dev):
        self.dev = dev
        self.db = DateBean()

    def getnetwork(self,activity):
        '''
        获取真机的流量
        获取上传和下载的流量
        :return:
        '''
        adc = AdbCommon(self.dev)

        global total
        try:

            uid = adc.get_app_uid(self.db.packagename)
            # 获取uid

            cmd = 'adb -s %s shell  cat /proc/uid_stat/%s/tcp_snd' % (self.dev, uid)
            # 上传流量
            logger.log_debug(cmd)

            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
            updata = int(pipe.read().split('/')[0])

            cmd = 'adb -s %s shell  cat /proc/uid_stat/%s/tcp_rcv' % (self.dev, uid)
            logger.log_debug(cmd)
            # 下载流量

            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
            downdata = int(pipe.read().split('/')[0])

            total = (format(float(updata + downdata) / float(1024 * 1024), '.3f'))

        except  Exception, e:
            logger.log_error('获取真机流量失败:%s' + str(e))
            total = 0

        finally:

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 发生时间
            with open(self.db.networkpath, 'ab+') as f:
                f.write(
                    str(times) + ',' +
                    str(total) + ',' +
                    str(activity) + ',' + '\n'
                )

    def simulatorgetnetwork(self,activity):
        '''
        获取模拟器的流量
        获取上传和下载的流量
        :return:
        '''
        global total

        adc = AdbCommon(self.dev)

        try:
            uid = adc.get_app_pid(self.db.packagename)

            cmd = 'adb -s %s shell  cat /proc/%s/net/dev' % (self.dev, uid)
            # 获取流量命令
            logger.log_debug(cmd)

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
            logger.log_error('获取模拟器流量失败:%e' + str(e))
            total = 0

        finally:

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 发生时间

            with open(self.db.networkpath, 'ab+') as f:
                f.write(
                    str(times) + ',' +
                    str(total) + ',' +
                    str(activity) + ',' + '\n'
                )

    def selectnetwork(self,simulator,activity):
        '''
        选择真机或者模拟器获取流量的方法
        :param simulator: 取Path.py中的simulator的参数
        :return:
        '''

        logger.log_info("simulator: " + str(simulator))

        if simulator:
            self.simulatorgetnetwork(activity)
        else:
            self.getnetwork(activity)




