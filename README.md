# Bro-Log-Data-Analytics
Bro log data analytics for shits and gigs. input some log files and output some analysis.
### what is this?
so there's four files:

    - cc.csv (you're gonna need this for conn-analysis)
    - conn-analysis.py (analysis on connection log analysis)
    - excel-script.py (gzip files -> excel spreadsheet)
    - http-analysis.py (guess what this does)
###### you're gonna need all of these + any gzip logs you have laying around
### how to use
    1. python excel-script.py
    2. python conn-analysis.py OR python http-analysis.py
    drop down menus should show up and you just need to follow the instructions

### but i have different needs/wants/log types!
have no fear, it's pretty customizable.

just change the excel-script to fit what file name you have and change the delimiter + any special rules you may have for your files.
```python
http_filename = 'your_file_name.your_file_type' #line 9
for i in range(0,num_data_points):  #line 11
lines = file_content.split('your_delimiter') #line 18
```
### i want more analysis!
just look at the existing examples for ideas on how to start. like this one:
figure out what headers you need, perform your analysis, and print out the data you collected. _ezpz_.
```python
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
```
### why?
why not
