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
print (IParray)


#f = open('/var/www/html/javascriptCourse/MY_PEOJECT/new-project/mylog.txt')
#IParray = []
#patternIP = re.compile('(.*)\/(.*)')
#for line in f:
#    result = patternIP.match(line)
#    if result:    
#       print(result.group(0))
#    else:
#       print("Found nothing!")



#   child.logfile_read = sys.stdout
#f = open('mylog.txt', 'a+')
#child.sendline('y')
#child.logfile = open('mylog.txt', 'a+')

#child.logfile_read = sys.stdout  #show the output inform on the terminal
#child.expect('.*>')
#child.logfile = open('mylog.txt', 'a+')
#              child.interact()   #Give the control to user
#child.sendline('logout')

#print (child.logfile)

#get AP name
#patternAP = re.compile('^SNMPv2-SMI::enterprises\.14179\.2\.2\.1\.1\.3\.(\d*).*\:\s\"(.*)\"')
#queryAP = subprocess.Popen(["snmpwalk", "-v2c", "-cpity-test", "10.1.19.10", "1.3.6.1.4.1.14179.2.2.1.1.3"], stdout=subprocess.PIPE)


#APname = {}
#for line in queryAP.stdout:
#        result = patternAP.match(line)
#        APname[result.group(1)] = result.group(2)
#        print result.group(2)
