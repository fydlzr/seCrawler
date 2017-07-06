import os, sys

fpath = sys.argv[1]
while True:
        for line in open(fpath,'r'):
                line = line.strip() + ' inurl:gov'
                print line 
                print '='*50
                os.popen("scrapy crawl keywordSpider -L ERROR -a keywordList='"+ line  +"' -a se=baidu -a pages=20 -a MONGODB_DB=BGY_ZC_META")
