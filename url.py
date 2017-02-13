#-*-coding:utf-8 -*-
import os
import urllib2
import time 
from error import reinternet,errorType

headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
hurl='http://tj.lianjia.com/ershoufang/housestat?hid=%s&rid=%s'
retry_count=3

def get_page(url):
    print url
    for i in range(retry_count):
        try:
            page = urllib2.urlopen(urllib2.Request(url,headers=headers),timeout=10)
            html = page.read()
        except urllib2.HTTPError,e:
            if e.getcode() == 404:
                raise "404 page not found:%s"%url
            else:
                raise
        except:
            if i == 2:
                raise
            time.sleep(1)
            print "url read exception : %s"%url

    if errorType(html) == 'server_refused':
        reinternet()
        html = get_page(url)
    if -1 != html.find('MIWIFI'):
        html = get_page(url)

    return html

def get_json_info(houseid,rid):
    return get_page(hurl%(houseid,rid))

if __name__=='__main__':
    get_json_info('101100480930','1211045780133')
   

