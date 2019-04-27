#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 获取运行后数据
"""

import os,re,sys,base64,json
from bs4 import BeautifulSoup
from filetools import *
sys.path.append('..')
from loggers import JFMlogging
logger = JFMlogging().getloger()
from config import *


class GetData():

    def __init__(self):
        self.info = read_file(out_json_path)


    def get_size(self,org):
        '''
        计算apk大小
        :return:
        '''
        new = str(round(float(org) / (1024 * 1024),2))
        return new


    def get_base(self):
        '''
        获取基础信息
        :return:
        '''
        self.base_data = {}
        try:
            self.result = json.loads(self.info)[0]
            self.base_data['start-time'] = self.result['start-time']
            self.base_data['end-time'] = self.result['end-time']
            self.base_data['apksize'] =  self.get_size(self.result['total-size'])
            self.base_data.update()
        except Exception as e:
            logger.error("获取基础信息异常!{}".format(e))
        finally:
            return self.base_data


    def get_entries(self):
        '''
        获取文件资源分布
        :return:
        '''
        self.data_list = []
        self.data = {}
        try:
            entries = json.loads(self.info)[0]['entries']
            for info in entries:
                self.data = {}
                self.data['name'] = info['suffix']
                self.data['size'] = info['total-size']
                # for file in  info['files']:
                #     self.data['文件名字'] = file['entry-name']
                #     self.data['文件大小'] = file['entry-size']
                self.data_list.append(self.data)
        except Exception as e:
            logger.error("获取资源分布信息异常!{}".format(e))
        finally:
            return self.data_list


    def get_pkg_info(self):
        '''
        获取包相关信息
        :return:
        '''
        self.base_data = {}
        try:
            self.result = json.loads(self.info)[1]['manifest']
            self.base_data['package'] = self.result['package']
            self.base_data['versionName'] = self.result['android:versionName']
            self.base_data['minSdkVersion'] = self.result['android:minSdkVersion']
            self.base_data['targetSdkVersion'] = self.result['android:targetSdkVersion']
            self.base_data.update()
        except Exception as e:
            logger.error("获取包相关信息异常!{}".format(e))
        finally:
            return self.base_data



    def make_entries(self):
        '''
        组装资源分布
        :return:
        '''
        entries_list = self.get_entries()
        total_info = ''
        try:
            for entries in entries_list:
                info = "name:'{}',y:{}".format(entries['name'],entries['size'])
                info = "{ " + info + " }," + "\n"
                total_info += info
        except Exception as e:
            logger.error("组装资源分布异常!{}".format(e))
        finally:
            return total_info


    def get_html_table(self):
        '''
        获取html中的table区域
        :return:
        '''
        table_info = ''
        try:
            info = read_file(out_html_path)
            soup = BeautifulSoup(info,  # HTML文档字符串
                                 'html.parser',  # HTML解析器
                                 from_encoding='utf-8'  # HTML文档编码
                                 )
            table_info =  soup.prettify().replace("<html>","").replace("</html>","").\
                replace('<tr hidden="true">','<tr>').replace('...','') # 修改html中的属性
        except Exception as e:
            logger.error("获取html中的table区域异常!{}".format(e))
        finally:
            return self.replace_text(table_info)


    def replace_text(self,table_info):
        '''
        英文替换成中文
        :return:
        '''
        try:
            table_info = str(table_info).replace(taskDescription,zn_taskDescription).replace(taskDescription1,zn_taskDescription1). \
                replace(taskDescription10, zn_taskDescription10).\
                replace(taskDescription2,zn_taskDescription2).replace(taskDescription3,zn_taskDescription3).\
                replace(taskDescription4,zn_taskDescription4).replace(taskDescription5,zn_taskDescription5).\
                replace(taskDescription6, zn_taskDescription6).replace(taskDescription7, zn_taskDescription7). \
                replace(taskDescription8, zn_taskDescription8).replace(taskDescription9, zn_taskDescription9)
        except Exception as e:
            logger.error("获取英文替换成中文异常!{}".format(e))
        finally:
            return table_info

