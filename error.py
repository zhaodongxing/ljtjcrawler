#-*-coding:utf-8 -*-
import os
import time
def errorType(page):
    if -1 != page.find('流量异常'):
        return 'server_refused'
    else:
        return  'server_responsed'

def reinternet():
    print "please close the network"
    
    while not os.system("ping www.163.com -c 1 >/dev/null 2>&1"):
        time.sleep(1)
        print "network active"

    print "please connect the network"

    while os.system("ping www.163.com -c 1 >/dev/null 2>&1"):
        time.sleep(1)
        print "network inactive"
    print "network active again"
