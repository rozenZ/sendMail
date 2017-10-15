#!/usr/bin/env python
# coding:utf-8

import logging
import ConfigParser
import sys
from threading import Thread
import Queue
import multiprocessing
import types
import copy_reg
import proConf

# 设置日志
# 输出到日志文件
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=proConf.LOGPATH + 'run.log',
                    filemode='a')

# 输出到屏幕
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# 设置字符编码
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class cInfo(object):
    """
	读取配置文件
	"""
    __conFile = proConf.CONFPATH + 'config.ini'
    __cf = ConfigParser.ConfigParser()
    __cf.read(__conFile)

    @staticmethod
    def getV(classify=None, variable=None):
        if not classify or not variable:
            raise Exception("取配置变量名称不能为空！")

        return cInfo.__cf.get(classify, variable)


class parallelWork(Thread):
    '''
	多线程并发执行函数_func，函数参数_args为字典
	'''
    workQueue = Queue.Queue(20)

    def __init__(self, func, args={}):
        Thread.__init__(self)
        self.__func = func
        self.__args = args

    def run(self):
        returnInfo = self.__func(self.__args)
        parallelWork.queueAppend(returnInfo)

    @staticmethod
    def queueAppend(args):
        #print '放入队列：' + str(args)
        parallelWork.workQueue.put(args)

'''
multiprocessing.Pool传递一个普通方法(不在class中定义的)时, 能正常工作.
但在class中定义的方法使用multiprocessing.Pool会报pickling error错误.
pool方法都使用了queue.Queue将task传递给工作进程。multiprocessing必须将数据序列化以在进程间传递。
方法只有在模块的顶层时才能被序列化，跟类绑定的方法不能被序列化，就会出现multiprocessing.Pool报pickling error异常。
使用copy_reg来规避上面的异常.
python2都存在这种问题，python3已解决
不明白啥意思，先用着
'''


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


copy_reg.pickle(types.MethodType, _pickle_method)


class processWork(object):
    '''
	多进程并发执行函数_func，并发数runNum，并发函数入参args，args列表的元素个数表示函数执行的通道数
	'''

    def __init__(self, func, runNum, args=[]):
        self.__func = func
        self.__rnNum = runNum
        self.__args = args

    def run(self):
        pool = multiprocessing.Pool(processes=self.__rnNum)
        pool.map(self.__func, self.__args)
        pool.close()
        pool.join()


# if __name__ == '__main__':
