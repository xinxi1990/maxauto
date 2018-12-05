#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,time,sys,smtplib,re
sys.path.append('..')
from loggers import JFMlogging
logger = JFMlogging().getloger()
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
from mailconfig import *
from getdata import GetData
from config import *
reload(sys)
sys.setdefaultencoding('utf8')


class SendMail():

    def __init__(self,receive_list,report_path):
        self.receive_list = receive_list
        self.report_path = report_path
        self.gd = GetData('')

    def _joincontent(self):
        '''
        拼接邮件中content内容
        :return:
        '''
        try:
            if int(self.gd.get_crashcount()) != 0:
                crashtxt = '本次运行发现{}处崩溃,详见附件log'.format(self.gd.get_crashcount())
            else:
                crashtxt = '本次运行未发现崩溃'
            send_time = time.strftime("%Y-%m-%d %H:%M:%S")
            content = ' {} \n {} \n {} \n {}'.format(send_time,'具体Android自动化专项测试报告详见附件','如附件.html格式丢失,请手动改成.html格式!',crashtxt)
            return content
        except Exception as e:
            logger.error('拼接邮件中content失败:{}'.format(e))
            return ''

    def _format_receivers(self,receivers, message):
        '''
        格式化收件人地址
        :return:
        '''
        newlist = []
        if re.findall(',', receivers):
            receivers = str(receivers).split(',')
            for index in receivers:
                newlist.append(index)
            print newlist
            message['To'] = ','.join(newlist)
            return newlist
        elif isinstance(receivers, str):
            message['To'] = receivers
            return receivers


    def _format_addr(self,s):
        '''
        格式化姓名和地址
        :param s:
        :return:
        '''
        name, addr = parseaddr(s)
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))


    def send_mail(self):

        content = self._joincontent()
        # 邮件正文

        if content != '':
            message = MIMEMultipart()
            receivers = self._format_receivers(self.receive_list, message)
            message['From'] = self._format_addr(u'发件人<%s>' % mail_user)
            subject = 'Android自动化专项测试报告'
            message['Subject'] = Header(subject, 'utf-8')
            # 邮件正文内容
            message.attach(MIMEText(content, 'plain', 'utf-8'))
            # 构造附件1，传送当前目录下的附件文件
            att1 = MIMEText(open(self.report_path).read())
            att1["Content-Type"] = 'application/octet-stream'
            # filename是附件中的名字
            att1["Content-Disposition"] = 'attachment; filename="{}"'\
                .format("Android自动化专项测试报告.html".encode('gb2312'))
            message.attach(att1)

            if int(self.gd.get_crashcount()) != 0:
                # 构造附件3，传送当前目录下的附件文件
                att3 = MIMEText(open(crash_path).read())
                att3["Content-Type"] = 'application/octet-stream'
                # filename是附件中的名字
                att3["Content-Disposition"] = 'attachment; filename="{}"'.format(
                    "Android崩溃log日志.json".encode('gb2312'))
                message.attach(att3)
            try:
                s = smtplib.SMTP()
                s.connect(mail_host)
                s.login(mail_user, mail_pass)
                s.sendmail(mail_user, receivers, message.as_string())
                s.quit()
                logger.info("邮件发送成功!")

            except Exception, e:
                s.quit()
                logger.info("邮件发送失败!"+ '\n' + '异常信息:{}'.format(e))
        else:
            logger.info('发送内容为空!')




