import os, sys
import commands
fpath = sys.argv[1]

sitelist = [
	'163.com',
	'qq.com',
	'sina.com.cn',
	'xinhuanet.com',
	'ifeng.com',
	'hexun.com',
	'jiemian.com',
	'thepaper.com',
	'yicai.com',
]

c = commands.getstatusoutput("ps aux | grep BGY_YQ_NEWS_META")
if 'scrapy' in c[1]:
	exit()

for line in open(fpath,'r'):
	line = line.strip()
	print line 
	print '='*50
	os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +  "' -a se=baidunews -a pages=5  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_NEWS_META")
	os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +  "' -a se=360news -a pages=5  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_NEWS_META")
	for site in sitelist:
		os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +"'   -a extkey='site:" + site +  "' -a se=baidunews -a pages=3  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_NEWS_META")
		os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +"'   -a extkey='site:" + site +  "' -a se=360news -a pages=3  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_NEWS_META")


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
                os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +"'   -a extkey='site:" + site +  "' -a se=360news -a pages=3  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_NEWS_META")


sitelist = [
        'yahoo.com'
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
]

c = commands.getstatusoutput("ps aux | grep BGY_YQ_NEWS_EN")
if 'scrapy' in c[1]:
        exit()
fpath = 'keywords_news_en.txt'
for line in open(fpath,'r'):
        line = line.strip()
        print line
        print '='*50
        if ' ' in line:
                line = line.replace(' ', '%26').strip()
        for site in sitelist:
                os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +"'   -a extkey='site:" + site +  "' -a se=bing -a pages=3  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_NEWS_EN")


