#import gzip
import xlwt, xlrd, sys, datetime, time, unicodedata

#automated data analysis on http logs

#open the httplogs excel and write to a new sheet
#find the sheet number (logs are every other starting at 0)
wb = xlrd.open_workbook('httplogs.xls')
log = wb.sheet_by_index(0)

#I/O
looper = True
while looper:
    print "HTTP Analysis - Options (type a number)"
    print "(1) IP adresses of web servers that send more than 1 KB back to a client"
    print "(2) Breakdown of http methods"
    print "(3) Breakdown of transferred file types"
    print "(4) Breakdown of all ports"
    print "(5) Failed connection attempts per source address"
    print "(6) List of distinct browsers"
    print "(7) Time interval anomalies based on host"
    print "(8) Data based on UID"
    print "(9) End program."

    #input value/choice
    try:
        x = input('Enter a value: ')
        if x == 9:
                sys.exit()
        if x < 1 or x > 9:
            print "Not a valid number. Choose a number between 1 and 7."
    except ValueError:
        print "Not a valid number. Choose a number between 1 and 7."

    # * * * * * * * * * * * * * 
    #(1) Find IP adresses of web servers that send more than 1 KB back to a client

    # headers needed: id.resp_h (5) & response_body_length (13)
    if x == 1:
        # initialize an array of unique values
        arr = []
        for rownum in range(log.nrows):
            # find elements with value of more than 1 KB
            if rownum > 1 and log.cell(rownum,13).value > 1000:
                val = log.cell(rownum,5).value
                # traverse existing array to find common values
                if val not in arr:
                    arr.append(val)
                    
        # sort & print array
        arr.sort()
        pub = 0
        pri = 0
        for element in arr:
            print element
            if element.startswith("10") or element.startswith("172") or element.startswith("192"):
                pub+=1
            else:
                pri+=1
                
        print "\nAdditional information: "
        print "Number of unique IPs: ",len(arr)
        print "Number of public IPs: ",pub
        print "Number of private IPs: ",pri
            
    time.sleep(1)

    # * * * * * * * * * * * * *

    # (2) Find breakdown of http methods
    # headers needed: method (8)
    if x == 2:
        methods = []
        instances = []
        for rownum in range(log.nrows):
            if rownum > 1:
                s = log.cell(rownum,8).value
                if s not in methods:
                    methods.append(s)
                    ind = methods.index(s)
                    instances.append(1)
                else:
                    ind = methods.index(s)
                    instances[ind] += 1
        print "METHOD" + '\t' + "INSTANCES"
        for i in range(len(methods)):
            print methods[i] + '\t',instances[i]           

    # * * * * * * * * * * * * *

    # (3) Find breakdown of transferred file types
    # headers needed: resp_mime_types(27)
    if x == 3:
        ftype = []
        instances = []
        for rownum in range(log.nrows):
            if rownum > 1:
                s = log.cell(rownum,27).value
                if s not in ftype:
                    ftype.append(s)
                    ind = ftype.index(s)
                    instances.append(1)
                else:
                    ind = ftype.index(s)
                    instances[ind] += 1
        print "FILE" + '\t' + "INSTANCES"
        for i in range(len(ftype)):
                print ftype[i] + '\t', instances[i]

    # * * * * * * * * * * * * *

    # (4) Find breakdown of all ports
    # headers needed: id.resp_p (7)
    if x == 4:
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

    # (5) Failed connection attempts per source address
    # headers needed: hosts(9) info_code (17)
    if x == 5:
        hosts = []
        attempts = []
        for rownum in range(log.nrows):
            if rownum > 1:
                code = log.cell(rownum,15).value #value of error code
                host = log.cell(rownum,9).value #value of host
                if host not in hosts and (code.startswith("4") or code.startswith("5")):
                    #if the code indicates failed connection
                    hosts.append(host)
                    ind = hosts.index(host)
                    attempts.append(1)
                elif host in hosts and (code.startswith("4") or code.startswith("5")):
                    ind = hosts.index(host)
                    attempts[ind] += 1
        print "HOSTS" + ', ' + "ATTEMPTS"
        for i in range(len(hosts)):
            print hosts[i] + ', ',attempts[i]
                
    # * * * * * * * * * * * * *

    # (6) List of distinct browsers
    if x == 6:
        browsers = []
        for rownum in range(log.nrows):
            e = log.cell(rownum,12).value
            if e not in browsers:
                browsers.append(e)
        browsers.sort()        
        for i in range(len(browsers)):
            print browsers[i]

    # * * * * * * * * * * * * *

    # (7) Time interval anomalies based on host
    if x == 7:
        # input a host
        times = [] #raw time information
        uid = [] #uid of instances
        
        hostinput = raw_input('Enter a host: ')
        for rownum in range(log.nrows): #traverse 
            if rownum > 1:
                hostcheck = log.cell(rownum,9).value
                if hostcheck == hostinput:  # adds matching host times into the times array
                    hosttime = log.cell(rownum,1).value #find time of corresponding host
                    t = datetime.datetime.strptime(hosttime, '%Y-%m-%d %H:%M:%S') #convert element to time 
                    times.append(t) #append that element to the raw times
                    uid.append(log.cell(rownum,2).value) #append the corresponding uid
        intervals = [] #time intervals
        for i in range(len(times) - 1):
            intervals.append(times[i+1]-times[i])
            #calculate time intervals /choose times[i+1] index for uid     
        instances = []
        unique = []
        u_uid = []
        for k in range(len(intervals)):
            if intervals[k] not in unique:
                unique.append(intervals[k])
                ind = unique.index(intervals[k]) #index of the corresponding unique time interval
                instances.append(1)
                u_uid.append(uid[k+1])
            else:
                ind = unique.index(intervals[k])
                u_uid.append(uid[k+1])
                instances[ind]+=1       
        print "TIME INTERVALS" + '\t' + "INSTANCES" + '\t' + "UID"
        for i in range(len(unique)):
            print str(unique[i]),'\t',instances[i],'\t',u_uid[i]
                                   
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
                        
            
        

