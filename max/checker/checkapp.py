#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 检查app资源大小
"""

import os, re, time, sys, subprocess,json
from filetools import *
from config import *


class CheckApp():

    def __init__(self,apk_path):
        self.apk_path = apk_path
        self.result_path = out_name

    def write_config(self):
        '''
        修改配置文件
        :return:
        '''

        if os.path.exists(out_path):
            shutil.rmtree(out_path)
        os.mkdir(out_path)
        config_str = read_file(config_path)
        config_json = json.loads(config_str)
        config_json['--apk'] = self.apk_path
        config_json['--output'] = self.result_path
        config_json.update()
        del_files(config_path)
        write_file(config_path,json.dumps(config_json,indent=4))

    def check_app(self):
        '''
        执行脚本
        :return:
        '''
        try:
            self.write_config()
            cmd = "java -jar {} --config {}".format(matrix_path,config_path)
            subprocess.call(cmd,shell=True)
            logger.info("检查app完成!")
        except Exception as e:
            logger.error("检查app异常!{}".format(e))


    def upload_result(self):
        '''
        上传结果到服务器
        :return:
        '''

if __name__ == '__main__':
    apk = "/Users/xinxi/Desktop/checker/app_debug_5.5.0_20181225160438.apk"
    CheckApp(apk).check_app()





