#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：backend 
@File    ：ArticleFilter.py
@Author  ：kif<kif101001000@163.com>
@Date    ：2022/10/30 16:30 
'''

import os
import chardet

# 获取文件目录和绝对路径
curr_dir = os.path.dirname(os.path.abspath(__file__))
# os.path.join()拼接路径
sensitive_word_stock_path = os.path.join(curr_dir, 'sensitive_word_stock.txt')


# 获取存放敏感字库的路径
# print(sensitive_word_stock_path)


class ArticleFilter(object):
    def __init__(self):
        self.flag = False

    # 实现文章敏感词过滤
    def filter_replace(self, string):
        # string = string.decode("gbk")
        #   存放敏感词的列表
        filtered_words = []
        #   打开敏感词库读取敏感字
        with open(sensitive_word_stock_path, encoding='utf-8') as filtered_words_txt:
            lines = filtered_words_txt.readlines()
            for line in lines:
                #  strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
                filtered_words.append(line.strip())
        # 输出过滤好之后的文章
        reStr = self.replace_words(filtered_words, string)
        print("!!!!!过滤文字:" +string+'--->'+ reStr)
        return {
            'Forbidden': self.flag,
            "str": reStr
        }

    # 实现敏感词的替换,替换为*
    def replace_words(self, filtered_words, string):
        #   保留新字符串
        new_string = string
        #   从列表中取出敏感词
        for words in filtered_words:
            # 判断敏感词是否在文章中
            if words in string:
                # 如果在则用*替换(几个字替换几个*)
                print(words)
                new_string = string.replace(words, "*" * len(words))
                self.flag = True
        # 当替换好的文章(字符串)与被替换的文章(字符串)相同时,结束递归,返回替换好的文章(字符串)
        if new_string == string:
            #   返回替换好的文章(字符串)
            return new_string
        # 如果不相同则继续替换(递归函数自己调用自己)
        else:
            #   递归函数自己调用自己
            return self.replace_words(filtered_words, new_string)


def filter_replace(string):
    run = ArticleFilter()
    return run.filter_replace(string)
filter_replace('0ni9o1s3feu60.cn')