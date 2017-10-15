#!/usr/bin/env python
#coding:gbk

import Pyro4

from proxySendMail import *
from overAll import *

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

class sendMailClent(proxySendMail):
    __mailServ = {
        'proxyIp': cInfo.getV('proxy','ip'),
        'proxyPort': int(cInfo.getV('proxy','port')),
        'mailName': cInfo.getV('mail','mailName'),
        'mailAddr': cInfo.getV('mail','mailAddr'),
        'mailPwd': cInfo.getV('mail','mailPwd'),
        'smtp': cInfo.getV('mail','smtp'),
        'smtpPort': int(cInfo.getV('mail','smtpPort'))
    }

    __mailSign = '''
        <br><br><br><br>
        <font color="blue" size="2px" style="font-style:italic;">
        本邮件内容由华为ACT本地应用程序发送，请勿直接回复该邮件，并请注意核实邮件内容。<br>
        您收到这封邮件，是由于您的邮件地址设定为发送对象或者抄送对象，如不希望收到该邮件，请联系相关人员取消发送。<br>
        </font>
        <font color="gray" size="2px" style="font-style:italic;">
        <br>邮件有程序自动发送<br>
        </font>
        </br>
    '''

    def __init__(self):
        proxySendMail.__init__(self,self.__mailServ)

    def setMail(self,mailMsg):
        mailMsg['From'] = formataddr([self.__mailServ['mailName'], self.__mailServ['mailAddr']])
        toMail = mailMsg['To'].split(',')
        toMail.extend(mailMsg['Cc'].split(','))
        proxySendMail.setMailMsg(self,mailMsg)
        proxySendMail.setTomail(self,toMail)
        proxySendMail.appendMsg(self,self.__mailSign)


@Pyro4.expose
class serviceRMI(object):
    pass

if __name__ == '__main__':
    sm = sendMailClent()
    mailMsg = MIMEMultipart()
    mailMsg['Subject'] = '工资明细'
    mailMsg['To'] = 'rozen163@163.com'
    mailMsg['Cc'] = 'rozen117@163.com'
    msgCont = 'hello'
    mailMsg.attach(MIMEText(msgCont, 'html', 'gb2312'))
    sm.setMail(mailMsg)
    sm.sendMail()
