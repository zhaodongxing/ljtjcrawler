#-*-coding:utf-8 -*-
#!/usr/bin/python
import re
import urllib2
import os
import sys
import MySQLdb
import time
from parser import page_parser
crawl_delay = 2

def save_html_page(page):
    f=open(wfile,'w')
    f.write(page)
    f.close()

def get_html_page(url):
    headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0"}
    page=None
    for i in range(3):
        try:
            page=urllib2.urlopen(urllib2.Request(url,headers=headers))
            html = page.read()
            break
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
        for i in range(3):
            try:
                html = get_html_and_save(region_url,'%s/%s.html'%(region,region))
                total_index = html.index('totalPage')
                total_index = total_index + 11
                total_index_end = html.index(',',total_index)
                total_page  = int(html[total_index:total_index_end])
            except:
                if i == 2:
                    raise

        time.sleep(crawl_delay)
        for pindex in range(2,total_page+1):
            suburl = "%spg%d/"%(region_url,pindex)
            print "open %s"%suburl
            for i in range(3):
                try:
                    get_html_and_save(suburl,'%s/%s_page%d.html'%(region,region,pindex))
                except:
                    if i == 2:
                        raise
            time.sleep(crawl_delay)

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
            time.sleep(crawl_delay)
    
    
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
            time.sleep(crawl_delay)


if __name__=='__main__':

    seed_url={ #'tyc':'http://tj.lianjia.com/ershoufang/taiyangcheng/'}
               'mj':'http://tj.lianjia.com/ershoufang/meijiang/'}
    
    date_now=time.strftime("%Y-%m-%d")
    '''
    if os.path.exists(date_now):
        print "Directory exist! Dumplicate house data"
        sys.exit()
    
    os.mkdir(date_now)
    '''
    os.chdir(date_now)

#    save_url_houses(seed_url)
    
    
    conn = MySQLdb.connect('127.0.0.1','root','111111','',3306)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    
    save_houses_info(seed_url,cur)
    conn.commit()    
    
