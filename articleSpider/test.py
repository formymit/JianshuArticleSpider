#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: test.py 
@time: 2017/06/07 
"""
import re


with open('jianshu_urls.txt') as f:
    data =f.read()
    result = re.findall('http://www.jianshu.com/p/.*', data)
    # print(len(result))

    for each in result:
        with open('jianshu_article_urls.txt', 'a') as f2:
            f2.write(each + '\n')
            print(each)



    # str = '''a http://www.jianshu.com/p/293c5108e5cf
# http://www.jianshu.com/u/cbadd7e2f965
# http://www.jianshu.com/p/7c80e937faba
# http://www.jianshu.com/p/b64cb5f47b1e
# http://www.jianshu.com/p/d8d559a32770
# '''
#
# result = re.findall('http://www.jianshu.com/p/.*', str)
# print(result)
#
# for each in result:
#     print(each)



# content = 'Hello 123  '
# resutl2 = re.match('^Hello \d\d\d', content)
# print(resutl2)
# print(resutl2.group())
# print(resutl2)