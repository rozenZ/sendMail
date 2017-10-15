#/usr/bin/env python
#coding:gbk

import datetime
import time

#mailTo = ['zhaoruzhen@mail01.huawei.com']
#print ','.join(mailTo)
#mailList = []
#mailList.extend(mailTo)
#print mailList

#nowtime = datetime.datetime.today()
#lastCycle = datetime.datetime(nowtime.year,nowtime.month,1) - datetime.timedelta(days = 1)
#print nowtime.strftime('%Y%m')
#print lastCycle.strftime('%Y%m')

#haha = 3234234
#hehe = '32342342'

#print type(haha)
#print isinstance(haha,int)
#print type(hehe)
#print isinstance(hehe,str)

#print hehe.isdigit()


#dict = {'haha':1233}
#print len(dict)
#print dict.__getitem__('haha')

import xml.dom.minidom

#dom = xml.dom.minidom.parse('conf/autoMail.xml')
#root = dom.documentElement
#print root.nodeName
#print root.nodeValue
#print root.nodeType
#print root.ELEMENT_NODE

#e = root.getElementsByTagName('autoRoute')
#f = e[0].getElementsByTagName('selectByTaskId')
#print f[0].firstChild.data

#re = root.getElementsByTagName('autoMail')
#ree = re[0].getElementsByTagName('selectByTaskId')
#print ree[0].firstChild.data

#import os
#print os.environ['LD_LIBRARY_PATH']

list1 = [1,23,4]
list2 = [32,6,7]

print list1 + list2