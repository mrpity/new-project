#coding: utf_8

import sys
import pexpect


router_un = "root"
router_pw = "1DFl1H45"

test
#enable debugging
#import ipdb; ipdb.set_trace()

#range includes all numbers from the diapason without the last one
for x in range(150, 153):
#for x in [151, 152]:
          router_ip = "10.100.100.%s" % x
	  try:
              child = pexpect.spawn('ssh %s@%s' % (router_un, router_ip))
              child.timeout = 4
              child.expect('Password:')
          except pexpect.TIMEOUT:
	      f = open('mylog.txt', 'a+')
              f.write("Couldn't log on to the %s\n" % router_ip)
              f.close()
          else:
              child.sendline(router_pw)
              child.expect('#')
              child.sendline('conf t')
#              child.logfile = sys.stdout
              child.logfile = open('mylog.txt', 'a+')
              child.expect('\(config\)#')
              child.sendline('ip route 8.8.8.8 255.255.255.255 10.100.100.1')
              child.expect('#')
              child.sendline('end')
              child.expect('#')
              child.sendline('wr mem')
              child.expect('[OK]')
              child.expect('#')
              child.sendline('quit')
