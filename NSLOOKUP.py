#coding: utf_8


import subprocess, os, sys, re, smtplib

domainlist = ['www.msftncsi.com', 'clients1.google.com', 'clients2.google.com', 'clients3.google.com', 'clients4.google.com', 'clients5.google.com','clients6.google.com', 'clients7.google.com','clients8.google.com', 'clients9.google.com', 'apple.com', 'itools.info', 'ibook.info', 'thinkdifferent.us', 'airport.us', 'appleiphonecheck.com']

listIP = []
for name in domainlist:
    listIP.append(subprocess.Popen("nslookup %s | grep 'Address: ' | sed 's/Address: //g'" % name, shell=True, stdout=subprocess.PIPE).communicate()[0])
listIP = filter(lambda x: bool(x), listIP)

newList = []
for x in listIP:
    if x.split("\n"):
         for y in x.split("\n"):
             newList.append(y)
    else:
        newlist.append(x)
newList = filter(lambda x: bool(x), newList)

#for x in domainlist:
#     print x + ":"
#     dima = subprocess.call("nslookup %s | grep 'Address: ' | sed 's/Address: //g'" % x, shell=True)

pattern = re.compile(r'(\d*)\.(\d*)\.(\d*)\.(\d*)')
string = '17.142.49.2'
for x in newList:
    line = re.search(pattern, x)
    test = re.search(pattern, string)
    
#    print line.group(0), line.group(1), line.group(2)
    if line.group(1) == test.group(1):
        print("The first match was found:", test.group(1))
        if line.group(2) == test.group(2):
            print ("The second match was found:", test.group(1), "and", test.group(2), "from", test.group(0))
        else:
            print ("It mathces for the first octet only:", test.group(1))
    else:
        print("Ne ok", line.group(1), "is not", test.group(1) )

