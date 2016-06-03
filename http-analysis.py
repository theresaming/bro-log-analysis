#import gzip
import xlwt, xlrd, sys, time

#automated data analysis on http logs

#open the httplogs excel and write to a new sheet
#find the sheet number (logs are every other starting at 0)
wb = xlrd.open_workbook('httplogs.xls')
log = wb.sheet_by_index(0)

#I/O
looper = True
while looper:
    print "HTTP Analysis - Options (type a number)"
    print "(1) Find IP adresses of web servers that send more than 1 KB back to a client"
    print "(2) Find breakdown of http methods"
    print "(3) Find breakdown of transferred file types"
    print "(4) Find breakdown of all ports"
    print "(5) Failed connection attempts per source address"
    print "(6) Distinct browsers in this trace"
    print "(7) Top 10 referred hosts"
    print "(8) End program."

    #input value/choice
    try:
        x = input('Enter a value: ')
        if x == 8:
                sys.exit()
        if x < 1 or x > 8:
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
    
    y = raw_input('Do you want to continue? (y/n): ')
    if y == 'y':
        continue
    if y == 'n':
        sys.exit()
                        
            
        

