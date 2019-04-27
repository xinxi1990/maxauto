#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 邮件服务
"""

import os,time,sys,smtplib,re
sys.path.append('..')
from ..tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
reload(sys)
sys.setdefaultencoding('utf8')


class SendMail():

    def __init__(self,mail_info,report_path):
        self.mail_info = mail_info
        self.mail_list = mail_info['maillist']
        self.mail_host = mail_info['mailhost']
        self.mail_user = mail_info['mailuser']
        self.mail_pass = mail_info['mailpass']
        self.report_path = report_path

    def _joincontent(self):
        '''
        拼接邮件中content内容
        :return:
        '''
        content = ''
        try:
            send_time = time.strftime("%Y-%m-%d %H:%M:%S")
            content = '{},{}'.format(send_time,'具体Android稳定性测试报告详见附件!')
        except Exception as e:
            logger.error('邮件内容拼接失败:{}!'.format(e))
        finally:
            return content


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
        message = MIMEMultipart()
        receivers = self._format_receivers(self.mail_list, message)
        message['From'] = self._format_addr(u'发件人<%s>' %  self.mail_user)
        subject = 'Android稳定性测试报告'
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        att1 = MIMEText(open(self.report_path).read())
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="{}"'\
            .format("Android稳定性测试报告.html".encode('gb2312'))
        message.attach(att1)
        try:
            s = smtplib.SMTP()
            s.connect(self.mail_host)
            s.login(self.mail_user, self.mail_pass)
            s.sendmail(self.mail_user, receivers, message.as_string())
            s.quit()
            logger.info("邮件发送成功!")
        except Exception, e:
            s.quit()
            logger.info("邮件发送失败!"+ '\n' + '异常信息:{}'.format(e))





