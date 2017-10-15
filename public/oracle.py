#!/usr/bin/env python
# coding:utf-8

import os
import cx_Oracle

# 设置oracle编码环境变更，防止中文乱码
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

class oracle(object):
    '''
	oracle操作封装
	'''

    def __init__(self, linkStr):
        self.link = linkStr
        self.__conn = cx_Oracle.connect(self.link)
        self.__cursor = self.__conn.cursor()
        #print '创建连接：' + str(self.__cursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.rollback()
            self.close()
            raise Exception(exc_val)
        else:
            self.close()

    def execute(self, sql, args={}):
        try:
            return self.__cursor.execute(sql, args)
        except Exception, e:
            raise Exception("执行sql语句报错：" + str(e))

    def executemany(self, sql, args={}):
        try:
            return self.__cursor.executemany(sql, args)
        except Exception, e:
            raise Exception("执行sql语句报错：" + str(e))

    def getColumns(self, table):
        '''
		:param table: 数据库表名
		:return: 列名
		'''
        try:
            sql = 'select * from ' + table + ' where rownum < 2'
            self.execute(sql)
            columns = [i[0] for i in self.__cursor.description]
            return columns
        except Exception, e:
            raise Exception("获取表列名报错：" + str(e))

    def getCursorVarString(self):
        '''
        :return: 定义oracle变量VARCHAR2, NVARCHAR2, LONG
        '''
        return self.__cursor.var(cx_Oracle.STRING)

    def getCursorVarNumber(self):
        '''
        :return: 定义oracle变量NUMBER FLOAT
        '''
        return self.__cursor.var(cx_Oracle.NUMBER)

    def getCursorVarDatetime(self):
        '''
        :return: 定义oracle变量DATE
        '''
        return self.__cursor.var(cx_Oracle.DATETIME)

    def getCursorVarChar(self):
        '''
        :return: 定义oracle变量char
        '''
        return self.__cursor.var(cx_Oracle.FIXED_CHAR)

    def callProc(self,procName,procParam = []):
        try:
            self.__cursor.callproc(procName,procParam)
        except Exception,e:
            raise Exception("调用存储过程" + procName + "报错：" + str(e))

    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

    def close(self):
        if self.__cursor:
            #print '关闭连接：' + str(self.__cursor)
            self.__cursor.close()
        if self.__conn:
            self.__conn.close()

class oraclePool(object):
    '''
	orcal数据库连接池相关操作
	'''

    _pool = None

    def __init__(self, dbInfo={}):
        self.dbInfo = dbInfo
        self.__conn = oraclePool._getConn(dbInfo)
        self.__cursor = self.__conn.cursor()

    @staticmethod
    def _getConn(dbInfo):
        if oraclePool._pool is None:
            oraclePool._pool = cx_Oracle.SessionPool(
                user=dbInfo['user'],
                password=dbInfo['pwd'],
                dsn="%s:%s/%s" % (dbInfo['host'], dbInfo['port'], dbInfo['sid']),
                min=3,
                max=8,
                increment=1)
        return oraclePool._pool.acquire()

    def getCursor(self):
        return self.__cursor

    def getCursorVarString(self):
        '''
		:return: 定义oracle变量VARCHAR2, NVARCHAR2, LONG
		'''
        return self.getCursor().var(cx_Oracle.STRING)

    def getCursorVarNumber(self):
        '''
		:return: 定义oracle变量NUMBER FLOAT
		'''
        return self.getCursor().var(cx_Oracle.NUMBER)

    def getCursorVarDatetime(self):
        '''
		:return: 定义oracle变量DATE
		'''
        return self.getCursor().var(cx_Oracle.DATETIME)

    def getCursorVarChar(self):
        '''
		:return: 定义oracle变量char
		'''
        return self.getCursor().var(cx_Oracle.FIXED_CHAR)

    def execute(self, sql, args={}):
        '''
		:param sql: 执行语句
		:param args: 绑定变量
		:return: 执行结果
		'''
        try:
            return self.__cursor.execute(sql, args)
        except Exception, e:
            raise Exception("执行sql报错：" + str(e))

    def executemany(self, sql, args={}):
        '''
		:param sql: 执行语句
		:param args: 绑定变量
		:return: 执行结果
		'''
        try:
            return self.__cursor.executemany(sql, args)
        except Exception, e:
            raise Exception("批量执行报错：" + str(e))

    def getColumns(self, table):
        '''
		:param table: 数据库表
		:return: 所有列名
		'''
        try:
            sql = 'select * from ' + table + ' where rownum < 2'
            self.execute(sql)
            columns = [i[0] for i in self.__cursor.description]
            return columns
        except Exception, e:
            raise Exception("查询表列名报错：" + str(e))

    def callProc(self,procName,procParam = []):
        try:
            self.__cursor.callproc(procName,procParam)
        except Exception,e:
            raise Exception("调用存储过程" + procName + "报错：" + str(e))

    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

    def close(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__conn:
            self.__conn.close()

if __name__ == "__main__":
    #	op = oracle(cInfo.getV('dblinks','workkafkaact5'))
    #	result = op.execute('select * from ucr_act5.tf_f_user where serial_number = :v1',{'v1':'18538008103'})
    #	rs = result.fetchone()
    #	print rs
    #	colunms = op.getColumns('ucr_act5.tf_f_user')
    #	result1 = op.execute('update zrz_tmp_1 set left_money = :v1 where action_event_id = :v2',{'v1':'2','v2':'7617011198197419'})
    #	op.commit()
    #	op.close()
    #	logging.debug(rs);
    #	logging.debug(colunms);

    dbInfo = {
        'dbtype': 'oracle',
        'user': 'rozen',
        'pwd': '123456',
        'host': '192.168.188.188',
        'port': '1521',
        'sid': 'orcl'
    }

    #op = oraclePool(dbInfo)
    #result = op.execute('select * from ucr_act3.tf_f_user where serial_number = :v1', {'v1': '18538008103'})
    #rs = result.fetchone()
    #print rs
    #resultCode = op.getCursorVarNumber()
    #resultInfo = op.getCursorVarString()
    #procParam = [3,resultCode,resultInfo]
    #op.callProc('proc_zrz_tmp',procParam)
    #op.close()
    #print procParam
    #print resultInfo.getvalue()