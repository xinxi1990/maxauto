#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 常用操作封装
"""

import os,sys,subprocess,re
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")
from ..tools.loggers import JFMlogging
from ..tools.filetools import write_file
from ..tools.filetools import read_file
from ..config import run_activity_path_back
logger = JFMlogging().getloger()


def pull_file(device, remotefile, localfile):
    '''
    把crashlog pull到本地
    :return:
    '''
    try:
        cmd = 'adb -s {} pull {} {}'.format(device, remotefile, localfile)
        logger.info('拉取文件命令:{}'.format(cmd))
        os.system(cmd)
        # subprocess.Popen(cmd, shell=True)
    except Exception as e:
        logger.info('拉取文件异常:{}'.format(e))


def push_file(device, localfile, remotefile):
    '''
    push本地文件到设备
    :return:
    '''
    try:
        cmd = 'adb -s {} push {} {}'.format(device, localfile, remotefile)
        logger.info('push本地文件到设备命令:{}'.format(cmd))
        subprocess.call(cmd, shell=True)
    except Exception as e:
        logger.info('push本地文件异常:{}'.format(e))

def kill_pid(keyword):
    '''
    结束进程
    :param keyword:
    :return:
    '''
    try:
        cmd = "ps -ef | grep {} | grep -v grep".format(keyword)
        pids = os.popen(cmd).read()
        if pids == '' or pids == None:
            logger.info("未查询到pid")
        else:
            pids = str(pids).split()[1]
            subprocess.call("kill -9 {}".format(pids), shell=True)
            logger.info("结束:{},进程号:{}".format(keyword, pids))
    except Exception as e:
        logger.info("kill pid异常!{}".format(e))

def unlock_screen(device):
    '''
    唤醒屏幕
    :return:
    '''
    result=os.popen("adb -s {} shell dumpsys window policy "
                    "| grep isStatusBarKeyguard".format(device)).readlines()
    if "isStatusBarKeyguard=true" in result[0]:
        logger.info("screen start wakup!")
        os.system("adb shell input keyevent 26")
    else:
        logger.info("screen already wakup!")



def del_files(filesname):
    '''
    删除文件
    :param filesname:
    :return:
    '''

    try:
        if os.path.exists(filesname):
            subprocess.call("rm -rf {}".format(filesname), shell=True)
        logger.info("删除{}完成!".format(filesname))
    except Exception as e:
        logger.info("删除文件异常!".format(e))


def write_file(filename,content):
    '''
    写入文件
    :param filename:
    :param content:
    :return:
    '''
    try:
       newstr = ""
       if isinstance(content,list or tuple):
          for str in content:
              newstr = newstr + str + "\n"
       else:
           newstr = content
       with open(filename,"ab+") as f_w:
          f_w.write(newstr)
       logger.info("写{}文件完成".format(filename))
    except Exception as e:
       logger.info("{}写入异常!{}".format(e))


def read_file(filename):
    '''
    读取文件
    :return:
    '''
    result = ''
    try:
        with open(filename,"r") as f_r:
            for line in  f_r.readlines():
                result+= line.replace('\n','').replace('\t','') + '\n'
    except Exception as e:
        logger.error("{}读取异常!{}".format(e))
    finally:
        return result


def format_time(time_str):
    '''
    格式化时间
    :param time_str:
    :return:
    '''
    try:
      if re.findall('total',time_str):
          time_str = time_str.replace('ms','')
          time_str = time_str.split('(')[0].strip()
          if re.findall('s',time_str):
             new_time_m = str(time_str).split('s')[0]
             new_time_s = str(time_str).split('s')[1]
             new_time = int(new_time_m) * 1000 + int(new_time_s)
          else:
             new_time = time_str
      else:
          time_str = time_str.replace('ms', '')
          if re.findall('s',time_str):
             new_time_m = str(time_str).split('s')[0]
             new_time_s = str(time_str).split('s')[1]
             new_time = int(new_time_m) * 1000 + int(new_time_s)
          else:
             new_time = time_str
    except Exception as e:
        logger.error('格式化时间异常!{}'.format(e))
        new_time = 0
    finally:
        return new_time



def get_current_activity(device_name):
    '''
    获取当前的Activity
    '''
    activity = 'undefined'
    try:
        cmd = 'adb -s {} shell dumpsys activity | grep "mFocusedActivity"'.format(device_name)
        activity = str(os.popen(cmd).readlines()).split('/')[1].split()[0]
    except Exception, e:
        logger.error("获取当前activity异常!{}".format(e))
    finally:
        return activity


def get_app_pid(device_name,app_name):
    '''
    获取app的pid
    '''
    pid = ''
    try:
        cmd = 'adb -s {} shell ps | grep {}'.format(device_name,app_name)
        pid = os.popen(cmd).readlines()[0].split()[1]
    except Exception, e:
        logger.error("获取当前activity异常!{}".format(e))
    finally:
        return pid


def get_app_uid(device_name,pkg_name):
    '''
    根据包名得到进程id
    :return: 0表示未获取到,uid是设备的真实uid
    '''
    uid = ''
    try:
        pid = get_app_pid(device_name,pkg_name)
        cmd = "adb -s {} shell cat /proc/{}/status".format(device_name,pid)
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
        for line in result:
            if line.startswith('Uid'):
                uid =  line.split()[1]
    except Exception, e:
        logger.error("获取进程id异常{}".format(e))
    finally:
        return uid


def write_activity_back(activity):
    '''
    写备份运行的activity
    :return:
    '''
    try:
        result = read_file(run_activity_path_back)
        if result != '':
            if not re.findall(activity,result):
                write_file(run_activity_path_back,activity + '\n')
            else:
                logger.info("已经存在activity!")
        else:
            write_file(run_activity_path_back, activity + '\n')
    except Exception as e:
        logger.error("备份运行的activity写入异常!{}".format(e))
