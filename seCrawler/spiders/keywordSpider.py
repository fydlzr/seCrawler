# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.spiders import Spider
from seCrawler.common.searResultPages import searResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors, SearchEngineResultDateSelectors
from seCrawler.xpaths import xpaths, newsXpaths, blogXpaths
from scrapy.selector import  Selector
import scrapy
from scrapy.http import Request
import re
import time
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup as bs
from newspaper import Article
import chardet
from seCrawler.parsers.newsparser import *
import dateparser
from scrapy.conf import settings
from urllib import unquote

noFix = set(['pdf','doc','docx','xls','xlsx','doc','docs'])
date1 = re.compile(r'(\d{4})年(0{0,1}\d{1}|1[0-2])月([12]\d{1}|3[01]|0{0,1}\d{1})日'.decode('utf-8'))
date2 = re.compile(r'(\d{4})-(0{0,1}\d{1}|1[0-2])-([12]\d{1}|3[01]|0{0,1}\d{1})')
dateurl = re.compile(r'(\d{4})(0\d{1}|1[0-2])([12]\d{1}|3[01]|0\d{1})')
retweet = re.compile(u'转发\((\d+)\)')
reply = re.compile(u'评论\((\d+)\)')
time1 = r'((0[1-9])|(1[0-9])|(2[0-3])|([1-9]))\:([0-5][0-9])((\:([0-5][0-9]))|)'

class keywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = []
    start_urls = []
    keywordList = None
    searchEngine = None
    selector = None
    dateSelector = None
    govSelector = None
    myPipeline = None
    def __init__(self, keywordList,extkey=None, se = 'baidu', pages = 2, MONGODB_SERVER='127.0.0.1', MONGODB_PORT=27017, MONGODB_DB='BGY_ZC_META', *args, **kwargs):
        super(keywordSpider, self).__init__(*args, **kwargs)
        self.keywordList = keywordList.lower()
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors[self.searchEngine]
        self.dateSelector = SearchEngineResultDateSelectors[self.searchEngine]
	
	if 'WX' in MONGODB_DB or 'WB' in MONGODB_DB:
		settings['DOWNLOAD_DELAY'] = 5

        settings['MONGODB_SERVER'] =MONGODB_SERVER
        settings['MONGODB_PORT'] = int(MONGODB_PORT)
        settings['MONGODB_DB'] = MONGODB_DB
        keys = keywordList.split('，')
        for key in keys:
                key = key.strip()
                if key == '': continue
		key = key.strip()
		if extkey!=None:
	                key = key+ ' '+extkey.strip()
                pageUrls = searResultPages(key, se, int(pages))
                for url in pageUrls:
                    self.start_urls.append(url)
    
    def parse(self, response):
        #url = 'https://tieba.baidu.com/p/5109409644?pid=106971077843&cid=0'
        #yield scrapy.Request(url, callback = lambda response, argv = {'title':' ', 'date':' ', 'keyword':' '}: self.parse_detail(response, argv))
        #return

        if 'baidu' in response.url:
                if 'news' in response.url:
                        wd = response.url.find('word=')
                        keyword = response.url[wd+5 : response.url.find('&',wd)]
                elif 'tieba' in response.url:
                        wd = response.url.find('qw=')
                        keyword = response.url[wd+3 : response.url.find('&',wd)]
                else:
                        wd = response.url.find('wd=')
                        keyword = response.url[wd+3: response.url.find('&',wd)]
        else:
                q = response.url.find('q=')
                keyword = response.url[q+2: response.url.find('&',q)]
        keyword = unquote(keyword)

        if 'baiduwb' in response.url:
                items = self.parseWeibo(response,keyword)
                for it in items:
                        yield it
        else:         
                for urlnode in Selector(response).xpath(self.selector):
                        url = urlnode.xpath('@href').extract()[0]
                        if not url.startswith('http'):  # 处理相对URL
                                url = response.urljoin(url).strip('/')
                        if self.myPipeline.url_seen(url):
                                continue
                        title = urlnode.xpath('string(.)').extract()
                        if len(title)==0:
                                title = None
                        else:
                                title = ''.join(title)
                        date = urlnode.xpath(self.dateSelector).extract()
                        if len(date)==0:
                                date = None
                        else:
                                date = self.getDate(date[0])
                        #print url, title,date
                        yield scrapy.Request(url, callback = lambda response, argv = {'title':title, 'date':date, 'keyword':keyword}: self.parse_detail(response, argv))
    def parse_detail(self,response,argv):
        if self.myPipeline.url_seen(response.url):
                return
        title = argv['title']
        date = argv['date']
        body = response.body
        if 'GB' in chardet.detect(response.body)["encoding"]:
                try:
                        body = response.body.decode('gb18030').encode('utf-8')
                except:
                        self.myPipeline.faillog.write('编码ERROR: ' + response.url)
        ext = tldextract.extract(response.url)
        normUrl = '.'.join(e for e in ext if e)
        if normUrl not in xpaths:
                normUrl = '.'.join(e for e in ext[1:] if e)
        govselector = self.getSelector(response.url)
        item = {'url':response.url, 'title':'', 'pdate':'', 'content':'', 'showcontent':'',  'parser':{}}
        if govselector != None:
                sel = Selector(text=body)
                for key in govselector:
                        if type(govselector[key])!=list:
                                item[key] = govselector[key]
                                continue
                        if item[key]!=None and len(item[key])>5  and '…' not in item[key] and '...' not in item[key]:
                                continue
			res = None
                        for Sel in govselector[key]:
                                res = self.getNodeText(sel.xpath(Sel))
                                if len(res.strip())>0:
                                        break
                                else:
                                        if 'tbody' in Sel:
                                                Sel = Sel.replace('/tbody','')
                                                res = self.getNodeText(sel.xpath(Sel))
                                                if len(res.strip())>0:
                                                        break
                        item[key] = res
                        #print key + res
                        if len(item[key])>0:
                                item['parser'][key] = 'xpath'
                item['showcontent'] = self.cleanBR_RN(item['showcontent'], '<br/>')
                item['content'] = ('\n'.join(t for t in item['showcontent'].split('\n') if 'img' not in t and 'http' not in t)).encode('utf-8')
		if title != None and len(item['title'])==0:
                        item['title'] = title
                        item['parser']['title']= 'SE'
		item['pdate'] = self.getDate(item['pdate'])
                if date != None and len(item['pdate'])<6:
                        item['pdate'] = date
                        item['parser']['pdate'] = 'SE'
                if item['pdate']==None or len(item['pdate'])<6:
                        item['pdate'] = self.getDateFromURL(response.url)
		if item['pdate']==None or len(item['pdate'])<6:
                        item['pdate'] = self.getDate(item['showcontent'])
	#print item['title'], item['pdate'], len(item['showcontent'])
        if item['pdate']==None or len(item['pdate'])<6 or item['title']=='' or item['showcontent']=='':
                it = newsparser().parse({'html':body, 'url':response.url})
                for i in it['value']:
                        if i not in item or (i in item and (item[i]==None or len(item[i])<2)):
                                item[i] = it['value'][i]
                for i in it['parser']:
                        if i not in item['parser']:
                                item['parser'][i] = it['parser'][i]
        if 'lang' not in item:
                item['lang'] = 'zh'
        item['src'] = self.searchEngine
        item['region'] = ''
        item['edc'] = {}
        item['language'] = 'chineseUTF8'
        item['tags'] = ''
        item['database'] = ''
        item['crawlername'] = self.name
        item['image_url'] = ''
        item['image_data'] = ''
        item['crawltime'] = int(time.time())
        item['type'] = argv['keyword']
        try:
                item['pdate'] = int(item['pdate'])
        except:
                item['pdate'] = None
        yield item
    def getNodeText(self, sel):
        #print sel
        if type(sel)==Selector:
                uq = sel.extract_unquoted()
                if '<style' not in uq and '<script' not in uq:
			if '/@' in str(sel):
				return sel.extract().strip()
                        else:
                                return '\n'.join(sel.xpath('string(.)').extract()).strip()
                children = sel.xpath('./*')
                if len(children)==0:
                        if '<style' in uq or '<script' in uq:
                                return ''
                subtext = []
                for child in children:
                        t = self.getNodeText(child).strip()
                        if t!='':
                                subtext.append(t)
                return '\n'.join(subtext).strip()
        else:
                text = []
                for se in sel:
                        text.append(self.getNodeText(se))
                return '\n'.join(text).strip()
    def getDate(self, line):
        if line==None or line=='':
                return None
        if type(line)==int:
                return line
	try:
		dateint = int(line)
		return line
	except:
		pass
	try:
		t = line
                if ':' in line:
                        t = line.split(':')[1].strip()
                if len(t)>6:
                        t = dateparser.parse(t)
                        dateint = int(time.mktime(t.timetuple()))
                        return str(dateint)
        except:
                pass
	line = line.replace('/','-')
        line = line.replace('_','-')
        if u'前' in line:
                t = dateparser.parse(line)
		if t==None:
			return None
                dateint = int(time.mktime(t.timetuple()))
                return str(dateint)
        date = date1.findall(line)
        if date==None or len(date)==0:
                date = date2.findall(line)
        if date==None or len(date)==0:
                return None
        else:
		t = '-'.join(date[0])
		t1 = re.search(time1, line)
                if t1 != None:
                        t1 = t1.group()
                        t = t + ' ' + t1
		t = dateparser.parse(t)
                if t == None:
                        return None
                dateint = int(time.mktime(t.timetuple()))
                return str(dateint)
    def getDateFromURL(self, line):
	line = line.replace('/','-')
	line = line.replace('_','-')
        date = dateurl.findall(line)
        if date==None or len(date)==0:
                return None
        else:
                t = dateparser.parse('-'.join(date[0]))
                if t == None:
                        return None
                dateint = int(time.mktime(t.timetuple()))
                return  str(dateint)
    def cleanBR_RN(self, content, char):
        lines = re.split(char + '\t|\n|\r' if char=='' else '|\t|\n|\r',content)
        res = ''
        if char == '':
                char = '\n'
        for line in lines:
                line = line.strip()
                if len(line)>1:
                        res += line + char
        return res
    def getSelector(self, start_url):
	selector = None
        ext = tldextract.extract(start_url)
        normUrl = '.'.join(e for e in ext if e)
        if normUrl in xpaths:
                selector = xpaths[normUrl]
        elif 'www.'+'.'.join(e for e in ext[1:] if e) in xpaths:
                selector = xpaths['www.'+'.'.join(e for e in ext[1:] if e)]
        else:
		for xpath in blogXpaths:
			if xpath in start_url:
				return blogXpaths[xpath]
		for xpath in newsXpaths:
			if xpath in start_url:
				return newsXpaths[xpath]
        return selector
    def parseWeibo(self, response, keyword):
        its = []
        for weibo in Selector(response).xpath('//div[@class="weibo_detail"]'):
                url = weibo.xpath('.//a[@class="weibo_all"]/@href').extract()[0].strip()
                #print url
                if self.myPipeline.url_seen(url):
                        continue
                item = {'url':url}
                author = weibo.xpath("./p/a/text()").extract()
                if author != None and len(author)>0:
                        item['author'] = author[0]
                content = self.getNodeText(weibo.xpath('./p'))
                pz = self.getNodeText(weibo.xpath('.//div[@class="weibo_pz"]'))
                rt = retweet.findall(pz)
                if len(rt)>0:
                        item['retweet']=int(rt[0])
                rp = reply.findall(pz)
                if len(rp)>0:
                        item['reply'] = int(rp[0])
                tim = weibo.xpath('.//div[@class="m"]/a[1]/text()').extract()
                if len(tim)>0:
                        tim = tim[0].replace('\t','').replace('\n','')
                        item['pdate'] = int(self.getDate(tim))
                else:
                        item['pdate'] == None
                item['showcontent'] = self.cleanBR_RN(content, '').strip()
                item['content'] = ('\t'.join(t for t in item['showcontent'].split('\t') if 'img' not in t)).encode('utf-8')                
                if '【' in item['content'] and '】' in item['content']:
                        item['title'] = item['content'][item['content'].find('【')+3:item['content'].find('】')]
                else:
                        item['title'] = item['content']
                if 'lang' not in item:
                        item['lang'] = 'zh'
                item['src'] = self.searchEngine
                item['region'] = ''
                item['edc'] = {}
                item['language'] = 'chineseUTF8'
                item['tags'] = ''
                item['database'] = ''
                item['crawlername'] = self.name
                item['image_url'] = ''
                item['image_data'] = ''
                item['crawltime'] = int(time.time())
                item['type'] = keyword
                its.append( item)
        return its
