#-*-coding:utf-8 -*-
import os
import re
import urllib2
import json

class page_parser:
    def __init__(self,page):
        self.page   = page
        self.offset = 0

        self.parsetotal()
        self.parseprice()
        self.parsetype()
        self.parsearea()
        self.parsecommunityName()
        self.parseregions()
        self.parsehouseid()
        self.parsehousetype()
        self.parsevisit()

    def getslice(self,keys):
        lcur = 0
        for key in keys[0:-1]:
            lcur = self.page.find(key,self.offset)
            self.offset = lcur
        rcur = self.page.find(keys[-1],self.offset)
        return self.page[lcur:rcur]

    def parsetotal(self):
        pattern = re.compile(r'"total">([0-9]*).*')
        keys = ['overview','price','unit']
        self.total = pattern.search(self.getslice(keys)).group(1)

    def parseprice(self):
        pattern = re.compile(r'unitPriceValue">([0-9]*)')
        keys = ['unitPrice','unitPriceValue','\n']
        self.price = pattern.search(self.getslice(keys)).group(1)

    def parsetype(self):
        pattern = re.compile(r'mainInfo">(.*)</div>\n.*"subInfo">(.*)</div>\n')
        keys = ['houseInfo','room','mainInfo','type']
        match = pattern.search(self.getslice(keys))
        self.type     = match.group(1)
        self.sub_info = match.group(2)

    def parsearea(self):
        pattern = re.compile(r'mainInfo">(.*)</div>')
        keys = ['area','mainInfo','\n']
        self.area = pattern.search(self.getslice(keys)).group(1)

    def parsecommunityName(self):
        pattern = re.compile(r'xiaoqu/([0-9]*).*info">(.*)</a>')
        keys = ['communityName','href','\n']
        match = pattern.search(self.getslice(keys))
        self.rid = match.group(1)
        self.communityName = match.group(2)
        print 'rid %s,%s'%(self.rid,self.communityName)

    def parseregions(self):
        pattern = re.compile(r'target="_blank">(.*)</a>.*target="_blank">(.*)</a>')
        keys = ['areaName','info','\n']
        match = pattern.search(self.getslice(keys))
        self.region = match.group(1) 
        self.sub_region = match.group(2) 

    def parsehouseid(self):
        pattern = re.compile(r'info">([0-9]*)')
        keys = ['houseRecord','info','\n']
        self.houseid = pattern.search(self.getslice(keys)).group(1)

    def parsehousetype(self):
        pattern = re.compile(r'</span>(.*)</li>')
        keys = ['transaction',r'房屋用途','\n']
        self.housetype = pattern.search(self.getslice(keys)).group(1)

    def parsevisit(self):
        headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        url='http://tj.lianjia.com/ershoufang/housestat?hid=%s&rid=%s'%(self.houseid,self.rid)
        page = None
        jobj = None
        for i in range(3):
            try:
                page = urllib2.urlopen(urllib2.Request(url,headers=headers))
                jstr = page.read()
                jobj = json.loads(jstr)
                break
            except:
                if i == 2:
                    raise
                print "url read exception : %s"%url

        self.recentvisit = jobj['data']['seeRecord']['thisWeek']
        self.totalvisit = jobj['data']['seeRecord']['totalCnt']


"""
    def parsevisit(self):
        pattern = re.compile(r'count">([0-9]*)</div>.*\n.*<span>([0-9]*)')
        keys = ['class="record"',r'近7天带看次数','count','</span>']
        match = pattern.search(self.getslice(keys))
        self.recentvisit = match.group(1)
        self.totalvisit = match.group(2)
"""

