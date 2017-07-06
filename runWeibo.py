import os, sys

fpath = sys.argv[1]
while True:
        for line in open(fpath,'r'):
                line = line.strip()
                print line 
                print '='*50
                os.popen("scrapy crawl keywordSpider -L ERROR -a keywordList='"+ line  +"' -a se=baiduweibo -a pages=20 -a MONGODB_DB=BGY_YQ_WB")
