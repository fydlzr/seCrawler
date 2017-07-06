#!/bin/bash
cd /root/spider/seCrawler
PATH=$PATH:/usr/local/bin
export PATH

nohup python runNews.py keywords_news.txt > news1.out &
#nohup python runNews2.py keywords_news.txt > news2.out &
#nohup python runENnews.py keywords_news_en.txt > newsEN.out &
