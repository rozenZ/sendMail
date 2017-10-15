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
        ���ʼ������ɻ�ΪACT����Ӧ�ó����ͣ�����ֱ�ӻظ����ʼ�������ע���ʵ�ʼ����ݡ�<br>
        ���յ�����ʼ��������������ʼ���ַ�趨Ϊ���Ͷ�����߳��Ͷ����粻ϣ���յ����ʼ�������ϵ�����Աȡ�����͡�<br>
        </font>
        <font color="gray" size="2px" style="font-style:italic;">
        <br>�ʼ��г����Զ�����<br>
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
    mailMsg['Subject'] = '������ϸ'
    mailMsg['To'] = 'rozen163@163.com'
    mailMsg['Cc'] = 'rozen117@163.com'
    msgCont = 'hello'
    mailMsg.attach(MIMEText(msgCont, 'html', 'gb2312'))
    sm.setMail(mailMsg)
    sm.sendMail()
