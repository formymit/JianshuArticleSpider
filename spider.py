#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: spider.py 
@time: 2017/06/06 
"""
import requests
from lxml import etree
import re
import time
from mongodb_queue import MongoQueue
import multiprocessing

url = 'http://www.jianshu.com/c/dqfRwQ'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('jianBook', 'main_urls')


def infoCrawler():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('队列没有数据啦')
            break
        else:
            result = getData(url[:-1]) #不能有回车啊~~ 昨天也是这个问题
            if len(result) == 0:  #很聪明的办法 用title代替 sumContent
                #区分没有抓到数据以及本身没有数据 有重置 死循环？ 谨慎重置 不然就是死循环 永远抓不完 如果有isotime 则complete
                spider_queue.reset(url)
            else:
                spider_queue.complete(url)

def getData(url):
    try:
        response = requests.get(url, headers = headers)

        # print(response.text)
        selector = etree.HTML(response.text)

        all_names = selector.xpath('//div[@class="name"]//a')
        all_times = selector.xpath('//span[@class="time"]/@data-shared-at')
        all_titles = selector.xpath('//a[@class="title"]')
        all_hrefs = selector.xpath('//a[@class="title"]/@href')
        all_readsAndcomments = selector.xpath('//div[@class="meta"]//a') #0 ,1
        all_likes = selector.xpath('//ul[@class="note-list"]//li//div[@class="meta"]') # 0 [1]
        # print(len(all_likes)) #如何区分？

        likes = []

        str = response.text
        start = str.find('<i class="iconfont ic-list-like"></i>')
        end = str.find('</span>', start)
        like = str[start + len('<i class="iconfont ic-list-like"></i>'): end]
        like = ' '.join(like.split())
        # print(like)

        likes.append(like)

        for j in range(9):
            start = str.find('<i class="iconfont ic-list-like"></i>', end)
            end = str.find('</span>', start)
            like = str[start + len('<i class="iconfont ic-list-like"></i>'): end]
            like = ' '.join(like.split())
            # print(like)
            likes.append(like)
        print(likes)

        for i in range(len(all_titles)):
            name = all_names[i].xpath('string(.)')
            time = all_times[i]
            title = all_titles[i].xpath('string(.)')
            title = ' '.join(title.split())
            href = all_hrefs[i]
            href = 'http://www.jianshu.com' + href
            read = all_readsAndcomments[2*i].xpath('string(.)')
            read = ' '.join(read.split())
            comment = all_readsAndcomments[2*i - 1].xpath('string(.)')
            comment = ' '.join(comment.split())

            # print('article title: '+ title + ', author: ' + name + ', released time: ' + time)
            # print(href
            # print(read + ', ' + comment+ ', ' + likes[i])

            result = '{' + '"articleTitle": ' + '"' + title + '", ' + '"url": ' + '"' + href + '", ' + '"author": ' + '"' + name + '", ' + '"releasedTime": ' + '"' + time + '", ' + '"read": '  + read + ', ' +'"comment": ' + comment + ', ' +'"like": ' + likes[i] +  '}'

            with open('article_infos.txt', 'a') as file:
                file.write(result + '\n')
            print(result)
    except Exception as e:
        print(e)

    return title

def process_crawler():
    process = []
    for i in range(3):
        p = multiprocessing.Process(target=infoCrawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()


if __name__ == '__main__':

    process_crawler()
    # for i in range(1,100):
    #     url = 'http://www.jianshu.com/c/dqfRwQ?order_by=added_at&page=' + str(i)
    #     getData(url)
    #     time.sleep(1)






