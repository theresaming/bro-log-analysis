import xlwt, xlrd, sys, datetime, time, unicodedata

#automated data analysis on conn logs

#open the connlogs excel and write to a new sheet
#find the sheet number (logs are every other starting at 0)
wb = xlrd.open_workbook('logs.xls')
log = wb.sheet_by_index(1)
