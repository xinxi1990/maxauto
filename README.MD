# 简介

使用开源工具Maxim进行Monkey测试,包含如下功能:<br>
1.安装测试<br>
2.启动测试<br>
3.登录测试<br>
4.Monkey测试<br>
5.性能数据统计<br>
6.崩溃日志及崩溃回溯图片<br>


# 环境依赖
1.adb环境<br>
brew install adb<br>
2.appium环境<br>
npm install appium<br>
3.python库<br>
在根目录,执行python setup.py会安装有python需要的库


# 运行
```
cd到根目录下

apk_path:本地apk路径
device_name:设备号,使用adb devices查看
run_time:运行时间,单位分钟
mail_list:报告邮件人,多人用逗号分隔

python run.py apk_path device_name run_time mail_list

```
# 报告
在report/reports目录下生成,效果展示如下


![report1.png](./report1.jpg)

![report2.png](./report2.jpg)

![report3.png](./report3.jpg)