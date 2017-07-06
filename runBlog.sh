#!/bin/bash
PATH=$PATH:/usr/local/bin
export PATH

nohup python runBlog.py keywords_news.txt > blog.out &

