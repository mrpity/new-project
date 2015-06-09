#coding: utf_8

""" 
This Script gets the list of nets that contains Flexconnect ACL inet3
"""


import sys
import pexpect
import  subprocess, os, sys, re, smtplib


router_user = "mr.pity"
router_pass = "Neistrebim1201"

#enable debugging
#import ipdb; ipdb.set_trace()

"""
Connect to WCL and write flexACL in file:mylog.txt
"""
router_ip = "10.1.19.10"
child = pexpect.spawn('ssh %s@%s' % (router_user, router_ip))
#child.logfile = sys.stdout  #show the output inform on the terminal
child.logfile = open('mylog.txt', 'w+')
child.timeout = 10
child.expect('.*:')
child.sendline(router_user)
child.expect('.*:')
child.sendline(router_pass)
child.expect('.*>')
child.sendline("show flexconnect acl detailed inet3")
child.expect('.*') #need to do if construction
child.sendline('')
child.expect('.*')
child.sendline('')
child.expect('.*')
child.sendline('')
child.expect('.*>')
child.sendline('logout')

"""
look the file through and with help of rv  find ip address of network
"""

f = open('/var/www/html/javascriptCourse/MY_PEOJECT/new-project/mylog.txt')
IParray = []  # list of  nets in ACL
ipPattern = re.compile(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(.*)') 
for line in f: 
    findIP = re.search(ipPattern,line)
    if findIP:
#       print "Found match", findIP.group(1)
       if findIP.group(1) !=  "0.0.0.0":
           IParray.append(findIP.group(1))
       else:
            pass
#           print("something wrong!")
    else:
            pass
#       print("Found nothing", line)
for x in IParray:
    print x
print ("______________________________________________________________________________")


"""
get ip adresses with help of nslookup
"""


domainlist = ['www.msftncsi.com', 'clients1.google.com', 'clients2.google.com', 'clients3.google.com', 'clients4.google.com', 'clients5.google.com','clients6.google.com', 'clients7.google.com','clients8.google.com', 'clients9.google.com', 'apple.com', 'itools.info', 'ibook.info', 'thinkdifferent.us', 'airport.us', 'appleiphonecheck.com']

listIP = []
for name in domainlist:
    listIP.append(subprocess.Popen("nslookup %s | grep 'Address: ' | sed 's/Address: //g'" % name, shell=True, stdout=subprocess.PIPE).communicate()[0])
listIP = filter(lambda x: bool(x), listIP)
#Some nslookups results return 2 or more ip adresses, so we need to split it and add to newList separatey
newList = []
for x in listIP:
    if x.split("\n"):
         for y in x.split("\n"):
             newList.append(y)
    else:
        newlist.append(x)
newList = filter(lambda x: bool(x), newList)

for x in newList:
    print x


