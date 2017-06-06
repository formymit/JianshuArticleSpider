#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: writeMainURLsToDB.py 
@time: 2017/06/06 
"""
from mongodb_queue import MongoQueue

spider_queue = MongoQueue('jianBook', 'main_urls')

with open('main_urls.txt', 'r') as f:
    data = f.readline()
    while data:
        # print(data)
        url = data.split(',')[0]
        total_pages = data.split(',')[1]

        pages = int(int(total_pages)/10)
        # print(url)
        # print(total_pages)
        # print(pages)

#http://www.jianshu.com/c/dqfRwQ?order_by=added_at&page=2


        for i in range(1, pages):
            final_url = url + '?order_by=added_at&page=' + str(i)
            print(final_url)
            spider_queue.push(final_url)

            # with open('artcle_list_urls.txt', 'a') as f2:
            #     f2.write(url + '?order_by=added_at&page=' + str(i) + '\n')
        data = f.readline()





