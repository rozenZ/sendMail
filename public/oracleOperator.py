#/usr/bin/env python
#coding:utf-8

import xml.dom.minidom

import oracle
import proConf

class operators(object):
    '''
    从配置文件取相应sql语句进行执行
    '''

    def __init__(self,confFileName):
        self.__confFile = proConf.CONFPATH + confFileName

    def execXmlSql(self,dblink,tableXml,sqlXml,paramInfo):
        '''
        执行xml配置的sql语句
        '''
        sqlNode = self.getXmlSql(tableXml,sqlXml)
        sqlType = sqlNode.getAttribute('type')
        sql = sqlNode.firstChild.data
        with oracle.oracle(dblink) as oraConn:
            resultInfo = oraConn.execute(sql,paramInfo)
            if sqlType != 'select':
                oraConn.commit()
            else:
                return resultInfo.fetchall() if resultInfo is not None else []

    def getXmlSql(self,tableXml,sqlXml):
        '''
        读取xml配置
        '''
        dom = xml.dom.minidom.parse(self.__confFile)
        allRootNode = dom.documentElement
        tableNode = allRootNode.getElementsByTagName(tableXml)[0]
        sqlNode = tableNode.getElementsByTagName(sqlXml)[0]
        return sqlNode

    def callProc(self,dblink,procName,procInParam,procOutParam):
        '''
        执行存储过程
        '''
        with oracle.oracle(dblink) as oraConn:
            if len(procOutParam) != 0:
                for index, outParam in enumerate(procOutParam):
                    if outParam == 'number':
                        procOutParam[index] = oraConn.getCursorVarNumber()
                    elif outParam == 'varchar2':
                        procOutParam[index] = oraConn.getCursorVarString()
                    elif outParam == 'char':
                        procOutParam[index] = oraConn.getCursorVarChar()
                    elif outParam == 'date':
                        procOutParam[index] = oraConn.getCursorVarDatetime()
                    else:
                        raise Exception('未定义存储过程返回值类型！')
            print procOutParam
            oraConn.callProc(procName,procInParam + procOutParam)

    def execExistsSql(self, dblink, sql, paramInfo, sqlType):
        '''
        执行传入的sql
        '''
        with oracle.oracle(dblink) as oraConn:
            resultInfo = oraConn.execute(sql, paramInfo)
            if sqlType != 'select':
                oraConn.commit()
            else:
                return resultInfo.fetchall()

    def getTableColumn(self,dblink,tableName):
        '''
        读取表列名
        '''
        with oracle.oracle(dblink) as oraConn:
            columnList = oraConn.getColumns(tableName)

        return columnList if columnList is not None else []

if __name__ == '__main__':
    op = operators('autoMail.xml')
    #print op.getXmlSql('autoRoute','selectByTaskId')
    resultInfos = op.execXmlSql('rozen/123456@orcl','autoTask','selectAuto',{})
    for resultInfo in resultInfos:
        print resultInfo
    #procOutParam = ['number','varchar2']
    #op.callProc(None,None,None,procOutParam)
