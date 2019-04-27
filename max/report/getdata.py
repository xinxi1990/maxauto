#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 获取运行后数据
"""

import os,re,sys,base64
sys.path.append('..')
from ..tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from bs4 import BeautifulSoup
from ..config import *


class GetData():

    def get_login(self):
        '''
        获取登录结果
        :return:
        '''
        result = 'error'
        try:
            with open(logintest_app_log) as f:
                result = f.readlines()[0].replace('\n','')
        except Exception as e:
            logger.error("获取登录数据异常!{}".format(e))
        finally:
            return result


    def get_install_time(self):
        '''
        获取安装耗时数据
        :return:
        '''
        result = "0"
        try:
            with open(install_app_log) as f:
                result = f.readlines()[0].replace('\n','')
        except Exception as e:
            logger.error("获取安装耗时数据异常!{}".format(e))
        finally:
            return result


    def get_lanuch_time(self):
        '''
        获取冷启动数据
        :return:
        '''
        result = "0"
        try:
            with open(lanuch_app_log) as f:
                result = f.readlines()[0].replace('\n','')
        except Exception as e:
            logger.info("获取冷启动数据异常!{}".format(e))
        finally:
            return result


    def get_crash_detail(self):
        '''
        获取崩溃信息
        :return:
        '''
        result = '暂无数据!'
        try:
            with open(crash_savepath, "r") as f_r:
                for line in f_r.readlines():
                    result += line.replace('\n', '').replace('\t', '') + '\n'
        except Exception as e:
            logger.error("{}读取异常!{}".format(e))
        finally:
            return result


    def get_crash_count(self):
        '''
        获取crash的次数
        :return:
        '''
        crash_count = 0
        try:
            with open(crash_savepath,"r") as f_r:
                for line in f_r.readlines():
                    if re.findall("end",line):
                        crash_count+=1
        except Exception as e:
            logger.error("获取crash次数异常!{}".format(e))
        finally:
            return crash_count


            logger.error("获取崩溃日志地址失败!{}".format(e))


    def get_all_activitys(self):
        '''
        获取app中所有的activity
        :return:activitylist和activitylist的个数
        '''
        try:
            with open(all_activity_path) as r:
                activitylist = r.readlines()
            return activitylist, len(activitylist)
        except Exception as e:
            logger.error("获取activitys异常!{}".format(e))
            activitylist = []
            return activitylist,len(activitylist)



    def get_run_activitys(self):
        '''
        获取已经执行的activity
        :return:activity个数
        '''
        actlist = []
        try:
            with open(run_activity_path,"r") as f_r:
               for line in  f_r.readlines():
                   actlist.append(line.replace("\n",""))
        except Exception as e:
            logger.error("获取运行的activity异常!{}".format(e))
        finally:
            return actlist, len(actlist)


    def get_calculate_coverage(self):
        '''
        计算自动化遍历覆盖率
        :return:覆盖率,未覆盖率
        '''
        try:
            run_list = self.get_run_activitys()[1]
            all_list = self.get_all_activitys()[1]
            coverage = float(run_list) / float(all_list)
            coverage_percent =  round(coverage * 100,1)
            not_coverage_percent = 100 - round(coverage * 100,1)
            return coverage_percent,not_coverage_percent
        except Exception as e:
            logger.error('计算遍历覆盖率异常!{}'.format(e))
            return '0','100'


    def get_run_pages(self):
        '''
        获取遍历的页面列表
        :return:
        '''
        try:
            with open(run_activity_path, "r") as f_r:
                activitylist = f_r.readlines()
            doneinfo = ''
            for index,act in  enumerate(activitylist):
                    tr = """
                        <tr>
                        <td align="center">{}</td>
                        <td align="center">{}</td>
                        <td align="center"><font color="blue">{}</font></td>
                        </tr>
                        """.format(index,act, "已遍历")
                    doneinfo +=tr
            return doneinfo
        except Exception as e:
            logger.error("获取遍历的页面列表异常!{}".format(e))
            return ""


    def get_runtime(self):
        '''
        获取遍历运行时间
        :return:
        '''
        runtime = 0
        try:
            with open(monkey_log) as f_r:
                for line in  f_r.readlines():
                    if re.findall("elapsed time= ",line):
                        runtime = line.split("elapsed time= ")[1].split(" ms")[0]
                        runtime = round(float(runtime) / 1000,1)
        except Exception as e:
            logger.error("获取monkey运行时间异常!{}".format(e))
        finally:
            return "{}秒".format(runtime)


    def get_click_count(self):
        '''
        获取元素点击数量
        :return:
        '''
        clickcount = 0
        try:
            with open(monkey_log) as f_r:
                for line in  f_r.readlines():
                    if re.findall("Events injected: ",line):
                        clickcount = line.split("Events injected: ")[1]
        except Exception as e:
            logger.error("获取Monkey点击次数异常!{}".format(e))
        finally:
            return clickcount


    def get_crash_image(self):
        '''
        获取崩溃图片,图片是base位编码
        :return:
        '''
        crash_image = "暂无图片"
        total_image = ''
        try:
            folder = os.listdir(local_images_path)
            if len(folder) != 0:
                for image_path in folder:
                    image_path = os.path.join(local_images_path, image_path)
                    with open(image_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    crash_image = '<img src="data:image/png;base64,{}" alt="image" height="400" width="200"/>'.format(encoded_string)
                    total_image += crash_image
        except Exception as e:
            logger.error("获取崩溃图片异常!{}".format(e))
        finally:
            return total_image


    def get_pagestime_list(self):
        '''
        获取页面响应时间列表
        :return:
        '''
        number = 0
        NewStr = ""
        try:
            if os.path.exists(self.PagesTimeList):
                with open(self.PagesTimeList) as f_r:
                    for index, line in enumerate(f_r.readlines()):
                        number += 1
                        line = line.replace("\n","")
                        ActName = line.split(",")[0]
                        SpeedTime = line.split(",")[1]
                        tr = """
                            <tr>
                            <td align="center">{}</td>
                            <td align="center">{}</td>
                            <td align="center">{}</td>
                            </tr>
                            """.format(number,ActName,SpeedTime)
                        NewStr += tr
            return NewStr
        except Exception as e:
            logger.error("获取页面响应时间列表异常!{}".format(e))



