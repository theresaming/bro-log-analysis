import xlwt, xlrd, sys, datetime, time, unicodedata, csv

#automated data analysis on conn logs

#open the connlogs excel and write to a new sheet
#find the sheet number (logs are every other starting at 0)
wb = xlrd.open_workbook('logs.xls')
log = wb.sheet_by_index(1)

#I/O
looper = True
while looper:
    print "CONN Analysis - Options (type a number)"
    print "(1) Find all connection durations greater than some threshold"
    print "(2) Breakdown of all connections by service"
    print "(3) Breakdown of all responding ports"
    print "(4) Breakdown of all transport layer protocols"
    print "(5) Breakdown of all origination country codes"
    print "(6) EMPTY"
    print "(7) EMPTY"
    print "(8) Data based on UID"
    print "(9) End program."

    try:
        x = input('Enter a value: ')
        if x == 9:
                sys.exit()
        if x < 1 or x > 9:
            print "Not a valid number. Choose a number between 1 and 7."
    except ValueError:
        print "Not a valid number. Choose a number between 1 and 7."

    # * * * * * * * * * * * * * 
    #(1) Find top 10 durations

    #headers needed: duration (9) and uid (2)
    if x == 1:
        arr = []
        uid = []
        threshold = input("Enter a lower limit (exclusive): ")
        for rownum in range(log.nrows):
            if rownum > 1:
                if log.cell(rownum,9).value != '-':
                    s = (float)(log.cell(rownum,9).value)
                    if s > threshold:
                        arr.append(s)
                        uid.append(log.cell(rownum,2).value)
        print "UID\t\t\tDURATION"
        for i in range(len(arr)):
            print uid[i], '\t', arr[i]
                    
    # * * * * * * * * * * * * * 
    #(2) Breakdown of all connections by service

    #headers needed: service (8)
    if x == 2:
        service = []
        instances = []
        for rownum in range(log.nrows):
            if rownum > 1:
                s = log.cell(rownum,8).value
                if s not in service:
                    service.append(s)
                    ind = service.index(s)
                    instances.append(1)
                else:
                    ind = service.index(s)
                    instances[ind] += 1
        print "INSTANCES\tSERVICE"
        for i in range(len(service)):
            print instances[i], '\t\t' + service[i]
                


    # * * * * * * * * * * * * *

    #(3) Breakdown of all responding ports

    #headers needed: id.resp_p(6)
    if x == 3:
        ports = []
        instances = []
        for rownum in range(log.nrows):
            if rownum > 1:
                s = log.cell(rownum,6).value
                if s not in ports:
                    ports.append(s) 
                    ind = ports.index(s)
                    instances.append(1)
                else:
                    ind = ports.index(s)
                    instances[ind] += 1
        print "PORTS" + '\t' + "INSTANCES"
        for i in range(len(ports)):
               print ports[i] + '\t', instances[i]

    # * * * * * * * * * * * * *

    # (4) Breakdown of all transport layer protocols

    #headers needed: proto (7)
    if x == 4:
        proto = []
        instances = []
        for rownum in range(log.nrows):
            if rownum > 1:
                s = log.cell(rownum,7).value
                if s not in proto:
                    proto.append(s) 
                    ind = proto.index(s)
                    instances.append(1)
                else:
                    ind = proto.index(s)
                    instances[ind] += 1
        print "PROTO" + '\t' + "INSTANCES"
        for i in range(len(proto)):
               print proto[i] + '\t', instances[i]

    # * * * * * * * * * * * * *

    # (5) Breakdown of all origination country codes
    if x == 5:
        cc = []
        instances = []
        
        for rownum in range(log.nrows):
            if rownum > 1:
                s = (str)(log.cell(rownum,21).value)
                if s not in cc:
                    cc.append(s) 
                    ind = cc.index(s)
                    instances.append(1)
                else:
                    ind = cc.index(s)
                    instances[ind] += 1
        country = []
        for i in range(len(cc)):
            country.append('-')
        with open('cc.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] in cc:
                    ind = cc.index(row[0])
                    country[ind] = row[1]
        f = input("Check for occurrences less than (input a number): ")
        print "CC" + '\t' + "INSTANCES" + '\t' + "COUNTRY" 
        for i in range(len(cc)):
            if instances[i] < f:
                print cc[i] + '\t', instances[i], '\t', country[i]
                

    # * * * * * * * * * * * * *

    # (8) Data based on UID
    if x == 8:
        # input a UID
        # all data
        headerunicode = []
        header = []
        data = []
        uid = raw_input('Enter a UID: ')
        for item in log.row(0):
            header.append(item.value)
        #for item in header:
            #print item
        for rownum in range(log.nrows):
            if rownum > 1:
                uidcheck = log.cell(rownum,2).value
                if (uidcheck == uid):
                    for element in log.row(rownum):
                        data.append(element.value)
        for i in range(len(header)):
            print header[i] + ': ' + data[i] + '\n'
    # * * * * * * * * * * * * *
    
    y = raw_input('Do you want to continue? (y/n): ')
    if y == 'y':
        continue
    if y == 'n':
        sys.exit()
                    
    
