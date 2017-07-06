# -*- coding: utf-8 -*-
__author__ = 'liuhui'

import os, sys
from scrapy import cmdline
os.popen("scrapy crawl keywordSpider -L ERROR -a keywordList='碧桂园 火爆' -a se=baidunews -a pages=5 -a MONGODB_SERVER=app.raydata.cn -a MONGODB_PORT=23927 -a MONGODB_DB=lh_BGY_YQ_NEWS_META")