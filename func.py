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

def matchIP():
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
        else:
              pass
    return IParray

#list of domain name
domainlist = ['www.msftncsi.com', 'clients1.google.com', 'clients2.google.com', 'clients3.google.com', 'clients4.google.com', 'clients5.google.com','clients6.google.com', 'clients7.google.com','clients8.google.com', 'clients9.google.com', 'apple.com', 'itools.info', 'ibook.info', 'thinkdifferent.us', 'airport.us', 'appleiphonecheck.com']

"""
get list of ip addresses with help of nslookup
"""

def nslookup(domainlist):
    dictIP = {}
    for name in domainlist:
        dictIP[name] = filter(lambda x: bool(x), subprocess.Popen("nslookup %s | grep 'Address: ' | sed 's/Address: //g'" % name, shell=True, stdout=subprocess.PIPE).communicate()[0].split("\n"))
    return dictIP

def createListfor(dictIP):
    listResult = []
    for x in dictIP:
        if bool(dictIP[x]):
            listResult.append(dictIP[x])
        else:
            pass
    NewListResult = list()
    for x in listResult:
        NewListResult.extend(x)
    return NewListResult


"""
find matches - ip octets
"""

def matchOctets(newListIP, IParray):
    matches_arr = dict()
    for ip1 in newListIP:
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

def mailCreate(mailResult):
    result = dict()
    for site in dictIP:
        for x in mailResult:
            if x in dictIP[site]:
                result[site] = x
            else:
                 pass
    return result


"""
transfer ACL in Functions and send email
"""

listACL = ['inet5', 'inet3']

for oneACL in listACL:
    WLC('mr.pity', 'Neistrebim1201', '10.1.19.10', oneACL )
    dictIP = nslookup(domainlist)
    newListIP = createListfor(dictIP)
    IParray = matchIP()
    result = matchOctets(newListIP, IParray)
    mailResult = []
    for x in result:
       if result[x] == 0:
           print(x, "NET sovpodeniy")         
           mailResult.append(x)
       elif result[x] == 1:
            pass
       elif result[x] == 2:
            pass
       else:
            pass
    mailMessage = mailCreate(mailResult)
    
    if mailMessage != 0:
    #SMTP configuration
        to = 'd@wi-fi-bar.com'
#    message = '<br> Нет совпадения с : '.join(str(mailMessage))
        message = '<br> Нет совпадения с : '.join([''] + map(str, mailMessage.iteritems()))
        subject = "ip in ACL: {}".format(oneACL)
        msg = 'To: %s\r\nContent-Type: text/html; charset="utf-8"\r\nSubject: %s\r\n' % (to, subject)
        msg += message
        server = smtplib.SMTP('z.wi-fi-bar.com:25')
        server.sendmail('zabbix-report@wi-fi-bar.com', to , msg)
    else:
        to = 'd@wi-fi-bar.com'
#    message = '<br> Нет совпадения с : '.join(str(mailMessage))
        message = 'Аксесс листы сопадают!'
        subject = "ip in ACL: {}".format(oneACL)
        msg = 'To: %s\r\nContent-Type: text/html; charset="utf-8"\r\nSubject: %s\r\n' % (to, subject)
        msg += message
        server = smtplib.SMTP('z.wi-fi-bar.com:25')
        server.sendmail('zabbix-report@wi-fi-bar.com', to , msg)
        

