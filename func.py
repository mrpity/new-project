#coding: utf_8

""" 
This Script gets the list of networks that contains Flexconnect ACL inet3,5. 
"""

import sys
import pexpect
import  subprocess, os, sys, re, smtplib


def WLC(router_user, router_pass, router_ip, acl):
    """
    Connect to WCL and write flexACL in file:mylog.txt
    """
    child = pexpect.spawn('ssh %s@%s' % (router_user, router_ip))
    child.logfile = open('mylog.txt', 'w+')
    child.timeout = 10
    child.expect('.*:')
    child.sendline(router_user)
    child.expect('.*:')
    child.sendline(router_pass)
    child.expect('.*>')
    child.sendline("show flexconnect acl detailed %s" % (acl))
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

def match():
    f = open('/var/www/html/javascriptCourse/MY_PEOJECT/new-project/mylog.txt')
    IParray = []  # list of  nets in ACL
    ipPattern = re.compile(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(.*)')
    for line in f:
        findIP = re.search(ipPattern,line)
        if findIP:
           if findIP.group(1) !=  "0.0.0.0":
               IParray.append(findIP.group(1))
           else:
               pass
#           print("something wrong!")
        else:
              pass
#       print("Found nothing", line)
#    for x in IParray:
#        print x
#    print ("______________________________________________________________________________")
    return IParray


#list of domain name
domainlist = ['www.msftncsi.com', 'clients1.google.com', 'clients2.google.com', 'clients3.google.com', 'clients4.google.com', 'clients5.google.com','clients6.google.com', 'clients7.google.com','clients8.google.com', 'clients9.google.com', 'apple.com', 'itools.info', 'ibook.info', 'thinkdifferent.us', 'airport.us', 'appleiphonecheck.com']

"""
get list of ip addresses with help of nslookup
"""

def nslookup(domainlist):
    listIP = []
    for name in domainlist:
        listIP.append(subprocess.Popen("nslookup %s | grep 'Address: ' | sed 's/Address: //g'" % name, shell=True, stdout=subprocess.PIPE).communicate()[0])
    listIP = filter(lambda x: bool(x), listIP)  #check '' in listIP and delete this element
#Some nslookups results return 2 or more ip adresses, so we need to split it and add to newList separatey
    newList = []
    for x in listIP:
        if x.split("\n"):
             for y in x.split("\n"):
                 newList.append(y)
        else:
            newlist.append(x)
    newList = filter(lambda x: bool(x), newList)
    return newList 


"""
find matches - ip octets
"""

def matchOctets(newList, IParray):
    matches_arr = dict()
    for ip1 in newList:
        matches = list()
        for ip2 in IParray:
            match = 0
            for index, octet in enumerate(ip1.split('.')[:3]):
                if match == 0 and index > 0:
                    break
                match += bool(octet == ip2.split('.')[index])
            matches.append(match)
        matches_arr.update({ip1: max(matches)})
    return matches_arr


"""
transfer ACL in Functions and send email
"""

listACL = ['inet5', 'inet3']

for oneACL in listACL:
    WLC('mr.pity', 'Neistrebim1201', '10.1.19.10', oneACL )
    IParray = match()
    newList = nslookup(domainlist)
    result = matchOctets(newList, IParray)

    mailResult = []
    for x in result:
       if result[x] == 1:
           print(x, "odno sovpadenie"
           mailResult.append(x)
       elif result[x] == 2:
           print(x, "dva sovpadenie")
    print(mailResult)


    #SMTP configuration
    to = 'd@wi-fi-bar.com'
    message = '<h1>\r\n'.join(mailResult)
    subject = "ip in ACL: {}".format(oneACL)
    msg = 'To: %s\r\nContent-Type: text/html; charset="utf-8"\r\nSubject: %s\r\n' % (to, subject)
    msg += message
    server = smtplib.SMTP('z.wi-fi-bar.com:25')
    server.sendmail('zabbix-report@wi-fi-bar.com', to , msg)
        

