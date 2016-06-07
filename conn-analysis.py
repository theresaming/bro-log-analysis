import xlwt, xlrd, sys, datetime, time, unicodedata

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
    print "(5) EMPTY"
    print "(6) EMPTY"
    print "(7) EMPTY"
    print "(8) EMPTY"
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
    
    y = raw_input('Do you want to continue? (y/n): ')
    if y == 'y':
        continue
    if y == 'n':
        sys.exit()
                    
    
