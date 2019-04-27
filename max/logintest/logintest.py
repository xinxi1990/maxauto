#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,os,sys,subprocess,json
from ..tools.filetools import write_file
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from location import Location
from ..tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from ..config import logintest_app_log,appium_log


class AppiumDriver(object):
    driver = None
    def  __init__(self ,device_name,pck_name,lanuch_activity):
        self.device_name = device_name
        self.url = "127.0.0.1"
        self.port = "4725"
        self.pck_name = pck_name
        self.lanuch_activity = lanuch_activity
        self.appium_log = appium_log

    def init_capability(self):
        '''
        启动配置文件
        :return:
        '''
        desired_caps = {
            "platformName": "Android",
            "appPackage": self.pck_name,
            "platformVersion ": "7.0",
            "appActivity": self.lanuch_activity,
            "autoLaunch": "true",
            "unicodeKeyboard": "true", # 使用appium的输入法，支持中文并隐藏键盘
            "resetKeyboard": "true", # 重置键盘
            #"newCommandTimeout": 120, # 设置driver超时时间
            "automationName": "uiautomator2"
        }
        desired_caps["deviceName"] = self.device_name
        desired_caps.update()
        AppiumDriver.driver = webdriver.Remote('http://{}:{}/wd/hub'.format(self.url ,self.port), desired_caps)
        return AppiumDriver.driver


    def kill_appium(self):
        '''
        结束appium进程
        :return:
        '''
        if os.popen('lsof -i:{}'.format(self.port)).read() == '':
            logger.info('appium进程不存在')
        else:
            pid = os.popen('lsof -i:{}'.format(self.port)).readlines()[1].split()[1]
            subprocess.call('kill -9 {}'.format(pid),shell=True)
            logger.info('停止appium进程:{}'.format(pid))


    def start_appium(self):
        '''
        启动appium服务
        :return:
        '''
        self.kill_appium()
        args = 'appium --log {} --session-override --udid {} -a {} -p {}'.\
            format(self.appium_log,self.device_name ,self.url,self.port)
        logger.info('appium启动命令:{}'.format(args))
        appium = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, bufsize=1,close_fds=True)
        while True:
            appium_line = appium.stdout.readline().strip().decode()
            time.sleep(1)
            logger.info("启动appium中...")
            if 'Welcome to Appium' in appium_line or 'Error: listen' in appium_line:
                logger.info("appium启动成功")
                break
        return self.init_capability()


    def reset_keyboard(self ,device):
        '''
        重置键盘
        :return:
        '''
        try:
            cmd = "adb -s {} shell ime list -s | grep -v 'appium'".format(device)
            cmdline = subprocess.Popen(cmd ,shell=True, stdout=subprocess.PIPE)
            Keyboard = cmdline.stdout.readlines()[0].replace("\r\n" ,"")
            resetcmd = "adb -s {} shell ime set {}".format(device ,Keyboard)
            subprocess.call(resetcmd ,shell=True)
            logger.info("重置输入法完成")
        except Exception as e:
            logger.info("重置输入法异常!{}".format(e))


class LoginApp():

    def __init__(self,device_name,pck_name,lanuch_activity,login_caseinfo):
        '''
        初始化外部入参数
        '''
        self.device_name = device_name
        self.pck_name = pck_name
        self.lanuch_activity = lanuch_activity
        self.login_caseinfo = login_caseinfo


    def logcat(self,log_path,delay):
        time.sleep(delay)
        cmd = 'adb logcat > {}'.format(log_path)
        subprocess.call(cmd,shell=True)
        logger.info('启动logcat')



    def test_login(self):
        login_result = 'fail'
        try:
            self.appium_driver = AppiumDriver(self.device_name, self.pck_name, self.lanuch_activity)
            self.driver = self.appium_driver.start_appium()
            self.driver.implicitly_wait(5)
            location = Location(self.driver)
            for case_step in self.login_caseinfo:
                try:
                    if case_step['action'] == "click":
                        element = location.create_location(case_step['location'])
                        location.display_wait(case_step["time"], element).click()
                    elif case_step['action'] == "send_keys":
                        element = location.create_location(case_step['location'])
                        location.display_wait(case_step["time"], element).send_keys(case_step['text'])
                    elif case_step['action'] == "wait_sleep":
                        location.wait_sleep(case_step["time"])
                    elif case_step['action'] == "when_element_click":
                        element = location.create_location(case_step['location'])
                        location.when_element_click(case_step["time"], element)
                except Exception as e:
                    logger.error("登录异常:{}".format(e))
                    login_result = 'fail'
        except Exception as e:
            logger.info('登录测试异常:{}'.format(e))
        finally:
            self.appium_driver.kill_appium()
            write_file(logintest_app_log, login_result, is_cover=True)
