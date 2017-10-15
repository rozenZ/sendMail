#!/usr/bin/env python
# encoding: gbk
 
import smtplib 
#import socket
#import socks
import os

from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr


class proxySendMail(object):

	def __init__(self,mailServ = {}):
		self.__mailMsg = None
		self.__toMail = None

		self.__proxyIp = mailServ['proxyIp']
		self.__proxyPort = mailServ['proxyPort']
		self.__mailName = mailServ['mailName']
		self.__mailFrom = mailServ['mailAddr']
		self.__mailPwd = mailServ['mailPwd']
		self.__smtp = mailServ['smtp']
		self.__smtpPort = mailServ['smtpPort']

		#set proxy
		#socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, self.__proxyIp, self.__proxyPort)
		#socket.socket = socks.socksocket

		#set mail
		'''
		self.__mailMsg = MIMEMultipart()
		self.__mailMsg['From'] = formataddr([self.__mailName, self.__mailFrom])

		if subject:			 
			#if not isinstance(subject,unicode):  
			#    subject = unicode(subject, 'utf-8')      
			self.__mailMsg['Subject'] = subject
		else:
			raise Exception("邮件主题为空")
		
		if toMail:
			self.__toMail = toMail
			self.__mailMsg['To'] = ','.join(toMail)
		else:
			raise Exception("邮件发送列表为空")
		
		if ccMail:
			self.__toMail.extend(ccMail)
			self.__mailMsg['Cc'] = ','.join(ccMail)
  	
		if msgCont: 
			self.__mailMsg.attach(MIMEText(msgCont, 'html', 'gb2312'))
		'''

	def setMail(self,subject = None,toMail = None,ccMail = None,msgCont = None):
		self.__mailMsg = MIMEMultipart()
		self.__mailMsg['From'] = formataddr([self.__mailName, self.__mailFrom])

		if subject:
			# if not isinstance(subject,unicode):
			#    subject = unicode(subject, 'utf-8')
			self.__mailMsg['Subject'] = subject
		else:
			raise Exception("邮件主题为空")

		if toMail:
			self.__toMail = toMail
			self.__mailMsg['To'] = ','.join(toMail)
		else:
			raise Exception("邮件发送列表为空")

		if ccMail:
			self.__toMail.extend(ccMail)
			self.__mailMsg['Cc'] = ','.join(ccMail)

		if msgCont:
			self.__mailMsg.attach(MIMEText(msgCont, 'html', 'gb2312'))

	def setMailMsg(self,mailMsg):
		self.__mailMsg = mailMsg

	def setTomail(self,toMail):
		self.__toMail = toMail

	def appendMsg(self,msgCont):
		'''
		追加邮件正文内容
		:param msgCont:
		:return:
		'''
		self.__mailMsg.attach((MIMEText(msgCont, 'html', 'gb2312')))

	def addFile(self,mailFile = None,fileName = None):
		"""
		添加附件
		"""
		try:
			if not fileName:
				fileName = os.path.basename(mailFile)

			attFile = MIMEText(open(mailFile,'rb').read(), 'base64', 'gb2312')
			attFile["Content-Type"] = 'application/octet-stream'
			attFile["Content-Disposition"] = 'attachment; filename="%s"' % fileName
			
			self.__mailMsg.attach(attFile)
		except Exception,e:
			raise Exception('添加附件失败:'+str(e))

	def sendMail(self):
		"""
		发送邮件
		"""
		try:
			#QQ邮箱SSL验证
			#smtpObj = smtplib.SMTP()
			smtpObj = smtplib.SMTP_SSL()
			smtpObj.connect(self.__smtp, self.__smtpPort)
			state = smtpObj.login(self.__mailFrom, self.__mailPwd)
			if state[0] == 235:
				smtpObj.sendmail(str(self.__mailMsg['From']), self.__toMail, self.__mailMsg.as_string())
				#logging.info("\"" + self._mailMsg['subject'] + "\"邮件发送成功，" +
				#	"To:" + self._mailMsg['To'] + "，Cc:" + self._mailMsg['Cc'])
			smtpObj.quit()
		except smtplib.SMTPException, e:
			raise Exception('邮件发送失败:'+str(e))

if __name__ == '__main__':
	mailInfo = {
		'proxyIp':'122.193.14.114',
		'proxyPort':81,
		'mailName':'rozen',
		'mailAddr':'76998354@qq.com',
		#'mailPwd':'fhqrdfe681718465',
		'mailPwd': 'wpeagygtlnsfcabb',
		'smtp':'smtp.qq.com',
		'smtpPort':465
	}

	subject = '工资明细'
	toMail = ["rozen117@163.com"]
	ccMail = ["rozen163@163.com"]
	msg = '工资明细，请查收'
	try:
		testMail = proxySendMail(mailInfo)
		testMail.setMail(subject,toMail,ccMail,msg)
		testMail.sendMail()
	except Exception,e:
		print '邮件发送失败:'+str(e)