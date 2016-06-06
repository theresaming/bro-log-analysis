import gzip
import xlwt
import datetime

#content = "jsflajskfdjfkaljsfklsdjfa"
#f = gzip.open('tester.log.gz', 'wb')
#f.write(content)
#f.close()
#everything after row 2 has to be shifted right one
#convert timestamp
book = xlwt.Workbook()
sheet1 = book.add_sheet("2016-06-02 http")
http_filename = 'http_eth1.12_00_00-13_00_00_sanit.gz'
f = gzip.open(http_filename, 'rb')
for i in range(0,10000): # only taking the first 10,000 data points
	file_content=f.readline()
	if i >= 6: #start at header row
		if i == 6 or i == 7:
			startcol = 0
		else:
			startcol = 1 
		lines = file_content.split('\x09')
		for j in range(0,len(lines)):
			if j == 0 and i > 7:
				lines[0] = datetime.datetime.fromtimestamp(float(lines[0])).strftime('%Y-%m-%d %H:%M:%S')
			sheet1.write(i-6,j+startcol,lines[j])

sheet2 = book.add_sheet("2016-06-02 conn")
conn_filename = 'conn.12_00_00-13_00_00.log.gz'
f = gzip.open(conn_filename, 'rb')
for i in range(0,10000): # only taking the first 10,000 data points
	file_content=f.readline()
	if i >= 6: #start at header row
		if i == 6 or i == 7:
			startcol = 0
		else:
			startcol = 1 
		lines = file_content.split('\x09')
		for j in range(0,len(lines)):
			if j == 0 and i > 7:
				lines[0] = datetime.datetime.fromtimestamp(float(lines[0])).strftime('%Y-%m-%d %H:%M:%S')
			sheet2.write(i-6,j+startcol,lines[j])

sheet3 = book.add_sheet("2016-06-02 ftp")
ftp_filename = 'ftp.12_00_00-13_00_00.log.gz'
f = gzip.open(ftp_filename, 'rb')
for i in range(0,10000): # only taking the first 10,000 data points
	file_content=f.readline()
	if i >= 6: #start at header row
		if i == 6 or i == 7:
			startcol = 0
		else:
			startcol = 1 
		lines = file_content.split('\x09')
		for j in range(0,len(lines)):
			if j == 0 and i > 7:
				lines[0] = datetime.datetime.fromtimestamp(float(lines[0])).strftime('%Y-%m-%d %H:%M:%S')
			sheet3.write(i-6,j+startcol,lines[j])
	
book.save('logs.xls')
