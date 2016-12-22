#-*-coding:utf-8 -*-
import os
import re

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
        pattern = re.compile(r'info">(.*)</a>')
        keys = ['communityName','info','\n']
        self.communityName = pattern.search(self.getslice(keys)).group(1)

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
        pattern = re.compile(r'count">([0-9]*)</div>.*\n.*<span>([0-9]*)')
        keys = ['class="record"',r'近7天带看次数','count','</span>']
        match = pattern.search(self.getslice(keys))
        self.visit7days = match.group(1)
        self.visittotal = match.group(2)

