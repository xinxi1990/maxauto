# 简介

使用前请阅读https://testerhome.com/topics/16909<br>

使用开源工具Maxim进行Monkey测试,包含如下功能:<br>
1.安装测试<br>
2.启动测试<br>
3.登录测试<br>
4.Monkey测试<br>
5.性能数据统计<br>
6.崩溃日志及崩溃回溯图片<br>
7.apk包检查功能




# 环境依赖
1.adb环境<br>
brew install adb<br>
2.appium环境<br>
npm install appium<br>
3.python库<br>
在根目录,执行python install.py,会安装依赖项目的库


# 配置文件

参考在config文件下的config_temp.yaml文件格式

## commonconfig
```
apk_path:本地apk路径
device_name:设备号,使用adb devices查看
run_time:运行时间,单位分钟
```
## mailconfig
```
maillist: 报告邮件人,多人用逗号分隔
mailhost: 邮箱host
mailuser: 发件人邮箱地址
mailpass:  邮箱密码
mailpostfix: 邮箱后缀
```

## logincase

可配置登录测试用例或者其他前置脚本,支持click、sendkeys多种操作

eg：

```
logincase:
  - action: "click"
    location: "By.ID,xxxxx"
    time: 2
  - action: "click"
    location: "By.ID,xxxxx"
    time: 2
  - action: "send_keys"
    location: "By.ID,xxxx"
    text: "123321"
    time: 2
```


# 本地调试
```
python main.py max --config_path /Users/xinxi/PycharmProjects/maxauto/config/config.yaml
```


# 打包
```angularjs
建立setup.py

python setup.py bdist_egg

easy_install maxauto-1.0.0-py2.7.egg
```

# 发布
## 发布工具安装
```
pip install twine
```

## 发布文件配置

创建~.pypirc文件
```angularjs
[distutils]
index-servers = pypi

[pypi]
username:你的PyPi用户名
password:你的PyPi密码
```

## 发布到pypi
```
twine upload dist/*
```
# pip安装

```
pip install maxauto
```

# 运行
```angularjs

sudo chmod -R 777 /usr/local/lib/python2.7/site-packages/maxauto-1.0.0-py2.7.egg (赋予读写权限)

max --config_path /Users/xinxi/PycharmProjects/maxauto/config/config.yaml
```


# 报告
在report/reports目录下生成,效果展示如下


![report1.png](./report1.jpg)

![report2.png](./report2.jpg)

![report3.png](./report3.jpg)


# 其他

## app包检查使用命令如下:
```angularjs
cd checker
python run.py apk_path mail_list(多个人逗号分隔)
```