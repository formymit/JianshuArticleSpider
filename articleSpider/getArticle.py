#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: getArticle.py 
@time: 2017/06/07 
"""
import requests
from lxml import etree
import json
from mongodb_queue import MongoQueue
import multiprocessing
import time

spider_queue = MongoQueue('JianBook02', 'article_urls')

url = 'http://www.jianshu.com/p/d069fc24235a'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

def getInfo():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('没有数据啦~')
            break
        else:
            result = getData(url)
            if len(result) == 0:
                spider_queue.reset(url)
            else:
                spider_queue.complete(url)


def getData(url):
    try:

        response = requests.get(url, headers=headers)

        selector = etree.HTML(response.text)

        title = selector.xpath('//h1[@class="title"]/text()')[0]
        author = selector.xpath('//span[@class="name"]//a/text()')[0]
        time = selector.xpath('//span[@class="publish-time"]/text()')[0]
        # wordsNum = selector.xpath('//span[@class="wordage"]/text()')[0]

        other_info = selector.xpath('//script[@type="application/json"]/text()')[0]
        # print(other_info)
        myjson = json.loads(other_info)
        note = myjson['note']
        likes_count = note['likes_count']
        views_count = note['views_count']
        wordsNum = note['public_wordage']
        comments_count = note['comments_count']

        author_info = note['author']
        followers_count = author_info['followers_count']
        total_likes_count = author_info['total_likes_count']

        contents = selector.xpath('//div[@class="show-content"]//p//text()')  # //text() 获得所有文本
        text = ''
        for each in contents:
            text = text + each

        # print(title + ', ' + author + ', ' + time +  ', ' + wordsNum + ', ' + str(views_count) + ', ' +  str(comments_count) + ', ' + str(likes_count) + ', followers_count: ' + str(followers_count) + ', total_likes_count: ' + str(total_likes_count))
        # print(contents)
        # print(text)

        result = {
            'articleTitle': title,
            'url': url,
            'author': author,
            'publish_time': time,
            'wordNum': wordsNum,
            'view_count': views_count,
            'comments_count': comments_count,
            'likes_count': likes_count,
            'content': text,
            'follower_count': followers_count,
            'total_likes_count': total_likes_count
        }

        # result = '{' + '"articleTitle": ' + '"' + title + '", ' + '"url": ' + '"' + url + '", ' + '"author": ' + '"' + author + '", ' + '"publish-time": ' + '"' + time + '", ' + '"wordsNum": ' + '"' + wordsNum + '"' + ', ' + '"views_count": ' + '"' + str(
        #     views_count) + '"' + ', ' + '"comments_count": ' + '"' + str(
        #     comments_count) + '"' + ', ' + '"likes_count": ' + '"' + str(
        #     likes_count) + '"' + ', ' + '"followers_count": ' + '"' + str(
        #     followers_count) + '"' + ', ' + '"total_likes_count": ' + '"' + str(total_likes_count) + '"' + '}'
        print(result)

        if len(title) != 0:
            with open('articles_info.txt', 'a') as f3:
                f3.write(str(result) + '\n')


    except Exception as e:
        print(e)
    return title

def process_crawler():
    process = []
    for i in range(30):
        p = multiprocessing.Process(target=getInfo)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':

    url = 'http://www.jianshu.com/p/939326fa15f4'
    getData(url)


    # process_crawler()


    # with open('jianshu_article_urls.txt') as f:
    #     url = f.readline()
    #     while url:
    #         print(url)
    #         getData(url[:-1])
    #         time.sleep(1)
    #         url = f.readline()


