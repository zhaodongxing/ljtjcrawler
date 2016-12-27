#-*-coding:utf-8 -*-
import os
import urllib2
import time

headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
url='http://tj.lianjia.com/ershoufang/housestat?hid=%s&rid=%s'
retry_count=3

def get_page_pages():
    page=None

    for i in range(retry_count):
        try:
            page = urllib2.urlopen(urllib2.Request(url,headers=headers))
            html = page.read()
        except urllib2.HTTPError,e:
            if e.getcode() == 404:
                return None 
            else:
                raise
        except:
            if i == 2:
                raise
            time.sleep(1)
            print "url read exception : %s"%url

    return page

         

def get_json_info(houseid,rid):


test()
