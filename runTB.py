import os, sys
import commands
c = commands.getstatusoutput("ps aux | grep BGY_YQ_TB")
if 'scrapy' in c[1]:
        exit()



fpath = sys.argv[1]
for line in open(fpath,'r'):
        line = line.strip()
        print line 
        print '='*50
        os.system("scrapy crawl keywordSpider -L WARNING -a keywordList='"+ line  +"' -a MONGODB_SERVER=10.10.165.175 -a MONGODB_PORT=23927 -a se=tieba -a pages=6 -a MONGODB_DB=BGY_YQ_TB")
