#!/usr/bin/python
#-*-coding:utf-8 -*-
import re
import urllib2
import os
import MySQLdb
import time
import shutil
from parser import page_parser

def get_html_and_save(url,wfile):
    headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    page=urllib2.urlopen(urllib2.Request(url,headers=headers))
    html = page.read()
    index_file=open(wfile,'w')
    index_file.write(html)
    index_file.close()
    page.close()
    return html

def parse_index_file(fname,houses):
    house_pattern='<a class="" href=.* target="_blank" data-log_index="[0-9]*"   data-el="ershoufang"  data-sl="">.*</a>'
    http_pattern='http://.*\.html'
    index_file=open(fname)
    for line in index_file:
        match_obj=re.search(house_pattern,line)
        if match_obj:
            http_mobj=re.search(http_pattern,line)
            houses.append(http_mobj.group())
    index_file.close()

def save_url_houses(seed_url):
    for region in seed_url.keys():
        os.mkdir(region)
        region_url = seed_url[region]
        print "open %s"%region_url
        html = get_html_and_save(region_url,'%s/%s.html'%(region,region))
        total_index = html.index('totalPage')
        total_index = total_index + 11
        total_index_end = html.index(',',total_index)
        total_page  = int(html[total_index:total_index_end])
        for pindex in range(2,total_page+1):
            suburl = "%spg%d/"%(region_url,pindex)
            print "open %s"%suburl
            get_html_and_save(suburl,'%s/%s_page%d.html'%(region,region,pindex))
    
        houses=[]
        for f in os.listdir(region):
            fname=os.path.join(region,f)
            if os.path.isfile(fname):
                parse_index_file(fname,houses)
    
        house_dir = "%s/house"%region
        os.mkdir(house_dir)
        for house in houses:
            print "open %s"%house,
            house_id = house[house.rfind('/')+1:house.rfind('.')]
            get_html_and_save(house,'%s/house/%s.html'%(region,house_id))
            print " success"
    
def get_overview_info(fname):
    overview=''
    if os.path.isfile(fname):
        house_info=open(fname)
        in_overview = False
        for line in house_info:
            if in_overview:
                overview += line 
                if line.find('</div>') == 0:
                    break
            else:
                if line.find('overview') != -1:
                    overview += line
                    in_overview = True
        house_info.close()
    return overview
             
def save_houses_info(seed_url,cursor):

    for region in seed_url.keys():
        house_dir = "%s/house"%region
        for fn in os.listdir(house_dir):
            fname = os.path.join(house_dir,fn)
            print 'parse %s'%fname
            pageinfo = open(fname).read()
            record = page_parser(pageinfo)

            house_id   = record.houseid
            community  = record.communityName
            house_type = record.type
            sub_info   = record.sub_info
            
            house_area = record.area
            total      = record.total
            price      = record.price
            affected   = cursor.execute(r"insert into regions.%s values('%s','%s','%s','%s','%s','%s','%s','%s')"\
                                       %(region,date_now,house_id,house_area,community,house_type,sub_info,total,price))


seed_url={'tyc':'http://tj.lianjia.com/ershoufang/taiyangcheng/','mj':'http://tj.lianjia.com/ershoufang/meijiang/'}

date_now=time.strftime("%Y-%m-%d")
'''
if os.path.exists(date_now):
    shutil.rmtree(date_now)

os.mkdir(date_now)
'''
os.chdir(date_now)

#save_url_houses(seed_url)

conn = MySQLdb.connect('127.0.0.1','root','111111','',3306)
cur = conn.cursor()
cur.execute("SET NAMES utf8")

save_houses_info(seed_url,cur)
conn.commit()    

