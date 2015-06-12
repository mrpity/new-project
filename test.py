import smtplib

list1 = ['1.1.1.1', '2.2.2.2', '2.1.3.5', '6.2.5.7', '8.2.3.8']
list2 = ['1.1.2.2', '2.1.1.1', '5.5.5.5']

matches_arr = dict()
for ip1 in list1:
    matches = list()
    for ip2 in list2:
        match = 0
        for i, byte1 in enumerate(ip1.split('.')[:2]):
            if match == 0 and i > 0:            
                break
            match += bool(byte1 == ip2.split('.')[i])
        matches.append(match)
#        print match
    matches_arr.update({ip1: max(matches)})

#print matches_arr
for x in matches_arr:
   if matches_arr[x] == 0:
#        print matches_arr[x]
        to = 'd@wi-fi-bar.com'
        message = "Netu sovpadeniya ne s odmin ip in ACL " + x  
        subject = "test"
        if message:
            print "Ok"
            msg = 'To: %s\r\nContent-Type: text/html; charset="utf-8"\r\nSubject: %s\r\n' % (to, subject)
            msg += message
            server = smtplib.SMTP('z.wi-fi-bar.com:25')
            server.sendmail('zabbix-report@wi-fi-bar.com', to , msg)
        else:
            print "file is empty"
   else:
       print("vse sovpalo", matches_arr[x])

