#!/bin/bash

cd /root/spider/seCrawler
PATH=$PATH:/usr/local/bin
export PATH

sh /root/spider/seCrawler/runNews.sh
sh /root/spider/seCrawler/runTB.sh
sh /root/spider/seCrawler/runBlog.sh
#sh /root/spider/seCrawler/runWB.sh


