# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import  logging
import pymongo,os
from pybloom import BloomFilter
import hashlib
from scrapy.conf import settings
import time
from pymongo import DESCENDING
filetype = ['htm', 'asp', 'jsp', 'php', 'xml']

siteList = [
	'tieba',
	'weibo',
	'163.com',
        'qq.com',
        'sina.com.cn',
        'xinhuanet.com',
        'ifeng.com',
        'hexun.com',
        'jiemian.com',
        'thepaper.com',
        'yicai.com',
	'news.focus.cn',
        'home.news.cn',
        'people.com.cn',
        'eeo.com.cn',
        'fang.com',
        '21cn.com',
        'nbd.com.cn',
        'chinanews.com',
        'jjckb.cn',
        'chinadaily.com.cn',
        'house.china.com.cn',
        'yahoo.com',
        'theaustralian.com.au',
        'ap.org',
        'forbes.com',
        'abcnews.go.com',
        'zaobao.com',
        'apnews.com',
        'ausdaily.net.au',
        'wenweipo.com',
        'rtm.gov.my',
        'thestar.com.my',
        'hket.com',
        'takungpao.com',
        'nst.com.my',
        'cnn.com',
        'bbc.com',
        'enanyang.my',
        'guojiribao.com',
        'straitstimes.com',
        'utusan.com.my',
        'scmp.org.cn',
	'guojiribao.com',
	'scmp.org.cn',
	'nst.com.my',
	'apnews.com',
	'zaobao.com',
	'cnn.com',
	'theaustralian.com.au',
	'bbc.com',
	'rtm.gov.my',
	'enanyang.my',
	'abcnews.go.com',
	'wenweipo.com',
	'yahoo.com',
	'takungpao.com',
	'forbes.com',
	'hket.com',
	'ausdaily.net.au',
	'ap.org',
	'thestar.com.my',
	'utusan.com.my',
	'straitstimes.com',
]

class SespiderPipeline(object):

    def __init__(self):
        self.faillog = open('fail.txt','a')
        if os.path.exists(settings['MONGODB_DB']+'.urls'):
            #print("SEEN FILE EXISTS!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.bloomFilter = BloomFilter.fromfile(open(settings['MONGODB_DB']+'.urls','r'))
        else:
            self.bloomFilter = BloomFilter(1000000,0.001)
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collection.ensure_index('url', unique=True)
        self.collection.create_index([("crawltime", DESCENDING)])
        #self.file = open('urls.txt', 'a')
        #for line in open('urls.txt','r'):
        #        self.urls_seen.add(line.strip())
        #self.bloomFilter = rBloomFilter.rBloomFilter(100000, 0.01, 'bing')

    def process_item(self, item, spider):
        md5 = self.get_md5(item['url'])
        if self.url_seen(md5):
                raise DropItem("Duplicate item found: %s" % item['url'])
        else:
                self.url_add(md5)
        if self.myFilter(item):
                raise DropItem("myFilter Fail: %s" % item['url'])
        else:
                curtime = time.strftime("%Y%m%d")
                if curtime != self.collection.name:
                        self.collection = db[settings[curtime]]
                        self.collection.ensure_index('url', unique=True)
                        self.collection.create_index([("crawltime", DESCENDING)])
                self.collection.insert(dict(item))
        return item

    def open_spider(self, spider):
        spider.myPipeline = self

    # True: drop; False: write to DB
    def myFilter(self, item):
        u = item['url'].strip('/')
        flag = False
        if u.endswith(r'.cn') or u.endswith(r'.com') or u.endswith(r'.au') or u.endswith(r'.org') or u.endswith(r'.my'):
		raise DropItem("URL endsWITH  Fail: %s" % item['url'])
                return True
	if 'NEWS' in settings['MONGODB_DB']:
		for s in siteList:
			if s in u:
				flag = True
				break
		if flag == False:
			raise DropItem("NOT IN SiteList Fail: %s" % item['url'])
			return True
        if len(item['title'])<6 or item['pdate'] ==None or item['pdate'] =='' or item['showcontent'] == '':
                #print item['url'] + ':' + item['title'][:9] + '---' + str(item['pdate']) + '---' + str(len(item['content']))
                self.faillog.write(item['url']+'\n')
		raise DropItem("title/pdate/showcontent Fail: %s" % item['url'])
                return True
        return False
    #False:unSeen : True:Seen
    def get_md5(self, url):
        m2 = hashlib.md5()
        m2.update(url)
        return m2.hexdigest()
    
    def url_add(self, url_md5):
        self.bloomFilter.add(url_md5)

    def url_seen(self, url_md5):
        #return False
        return url_md5 in self.bloomFilter

    def open_spider(self, spider):
        spider.myPipeline = self

    def close_spider(self, spider):
        self.faillog.close()
        self.bloomFilter.tofile(open(settings['MONGODB_DB']+'.urls','wb'))
