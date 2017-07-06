#!/bin/bash
PATH=$PATH:/usr/local/bin
export PATH

nohup python runWX.py keywords_news.txt > WX.out  &
