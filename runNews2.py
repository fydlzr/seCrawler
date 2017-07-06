import os, sys
import commands
fpath = sys.argv[1]

sitelist = [
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
]

c = commands.getstatusoutput("ps aux | grep BGY_YQ_NEWS_META")
if 'scrapy' in c[1]:
        exit()


for line in open(fpath,'r'):
	line = line.strip()
	print line 
	print '='*50
	for site in sitelist:
		os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +"'   -a extkey='site:" + site +  "' -a se=baidunews -a pages=3  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_NEWS_META")
		os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +"'   -a extkey='site:" + site +  "' -a se=359news -a pages=3  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_NEWS_META")
