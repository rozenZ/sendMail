#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import xlwt
from xlutils.copy import copy
import os

import proConf

class excel(object):
	'''
	excel文档操作封装
	'''
	__excelPath = proConf.EXECLPATH
	
	def __init__(self,excelName):
		self._excelName = excelName
		self._file = self.__excelPath + self._excelName
		
		#单元格式
		self._style = xlwt.XFStyle()
		
		#字体
		fnt = xlwt.Font()
		fnt.name = u'微软雅黑'
		fnt.colour_index = 0x00     #字体颜色
		fnt.bold = False						#是否加粗
		
		#边框
		borders = xlwt.Borders()
		borders.left = 0x01
		borders.right = 0x01
		borders.top = 0x01
		borders.bottom = 0x01
		
		#默认格式
		self._style.font = fnt
		self._style.borders = borders
				
	def readExcel(self,sheetIndex = 0):
		'''
		读取excel数据内容，以列表的形式返回数据，默认只读取第一个sheet页
		'''
		try:
			wb = xlrd.open_workbook(self._file)
			sheet = wb.sheet_by_index(sheetIndex)
			nrows = sheet.nrows
			dataList = []
			for rowNum in range(0,nrows):
				rowData = sheet.row_values(rowNum)
				if rowData:
					dataList.append(rowData)
			return dataList
		except Exception,e:
			raise Exception('读取excel报错：' + str(e))

	def readExcelByFormat(self,startRow,startCol,sheetIndex):
		'''
		读取excel数据内容，以列表的形式返回数据
		从指定的sheet，指定的行列开始读取
		'''
		try:
			pass
		except Exception,e:
			raise Exception('读取excel报错：' + str(e))

	def writeExcel(self,dataList = []):
		'''
		新建excel，将列表数据写入excel，如果文件存在则会将文件覆盖
		格式为默认格式
		'''
		try:
			wb = xlwt.Workbook()
			ws = wb.add_sheet('sheet1',cell_overwrite_ok=True)

			for rowNum in range(0,len(dataList)):
				for colNum,rsColumn in enumerate(dataList[rowNum]):
					ws.write(rowNum,colNum,str(rsColumn).decode('gbk'),self._style)

			wb.save(self._file)
		except Exception,e:
			raise Exception('写excel报错：' + str(e))
		
	def overWriteByFormat(self,newExcel,startRow,startCol,sheetIndex,dataList = [],sheetName = None):
		'''
		打开指定的excel文档，向指定的sheet页，从指定的行列开始写入指定的数据
		如果excel文档不存在，则使用模板文档_file生成一个新的excel进行编辑
		如果sheetName不为空，把sheet页名字修改成改名称
		'''
		if not os.path.exists(self.__excelPath + newExcel):
			if not os.path.exists(self._file):
				raise Exception("excel模板文件不存在")
			else:
				openExcel = self._file
		else:
			openExcel = self.__excelPath + newExcel
		
		try:
			rb = xlrd.open_workbook(openExcel,formatting_info=True)
			wb = copy(rb)
			
			#根据sheet页名字查找索引
			#sheetNames = rb.sheet_names()
			#sheetIndex = sheetNames.index(sheetName)
			
			#ws = wb.add_sheet(sheetName)
			ws = wb.get_sheet(sheetIndex)
			if sheetName is not None:
				ws.set_name(str(sheetName).decode('gbk'))
			
			for rowNum in range(0,len(dataList)):
				for colNum,rsColumn in enumerate(dataList[rowNum]):
					if rsColumn == None:
						rsColumn = ''
					#ws.write(rowNum + startRow,colNum + startCol,str(rsColumn).decode('gbk'))
					self.setOutCell(ws, rowNum + startRow, colNum + startCol, str(rsColumn).decode('gbk'))
					#写
					#if isinstance(rsColumn,int) or isinstance(rsColumn,float):
					#	self.setOutCell(ws, rowNum + startRow, colNum + startCol, rsColumn)
					#else:
					#	#如果字符串全是数字且第一数字不为0，则按数字进行填充excel
					#	if str(rsColumn).isdigit() and str(rsColumn)[0] != '0':
					#		self.setOutCell(ws, rowNum + startRow, colNum + startCol, long(rsColumn))
					#	else:
					#		self.setOutCell(ws, rowNum + startRow, colNum + startCol, str(rsColumn).decode('gbk'))

			wb.save(self.__excelPath + newExcel)
		except Exception,e:
			raise Exception('写excel报错：' + str(e))

	def setOutCell(self,outSheet, row, col, value):
		""" Change cell value without changing formatting. """

		def _getOutCell(outSheet, colIndex, rowIndex):
			""" HACK: Extract the internal xlwt cell representation. """
			row = outSheet._Worksheet__rows.get(rowIndex)
			if not row: return None

			cell = row._Row__cells.get(colIndex)
			return cell

		# HACK to retain cell style.
		previousCell = _getOutCell(outSheet, col, row)
		# END HACK, PART I

		outSheet.write(row, col, value)

		# HACK, PART II
		if previousCell:
			newCell = _getOutCell(outSheet, col, row)
			if newCell:
				newCell.xf_idx = previousCell.xf_idx
			# END HACK

	def getPath(self):
		return self.__excelPath
	  
if __name__ == '__main__':
	ex = excel('hello.xls')
	dataList = [[None]]
	ex.overWriteByFormat('hello1.xls',1,0,0,dataList)
	#ex.writeExcel(dataList)
	#ex.overWrite('hello2.xls',dataList)
	#logging.info(ex.getCont())