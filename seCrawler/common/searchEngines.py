SearchEngines = {
    'baidu': 'http://www.baidu.com/s?wd={0}&pn={1}&ie=utf-8',
    'baidunews': 'http://news.baidu.com/ns?word={0}&pn={1}&cl=2&ct=0&tn=news&rn=20&ie=utf-8&bt=0&et=0',
    'baiduweibo'  : 'http://www.baidu.com/s?rtt=2&wd={0}&pn={1}&tn=baiduwb&ie=utf-8',
    'tieba':  'http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw={0}&rn=10&un=&only_thread=1&sm=1&sd=&ed=&pn={1}&ie=utf-8',

    'sogou' : 'https://www.sogou.com/web?query={0}&page={1}&ie=utf8',
    'sogouweixin' : 'http://weixin.sogou.com/weixin?query={0}&type=2&page={1}',

    '360': 'https://www.so.com/s?q={0}&pn={1}',
    '360news': 'http://news.so.com/ns?q={0}&pn={1}&tn=news&rank=pdate&j=0&src=page',

    'google': 'https://www.google.com/search?q={0}&start={1}',
    'bing': 'http://www.bing.com/search?q={0}&first={1}',
}


SearchEngineResultSelectors= {
    '360':'//h3/a',
    'bing':'//h2/a',
    'baidu':'//h3/a',
    'baidunews':'//h3/a',
    'tieba' : '//span[@class="p_title"]/a',
    '360news':'//h3/a',
    'baiduweibo':'//div[@class="weibo_detail"]',
    'sogou': '//h3/a',
    'sogouweixin':'//h3/a',
}

SearchEngineResultDateSelectors= {
    'baidu': "../../div[@class='c-abstract']/span/text()",
    '360': "../../div/div/span/text()",
    '360news': '../..//span[@class="posttime"]/@data-pdate',
    'baidunews' : '../../div/p',
    'tieba' : '../../font',
    'baiduweibo': '/div[2]/div[2]/a',
    'bing':'../../../div[2]/div',
    'sogou' : '../../div[2]/cite',
    'sogouweixin':'../../div/@t',
}
