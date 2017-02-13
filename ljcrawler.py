#-*-coding:utf-8 -*-
#!/usr/bin/python
import re
import urllib2
import os
import sys
import MySQLdb
import time
from url import get_page
from cactotal import save_total_info_to_db 
from lxml import etree
from lxml.html.clean import Cleaner
import getopt

def save_html_page(url,fname):
    page=get_page(url)
    f=open(fname,'w')
    f.write(page)
    return page

def save_url_houses(date,seed_url):
    os.mkdir(date)
    for region in seed_url.keys():
        path = os.path.join(date,region)
        os.mkdir(path)
        region_url = seed_url[region]
        html = save_html_page(region_url,'%s/%s.html'%(path,region))
        total_index = html.index('totalPage')
        total_index = total_index + 11
        total_index_end = html.index(',',total_index)
        total_page  = int(html[total_index:total_index_end])

        for pindex in range(2,total_page+1):
            suburl = "%spg%d/"%(region_url,pindex)
            save_html_page(suburl,'%s/%s_page%d.html'%(path,region,pindex))


def save_houses_info(date,seed_url,cursor):
    for area in seed_url.keys():
        path = date + "/" + area
        if not os.path.exists(path):
            continue
        for fn in os.listdir(path):
            fname = os.path.join(path,fn)
            print fname
            if os.path.isdir(fname):
                continue
            cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=False)
            page = open(fname).read()
            tree=etree.HTML(page) 
 
            houses = tree.xpath('.//div[@class="info clear"]') 
            for house in houses: 
                hid          = house.xpath('.//div[@class="unitPrice"]/@data-hid')[0] 
                rid          = house.xpath('.//div[@class="unitPrice"]/@data-rid')[0] 
                price        = house.xpath('.//div[@class="unitPrice"]/@data-price')[0]
                district     = house.xpath('.//div[@class="houseInfo"]/a/text()')[0] 
                info         = house.xpath('.//div[@class="houseInfo"]/text()') 
                info         = [x for x in info if len(x.strip('\n \t')) > 0]
                totalPrice   = house.xpath('.//div[@class="priceInfo"]/div/span/text()')[0] 
                followInfo   = house.xpath('.//div[@class="followInfo"]/text()')[0] 
                positionInfo = house.xpath('.//div[@class="positionInfo"]/text()')[0] 
                region       = house.xpath('.//div[@class="positionInfo"]/a/text()')[0] 

                infoList     = [i.strip() for i in info[0].split('|')]
                positionInfo = positionInfo.rstrip().rstrip('-').strip()
                followList   = [i.strip() for i in followInfo.split('/')]
#print rid,hid,region,district,infoList[1],infoList[2],infoList[3],infoList[4],totalPrice,price,followList[0],followList[1],followList[2],positionInfo
                sql = "insert into area.%s values('%s','%s','%s','%s','%s','%s','%s',\
                                                  '%s','%s','%s','%s','%s','%s','%s','%s')"\
                                                   %(area,date,hid,rid,region,district,infoList[1],infoList[2],infoList[3],infoList[4],totalPrice,price,followList[0],followList[1],followList[2],positionInfo)
                cursor.execute(r"%s"%sql.encode('utf-8'))
def usage():  
    print("Usage:%s [--history] args" %sys.argv[0]); 

if __name__=='__main__':

    history = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["history","help"])
        for opt,arg in opts:  
            if opt in ("-h", "--help"):  
                usage()  
                sys.exit(1)  
            elif opt in ("--history"):  
                history=True
            else:  
                usage()
                sys.exit(2)
    except getopt.GetoptError:
            usage()
            sys.exit(3)
        
    seed_url={ 'tyc':'http://tj.lianjia.com/ershoufang/taiyangcheng/',
               'mj':'http://tj.lianjia.com/ershoufang/meijiang/'}
 
    conn = MySQLdb.connect('127.0.0.1','root','111111','',3306)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
   
    if not history:
        date_now=time.strftime("%Y-%m-%d")
        if os.path.exists(date_now):
            print "Directory exist! Dumplicate house data"
            sys.exit()
        save_url_houses(date_now,seed_url)
        save_total_info(cur)
        past = [date_now]
    else:
        pattern = re.compile('\d{4}-\d\d-\d\d')
        past = (x for x in os.listdir('.')  if pattern.match(x))
    for day in past:
        save_houses_info(day,seed_url,cur)

    conn.commit()    
    
