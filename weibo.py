#-*-coding:utf8-*-
# 2883238665
# Cookie: _T_WM=b8c24577cd09d1be5b8a6c5a9c1d47e6; SUB=_2A253xlb4DeRhGeRG41ET8ybKzTmIHXVVSXqwrDV6PUJbkdAKLVP7kW1NUhX2yo2Wja9LcUomsfWDCrNS4Qal2DUv; SUHB=0LcDSGUyTY7QcK; SCF=AlP_GBfjyswbnHRlNygKugu6mKJud4sZyiKJQQlCyinFoURjyl-867gwqyEwRxq3hmEIdLRNiNjc3PSBYaHI2N0.; SSOLoginState=1522673320; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword%26uicode%3D20000174%26fid%3Dhotword
import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
import shutil
import time
from lxml import etree

reload(sys) 
sys.setdefaultencoding('utf-8')
#if(len(sys.argv)>=2):
#        user_id = (int)(sys.argv[1])
#else:
#        user_id = (int)(raw_input(u"please_input_id: "))
user_id = 2173539123  # 大楠姐
cookie = {"Cookie": "#T_WM=b8c24577cd09d1be5b8a6c5a9c1d47e6; SUB=_2A253xlb4DeRhGeRG41ET8ybKzTmIHXVVSXqwrDV6PUJbkdAKLVP7kW1NUhX2yo2Wja9LcUomsfWDCrNS4Qal2DUv; SUHB=0LcDSGUyTY7QcK; SCF=AlP_GBfjyswbnHRlNygKugu6mKJud4sZyiKJQQlCyinFoURjyl-867gwqyEwRxq3hmEIdLRNiNjc3PSBYaHI2N0.; SSOLoginState=1522673320; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword%26uicode%3D20000174%26fid%3Dhotword"}
url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id
html = requests.get(url, cookies = cookie).content
print u'user_id和cookie读入成功'
selector = etree.HTML(html)
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

result = "" 
urllist_set = set()
word_count = 1

print u'ready'
print pageNum
sys.stdout.flush()

times = 5
one_step = pageNum/times
for step in range(times):
    if step < times - 1:
        i = step * one_step + 1
        j =(step + 1) * one_step + 1
    else:
        i = step * one_step + 1
        j =pageNum + 1
    for page in range(i, j):
        #获取lxml页面
        try:
            url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page)
            lxml = requests.get(url, cookies = cookie).content
            #文字爬取
            selector = etree.HTML(lxml)
            content = selector.xpath('//span[@class="ctt"]')
            for each in content:
                text = each.xpath('string(.)')
                if word_count >= 3:
                    text = "%d: "%(word_count - 2) +text+"\n"
                else :
                    text = text+"\n\n"
                result = result + text
                word_count += 1
            print page,'word ok'
        except:
            print page,'error'
        print page, 'sleep'
        sys.stdout.flush()
        # time.sleep(60)
    # print u'正在进行第', step + 1, u'次停顿，防止访问次数过多'
    # time.sleep(300)

try:
    fo = open(os.getcwd()+"/%d"%user_id, "wb")
    fo.write(result)
    word_path=os.getcwd()+'/%d'%user_id
    print u'文字微博爬取完毕'
except:
    print u'存放数据地址有误'
sys.stdout.flush()

print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count - 3,word_path)