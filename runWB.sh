#!/bin/bash
PATH=$PATH:/usr/local/bin
export PATH

nohup python runWB.py keywords_news.txt > WB.out  &

