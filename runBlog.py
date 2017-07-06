import os, sys
import commands
fpath = sys.argv[1]

sitelist = [
	'blogchina.com',
	'blog.tianya.cn',
	'blog.ifeng.com',
	'blog.qq.com',
	'blog.sohu.com',
	'blog.sina.com.cn',
	'blog.163.com',
	'qgblog.people.com.cn',
]

c = commands.getstatusoutput("ps aux | grep BGY_YQ_BLOG")
if 'scrapy' in c[1]:
        exit()

for line in open(fpath,'r'):
	line = line.strip()
	print line 
	print '='*50
	for site in sitelist:
		os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +"'   -a extkey='site:" + site +  "' -a se=baidu -a pages=3  -a MONGODB_SERVER='10.10.165.175' -a MONGODB_PORT=23927  -a MONGODB_DB=BGY_YQ_BLOG")
