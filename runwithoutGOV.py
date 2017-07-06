import os, sys

fpath = sys.argv[1]

for line in open(fpath,'r'):
        line = line.strip()
        print line 
        print '='*50
        os.popen("scrapy crawl keywordSpider -L ERROR -a keywordList='"+ line  +"' -a se=baidunews -a pages=5 -a MONGODB_SERVER=10.10.165.175 -a MONGODB_PORT=23927 -a MONGODB_DB=BGY_YQ_NEWS_META")
