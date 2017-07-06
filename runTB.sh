#!/bin/bash
PATH=$PATH:/usr/local/bin
export PATH

nohup python runTB.py keywords_news.txt > TB.out  &

