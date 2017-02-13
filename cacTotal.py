#-*-coding:utf-8 -*-
#!/usr/bin/python
import MySQLdb
import time
from url import get_page
from lxml import etree

tj = 'http://tj.lianjia.com/ershoufang/'
bj = 'http://bj.lianjia.com/ershoufang/'

def get_total(url):
    page=get_page(url)
    tree=etree.HTML(page) 
    value = tree.xpath('.//h2[@class="total fl"]/span/text()')[0].strip()
    time.sleep(2)
    return value


def today_info(regions):
    every={}
    every['tj'] = get_total(tj);
    every['bj'] = get_total(bj);
     
    for region in regions:
        region_url = tj + region
        every[region]=get_total(region_url)

    return every

def save_total_info(cur):
    regions=['hexi','hedong','hongqiao','beichen','jinnan','nankai','heping','hebei','xiqing','tanggu','dongli']
    date_now=time.strftime("%Y-%m-%d")

    every = today_info(regions)
    keys=['date']
    values=[date_now]
    for region,value in every.items():
        keys.append(region)
        values.append(value)
    sql = "insert into area.amount(%s) values (%s)"%(','.join(keys),','.join(["'%s'"%i for i in values]))
    print sql
    cur.execute(r"%s"%sql.encode('utf-8'))
    

if __name__=='__main__':
    conn = MySQLdb.connect('127.0.0.1','root','111111','',3306)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    save_total_info_to_db(cur)
    conn.commit()    
