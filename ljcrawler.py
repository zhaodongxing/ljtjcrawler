#-*-coding:utf-8 -*-
#!/usr/bin/python
import re
import urllib2
import os
import sys
import MySQLdb
import time
from parser import page_parser
from url import get_page
crawl_delay = 2

def save_html_page(url,fname):
    page=get_page(url)
    f=open(fname,'w')
    f.write(page)
    return page

def parse_index_file(fname,houses):
    page=open(fname).read()
    offset = 0
    url_key='<a class="" href="'
    while True:
        offset = page.find(url_key,offset)
        if offset == -1:
            break 
        offset = offset + len(url_key)
        off_end = page.find('"',offset)
        if off_end == -1:
            raise "page format error" 
        url = page[offset:off_end]
        houses.append(url)

def save_url_houses(seed_url):
    for region in seed_url.keys():
        os.mkdir(region)
        region_url = seed_url[region]
        html = save_html_page(region_url,'%s/%s.html'%(region,region))
        total_index = html.index('totalPage')
        total_index = total_index + 11
        total_index_end = html.index(',',total_index)
        total_page  = int(html[total_index:total_index_end])

        for pindex in range(2,total_page+1):
            suburl = "%spg%d/"%(region_url,pindex)
            save_html_page(suburl,'%s/%s_page%d.html'%(region,region,pindex))

        houses=[]
        for f in os.listdir(region):
            fname=os.path.join(region,f)
            if os.path.isfile(fname):
                parse_index_file(fname,houses)
        print "found %d houses"%len(houses)
    
        house_dir = "%s/house"%region
        os.mkdir(house_dir)
        for house in houses:
            house_id = house[house.rfind('/')+1:house.rfind('.')]
            save_html_page(house,'%s/house/%s.html'%(region,house_id))
    
    
def save_houses_info(seed_url,cursor):

    for region in seed_url.keys():
        house_dir = "%s/house"%region
        for fn in os.listdir(house_dir):
            fname = os.path.join(house_dir,fn)
            print 'parse %s'%fname
            pageinfo = open(fname).read()
            record = page_parser(pageinfo)

            sql = "insert into regions.%s values('%s','%s','%s','%s','%s','%s','%s',\
                                                  '%s','%s','%s','%s','%s','%s')"\
                                                   %(region,date_now,record.houseid,record.area,record.region,\
                                                     record.sub_region,record.housetype,record.communityName,\
                                                     record.type,record.sub_info,record.total,record.price,\
                                                     record.totalvisit,record.recentvisit)
            cursor.execute(r"%s"%sql)


if __name__=='__main__':

    seed_url={ #'tyc':'http://tj.lianjia.com/ershoufang/taiyangcheng/'},
               'mj':'http://tj.lianjia.com/ershoufang/meijiang/'}
    
    date_now=time.strftime("%Y-%m-%d")
    if os.path.exists(date_now):
        print "Directory exist! Dumplicate house data"
        sys.exit()
    
    os.mkdir(date_now)
    os.chdir(date_now)

    save_url_houses(seed_url)
    
    
    conn = MySQLdb.connect('127.0.0.1','root','111111','',3306)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    
    save_houses_info(seed_url,cur)
    conn.commit()    
    
