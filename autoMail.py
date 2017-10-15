#/usr/bin/env python
#coding:utf-8

import datetime
import time
from public import *


class autoMail(object):
    '''
    自动发送邮件
    任务需要在数据库表中进行配置work_wk@kafkaact5
    tf_l_auto_task
    tf_l_auto_mail
    tf_l_auto_mail_file
    '''

    #邮件配置相关信息
    __mailServ = {
        'proxyIp': cInfo.getV('proxy','ip'),
        'proxyPort': int(cInfo.getV('proxy','port')),
        'mailName': cInfo.getV('mail','mailName'),
        'mailAddr': cInfo.getV('mail','mailAddr'),
        'mailPwd': cInfo.getV('mail','mailPwd'),
        'smtp': cInfo.getV('mail','smtp'),
        'smtpPort': int(cInfo.getV('mail','smtpPort'))
    }
    #邮件正文表格样式
    __htmlStyle = '''
        <head>
            <style type="text/css">
                table.gridtable {
                    font-family: verdana,arial,sans-serif;
                    font-size:11px;
                    color:#333333;
                    border-width: 1px;
                    border-color: #666666;
                    border-collapse: collapse;
                }
                table.gridtable th {
                    border-width: 1px;
                    padding: 8px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: #dedede;
                }
                table.gridtable td {
                    border-width: 1px;
                    padding: 8px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: #ffffff;
                }
            </style>
        </head>
    '''

    # 邮件签名
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
        self.__oper = operators('autoMail.xml')
        self.__taskDblink = cInfo.getV('dblinks', 'rozenLocal')

    def autoRun(self):
        try:
            while(True):
                logging.info('检测是否有需要处理的邮件任务。')
                taskInfos = self.__oper.execXmlSql(self.__taskDblink,'autoTask','selectAuto',paramInfo={})

                for taskInfo in taskInfos:
                    logging.info('开始自动邮件任务')
                    taskId = int(taskInfo[0])
                    taskName = taskInfo[1]
                    interval = str(taskInfo[5])
                    logging.info( '邮件任务：' + str(taskId) + '-' + str(taskName).decode('gbk') )

                    try:
                        self.autoSendMail(taskId)

                        paramInfo = {'vinterval':interval,'vtask_id':taskId}
                        self.__oper.execXmlSql(self.__taskDblink,'autoTask','updateSuccessed',paramInfo)
                        logging.info('邮件任务：' + str(taskId) + '-' + str(taskName).decode('gbk') + '执行成功！')
                    except Exception,e:
                        paramInfo = {'vinterval':interval,'vsql_errm':str(e).decode('utf-8'),'vtask_id': taskId}
                        self.__oper.execXmlSql(self.__taskDblink, 'autoTask', 'updateFailed', paramInfo)
                        logging.info('邮件任务：' + str(taskId) + '-' + str(taskName).decode('gbk') + '执行失败，请人工核查！')
                        continue

                logging.info('等待300秒，进行下一轮检测。')
                break
                time.sleep(300)
        except Exception,e:
            raise Exception('自动邮件任务报错：' + str(e))

    def autoRunById(self,taskId):
        try:
            paramInfo = {'vtask_id': taskId}
            print paramInfo
            taskInfos = self.__oper.execXmlSql((self.__taskDblink,'autoTask','selectByTaskId',paramInfo))

            for taskInfo in taskInfos:
                logging.info('开始自动邮件任务')
                taskName = taskInfo[1]
                interval = str(taskInfo[5]) if taskInfo[5] is not None else ''
                logging.info( '邮件任务：' + str(taskId) + '-' + str(taskName).decode('gbk') )

                try:
                    self.autoSendMail(taskId)

                    paramInfo = {'vinterval':interval,'vtask_id':taskId}
                    self.__oper.execXmlSql(self.__taskDblink, 'autoTask', 'updateSuccessed', paramInfo)
                    logging.info('邮件任务：' + str(taskId) + '-' + str(taskName).decode('gbk') + '执行成功！')
                except Exception,e:
                    paramInfo = {'vinterval':interval,'vsql_errm':str(e).decode('utf-8'),'vtask_id': taskId}
                    self.__oper.execXmlSql(self.__taskDblink, 'autoTask', 'updateFailed', paramInfo)
                    logging.info('邮件任务：' + str(taskId) + '-' + str(taskName).decode('gbk') + '执行失败，请人工核查！' + str(e).decode('gbk'))
        except Exception,e:
            raise Exception('自动邮件任务报错：' + str(e))

    def autoRoute(self,taskId):
        paramInfo = {'vtask_id':taskId}
        dblink = cInfo.getV('dblinks','rozenLocal')
        results = self.__oper.execXmlSql(dblink,'autoRoute','selectByTaskId',paramInfo)

        threadWorkList = []
        for result in results:
            taskName = result[0]
            routeId = result[1]
            status = result[2]
            routeFlag = result[3]
            procName = result[4]
            inParam = result[5].split(',') if result[4] is not None else None
            outParam = result[6].split(',') if result[4] is not None else None
            dbUser = result[7]

            paramDict = {'routeId': routeId, 'procName': procName, 'inParam': inParam, 'outParam': outParam,
                         'dbUser': dbUser}

            if status == '1':
                raise Exception('任务当前运行中！')

            try:
                if routeFlag == '0':
                    print '执行并行任务' + str(taskName).decode('gbk') + ':' + str(routeId)
                    if procName is None or dbUser is None:
                        raise Exception('存储过程或数据库用户配置为空')

                    paramInfo = {'vtask_id':taskId, 'vroute_id':routeId}
                    self.__oper.execXmlSql(self.__taskDblink,'autoRoute','updateByRouteWhenStart',paramInfo)

                    threadWork = parallelWork(self.execProc, paramDict)
                    threadWork.start()
                    threadWorkList.append(threadWork)
                elif routeFlag == '1':
                    if len(threadWorkList) != 0:
                        for work in threadWorkList:
                            work.join()

                        while not parallelWork.workQueue.empty():
                            resultInfo = parallelWork.workQueue.get()
                            tmpRouteId = resultInfo['routeId']
                            paramInfo = {'vresult_info':str(resultInfo['outParam']),'vtask_id':taskId,'vroute_id':tmpRouteId}
                            self.__oper.execXmlSql(self.__taskDblink,'autoRoute','updateByrouteWhenEnd',paramInfo)

                    del threadWorkList[:]

                    print '执行顺行任务' + str(taskName).decode('gbk') + ':' + str(routeId)

                    if procName is not None and dbUser is not None:
                        paramInfo = {'vtask_id': taskId, 'vroute_id': routeId}
                        self.__oper.execXmlSql(self.__taskDblink, 'autoRoute', 'updateByRouteWhenStart', paramInfo)
                        threadWork = parallelWork(self.execProc, paramDict)
                        threadWork.start()
                        threadWork.join()

                        resultInfo = parallelWork.workQueue.get()
                        tmpRouteId = resultInfo['routeId']
                        paramInfo = {'vresult_info': str(resultInfo['outParam']), 'vtask_id': taskId,
                                     'vroute_id': tmpRouteId}
                        self.__oper.execXmlSql(self.__taskDblink, 'autoRoute', 'updateByrouteWhenEnd', paramInfo)
            except Exception,e:
                paramInfo = {'vresult_info': str(e).decode('utf-8'), 'vtask_id': taskId, 'vroute_id': routeId}
                self.__oper.execXmlSql(self.__taskDblink, 'autoRoute', 'updateByrouteWhenEnd', paramInfo)
        else:
            if len(threadWorkList) != 0:
                for work in threadWorkList:
                    work.join()

                while not parallelWork.workQueue.empty():
                    resultInfo = parallelWork.workQueue.get()
                    print resultInfo
                    tmpRouteId = resultInfo['routeId']
                    paramInfo = {'vresult_info': str(resultInfo['outParam']), 'vtask_id': taskId, 'vroute_id': tmpRouteId}
                    self.__oper.execXmlSql(self.__taskDblink, 'autoRoute', 'updateByrouteWhenEnd', paramInfo)

    def execProc(self,paramDict = {}):
        procName = paramDict['procName']
        procInParam = paramDict['inParam']
        procOutParam = paramDict['outParam']
        dbUser = paramDict['dbUser']
        dblink = cInfo.getV('dblinks',dbUser)
        self.__oper.callProc(dblink,procName,procInParam,procOutParam)
        return paramDict

    def autoSendMail(self,taskId):
        '''
        收集邮件数据，发送邮件
        :param taskId:
        :return:
        '''
        paramInfo = {'vtask_id':taskId}
        mailInfos = self.__oper.execXmlSql(self.__taskDblink,'autoMail','selectByTaskId',paramInfo)
        for mailInfo in mailInfos:
            mailSendFlag = mailInfo[4]

            # 只生成文件，不发送邮件
            if mailSendFlag is not None and mailSendFlag == '0':
                self.getMailFile(taskId)
                continue

            mailSubject = self.replaceStr(mailInfo[0])
            mailTo = mailInfo[1].split(',') if mailInfo[1] != None else None
            mailCc = mailInfo[2].split(',') if mailInfo[2] != None else None
            mailMsg = self.__htmlStyle + self.replaceStr(str(mailInfo[3]))

            sMail = proxySendMail(self.__mailServ)
            sMail.setMail(mailSubject,mailTo,mailCc,mailMsg)

            # 添加附件
            mailFileList = self.getMailFile(taskId)
            if len(mailFileList) != 0:
                for mailFile in mailFileList:
                    sMail.addFile(mailFile)

            #添加邮件正文表格
            msgCont = self.getMailContentExcel(taskId)
            if msgCont is not None:
                sMail.appendMsg(msgCont)

            #添加签名
            sMail.appendMsg(self.__mailSign.decode('utf-8'))
            sMail.sendMail()

    def getMailFile(self,taskId):
        '''
        根据sql及数据模板生成邮件附件
        :param taskId:
        :return:
        '''
        paramInfo = {'vtask_id':taskId}
        fileInfos = self.__oper.execXmlSql(self.__taskDblink,'autoMailFile','selectExcelSql1',paramInfo)
        if len(fileInfos) == 0:
            return []

        fileList = []

        for fileInfo in fileInfos:
            fileName = fileInfo[0]
            fileSql = fileInfo[1]
            fileSheet = fileInfo[2]
            startRow = fileInfo[3]
            startCol = fileInfo[4]
            fileNameTemp = fileInfo[5]
            sheetName = self.replaceStr(fileInfo[6])

            if fileSql is None:
                raise Exception('sql语句配置不能为空！')

            if fileNameTemp is None:
                raise Exception('excel模板配置不能为空！')

            if fileSheet is None or startCol is None or startRow is None:
                raise Exception('sheet索引、开始行号、开始列号配置不能为空！')

            datas = self.__oper.execExistsSql(self.__taskDblink,fileSql,paramInfo={},sqlType='select')
            if fileName is not None:
                excelName = self.replaceStr(fileName)
            else:
                currDate = time.strftime('%Y%m%d', time.localtime(time.time()))
                excelName = fileNameTemp + '-' + currDate
            ex = excel(fileNameTemp)
            ex.overWriteByFormat(excelName, startRow, startCol, fileSheet, datas, sheetName)
            fileList.append(ex.getPath() + excelName)

        return fileList

    def replaceStr(self,mailStr):
        '''
        替换主题及邮件正文中的账期字符串
        目前只替换this_cycle、last_cycle、this_day，如果需要其他的，可以再添加
        :param mailStr:
        :return:
        '''
        if mailStr is None:
            return None

        nowtime = datetime.datetime.today()
        thisDayDate = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)
        lastMonth = datetime.datetime(nowtime.year, nowtime.month, 1) - datetime.timedelta(days=1)
        thisCycle = nowtime.strftime('%Y%m')
        lastCycle = lastMonth.strftime('%Y%m')
        thisDay = thisDayDate.strftime('%Y%m%d')
        repStr = {}
        repStr['this_cycle'] = thisCycle
        repStr['last_cycle'] = lastCycle
        repStr['this_day'] = thisDay

        tmpStr = mailStr
        for key,value in repStr.items():
            tmpStr = tmpStr.replace(key,value)

        return tmpStr

    def getMailContentExcel(self,taskId):
        '''
        添加邮件正文数据表格
        :param taskId:
        :return:
        '''
        tmpStr = '<table class="gridtable">'
        paramInfo = {'vtask_id': taskId}
        resultInfo = self.__oper.execXmlSql(self.__taskDblink,'autoMailFile','selectExcelSql2',paramInfo)
        if len(resultInfo) == 0:
            return None

        excelSql = str(resultInfo[0][0])

        #取列名
        tableName = '(' + excelSql + ')'
        colNames = self.__oper.getTableColumn(self.__taskDblink,tableName)

        #取数据
        excelInfos = self.__oper.execExistsSql(self.__taskDblink,excelSql,paramInfo={},sqlType='select')

        if len(excelInfos) > 0:
            tmpStr = tmpStr + '<tr>'
            for colName in colNames:
                tmpStr = tmpStr + '<th>' + str(colName) + '</th>'
            tmpStr = tmpStr + '</tr>'
        else:
            return None

        for excelInfo in excelInfos:
            tmpStr = tmpStr + '<tr>'
            for rowValue in excelInfo:
                if rowValue == None:
                    rowValue = ''
                tmpStr = tmpStr + '<td>' + str(rowValue) + '</td>'
            tmpStr = tmpStr + '</tr>'

        tmpStr = tmpStr + '</table>'

        return tmpStr

if __name__ == '__main__':
    at = autoMail()
    #at.autoRoute(170926100004)
    #at.autoRun()
    at.autoRunById(170926100004)