#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 运行Monkey
"""

import os,re,time,sys,subprocess,linecache,shutil,zipfile,glob
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")
import common
from getcpu import GetCPU
from getmem import GetMem
from getbasic import GetBasic
from getnetwork import GetNetWork
from getfps import GetFPS
from ..tools.loggers import JFMlogging
from ..config import *
logger = JFMlogging().getloger()


class Monkey():
    def __init__(self, device_name,runtime,app_name):
        self.device = device_name
        self.runtime = runtime
        self.pkg = app_name
        self.throttle = throttle
        self.runmodel = run_model
        self.monkeyjar = monkey_jar
        self.frameworkjar = framework_jar
        self.crash_savepath = crash_savepath
        self.monkeylog = monkey_log
        self.device_crash_path = device_crash_path
        self.sleep_time = sleep_time

    def make_env(self):
        '''
        初始化环境
        :return:
        '''
        if os.path.exists(local_images_path):
            shutil.rmtree(local_images_path)
        if os.path.exists(images_zip):
            os.remove(images_zip)
        self.del_crash_log()
        self.del_crash_images()
        self.del_logcat()
        common.push_file(self.device, self.monkeyjar, sdcard_path)
        common.push_file(self.device, self.frameworkjar, sdcard_path)
        common.push_file(self.device, max_path,sdcard_path)
        common.kill_pid("Maxim")
        common.kill_pid("logcat")



    def start_monkey(self):
        '''
        启动monkey
        :return:
        '''
        try:
            self.make_env()
            cmd = ("adb -s {} shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec "
                   "app_process /system/bin tv.panda.test.monkey.Monkey "
                   "-p {} --{} --imagepolling --running-minutes {} --throttle {} > {}"
                   .format(self.device,self.pkg,self.runmodel,self.runtime,self.throttle,self.monkeylog))
            logger.info("Monkey执行命令:{}".format(cmd))
            subprocess.Popen(cmd,shell=True)
            is_runing = True
            time.sleep(self.sleep_time)
            while is_runing:
                if self.find_monkey() or self.find_device_monkey() :
                    logger.info("="*10 + "Monkey运行中..." + "="*10)
                    current_activity = common.get_current_activity(self.device)
                    GetCPU(self.device,current_activity,self.pkg).get_cpu()
                    GetMem(self.device,current_activity,self.pkg).get_mem()
                    GetNetWork(self.device,current_activity,self.pkg).get_network()
                    GetFPS(self.device,current_activity,self.pkg).getfps()
                    self.write_page()
                    common.write_activity_back(current_activity)
                    time.sleep(self.sleep_time)
                else:
                    is_runing = False
                    logger.info("="*10 + "Monkey运行结束!" + "="*10)
            self.get_run_activitys()
            common.pull_file(self.device, self.device_crash_path, self.crash_savepath)
            crash_detail = common.read_file(self.crash_savepath)
            if  crash_detail != '':
                image_path = self.get_crash_images()
                if image_path != '':
                    common.pull_file(self.device,image_path,local_images_path)
                    self.rename_image()
        except Exception as e:
            logger.error('Monkey运行异常!{}'.format(e))


    def find_crash_log(self):
        '''
        查询crash-dump.log文件
        :return:0表示不存在,1表示存在
        '''
        try:
            cmd = 'adb -s {} shell find -name {}'.format(self.device, 'crash-dump.log')
            logger.info('查询crash log命令: ' + cmd)
            result = os.popen(cmd).read()
            if result == '' or result ==None:
                logger.info('{}设备中未查询到崩溃'.format(self.device))
                return 0
            else:
                logger.info('{}设备中查询到崩溃'.format(self.device))
                return 1
        except Exception as e:
            logger.info('{}设备中查询崩溃异常:{}'.format(self.device,e))
            return 0


    def write_page(self):
        '''
        页面加载时间
        :return:
        '''
        try:
            cmd = 'adb -s {} logcat -d | grep -i activitymanager.*Displayed'.format(self.device)
            result = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE).stdout.read()
            if result != None or result != '':
                with open(page_path,'a') as f:
                    f.write(result)
        except Exception as e:
            logger.error("页面加载时间写入失败!{}".format(e))


    def del_crash_log(self):
        '''
        删除crash-dump.log文件
        :return:
        '''
        try:
            cmd = 'adb -s {} shell rm -rf {}'.format(self.device, device_crash_path)
            logger.info('删除设备中crash命令:{}'.format(cmd))
            subprocess.call(cmd,shell=True)
        except Exception as e:
            print '删除设备中crash异常:{}'.format(e)


    def get_run_activitys(self):
        '''
        获取运行的Activitie列表
        :return:个数,接口列表
        '''
        startnumber = None
        endnumber = None
        actlen = None
        actlist = []

        try:
            with open(self.monkeylog) as f_w:
                result =  f_w.read()
                if re.findall("Total activities", result) and re.findall("How many Events Dropped", result):
                    with open(self.monkeylog) as f_w:
                        for number,line in  enumerate(f_w.readlines()):
                            if re.findall("Total activities",line):
                                actlen = line.split("Total activities")[1].replace("\n","").strip()
                                startnumber = number + 1
                            elif re.findall("How many Events Dropped",line):
                                endnumber = number
                        act_result = linecache.getlines(self.monkeylog)[startnumber:endnumber]
                        for act in act_result:
                            actlist.append(str(act).split("-")[1].replace("\n","").strip())
                else:
                    logger.info("{}文件中未查询到activity列表".format(self.monkeylog))
                common.write_file(run_activity_path, actlist)
        except Exception as e:
            logger.error('获取activity列表异常:{}'.format(e))
        finally:
            return actlen, actlist


    def find_device_monkey(self):
        '''
        查询设备monkey的pid
        :return:
        '''
        is_alive = False
        try:
            grep_cmd = "adb -s {} shell ps | grep monkey".format(self.device)
            pipe = os.popen(grep_cmd)
            pids = pipe.read()
            if pids == '':
               logger.info("当前monkey进程不存在")
            else:
               pid = pids.split()[1]
               is_alive = True
               logger.info("当前monkey进程pid:{}".format(pid))
        except Exception as e:
            logger.error("当前monkey进程查询异常!{}".format(e))
        finally:
            return is_alive


    def find_monkey(self):
        '''
        查询设备monkey的pid
        :return:
        '''
        is_alive = False
        try:
            grep_cmd = 'ps | grep tv.panda.test.monkey.Monkey | grep -v "grep"'
            pipe = os.popen(grep_cmd)
            pids = pipe.read()
            if pids == '':
               logger.info("当前monkey进程不存在")
            else:
               is_alive = True
        except Exception as e:
            logger.error("当前monkey进程查询异常!{}".format(e))
            return 1
        finally:
            return is_alive




    def get_performance(self):
        '''
        采集性能
        :return:
        '''
        try:
            cmd = "sh {} {} {}".format(get_performance_path, self.device,performance_folder,self.pkg)
            subprocess.call(cmd, shell=True)
        except Exception as e:
            logger.error("获取性能异常!{}".format(e))


    def del_crash_images(self):
        '''
        删除设备中崩溃的缓存图片
        :return:
        '''
        try:
            cmd = 'adb -s {} shell rm -rf {}'.format(self.device,device_crash_image)
            subprocess.call(cmd,shell=True)
        except Exception as e:
            logger.error('删除图片异常!{}'.format(e))


    def get_crash_images(self):
        '''
        获取设备中崩溃的缓存图片地址
        :return:
        '''
        image_path = ''
        root_path = "./data/media/0"
        try:
            cmd = 'adb -s {} shell ls {}'.format(self.device,root_path)
            result = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE).stdout.readlines()
            logger.info(cmd)
            for line in result:
                if 'Crash_' in line:
                    image_path = os.path.join(root_path,line).replace("\n","")
                    logger.info('崩溃图片路径:{}'.format(image_path))
                    break
        except Exception as e:
            logger.error('删除图片异常!{}'.format(e))
        finally:
            return image_path


    def del_logcat(self):
        '''
        清除logcat日志
        :return:
        '''
        try:
            cmd = 'adb -s {} logcat -c'.format(self.device)
            result = subprocess.Popen(cmd, shell=True)
            logger.info('清除logcat日志')
        except Exception as e:
            logger.error('清除logcat日志异常!{}'.format(e))


    def rename_image(self):
        '''
        重命名崩溃图片文件夹
        :return:
        '''
        try:
            class_path = os.path.abspath(os.path.dirname(__file__))
            for file_name in os.listdir(class_path):
                if 'Crash_' in file_name:
                    os.rename(file_name, local_images_path)
        except Exception as e:
            logger.error('重命名文件失败!{}'.format(e))


    def zip_image(self):
        '''
        压缩图片成zip
        :return:
        '''
        zip_path = ''
        try:
            files = glob.glob('./images/*')
            f = zipfile.ZipFile(images_zip, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                f.write(file)
            f.close()
            logger.info('压缩图片成功!')
            zip_path = './images.zip'
        except Exception as e:
            logger.error('压缩图片失败!{}'.format(e))
        finally:
            return zip_path


    def get_current_activity(self):
        '''
        获取当前的Activity
        '''
        activity = 'undefined'
        try:
            cmd = 'adb -s {} shell dumpsys activity | grep "mFocusedActivity"'.format(self.devices)
            activity = str(os.popen(cmd).readlines()).split('/')[1].split()[0]
        except Exception, e:
            logger.error("获取当前activity异常!{}".format(e))
        finally:
            return activity