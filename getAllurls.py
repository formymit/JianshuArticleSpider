#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: getAllurls.py 
@time: 2017/06/06 
"""
import requests
from lxml import etree

url = 'http://www.jianshu.com/recommendations/collections?utm_medium=index-collections&utm_source=desktop'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

def geturls(url):
    try:
        resposne = requests.get(url, headers=headers)

        selector = etree.HTML(resposne.text)

        all_names = selector.xpath('//a[@class="name"]')
        all_hrefs = selector.xpath('//a[@class="name"]/@href')
        total_num = selector.xpath('//div[@class="count"]//a')

        for i in range(len(all_names)):
            name = all_names[i].xpath('string(.)')
            href = all_hrefs[i]
            href = 'http://www.jianshu.com' + href

            total_pages = total_num[i].xpath('string(.)')
            with open('main_urls.txt', 'a') as f:
                f.write(href + ','+ total_pages[:-3]+'\n')
            print(name + ', ' + href + ', ' + total_pages)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    for i in range(1,4):
        url = 'http://www.jianshu.com/recommendations/collections?page=' + str(i)
        geturls(url)
