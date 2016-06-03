import xlrd
import xlwt
from lxml import html
from bs4 import BeautifulSoup
from urllib2 import urlopen

wb = xlrd.open_workbook('data1.xls')
data = wb.sheet_by_index(0)
book = xlwt.Workbook()
sheet1 = book.add_sheet("IP List")
countrow = 2
for rownum in range(data.nrows): 
	if rownum > 1: 
		IPdest = data.cell(rownum,5).value
		if not IPdest.startswith("10") and not IPdest.startswith("172") and not IPdest.startswith("192"):
			sheet1.write(countrow-2,0,IPdest)
			countrow+=1
book.save('iplist.xls')
