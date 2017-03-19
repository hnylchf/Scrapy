#!/usr/bin/python
# -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod
import urllib
import urllib2
import cookielib
import StringIO
import gzip
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import chardet
import ConfigUtil


class BaseHttp(object):
    __metaclass__ = ABCMeta
    url = ''
    handlers = None
    cookie_path = None


    def __init__(self,url,handler,cookie_path = 'cookie.txt'):
        self.url = url
        self.handlers = handler
        self.cookie_path = cookie_path

    @abstractmethod
    def send_get(self,cookie):

        if cookie is None or len(cookie) == 0:
            cookie = cookielib.MozillaCookieJar(self.cookie_path)

        # 创建cookie处理器
        handler = urllib2.HTTPCookieProcessor(cookie)
        # 构建opener
        opener = urllib2.build_opener(handler)
        if not self.handlers is None:
            opener.addheaders = self.handlers
        res = opener.open(self.url)
        self.save_cookie(cookie)
        isGzip = res.headers.get('Content-Encoding')
        if isGzip:
            compresseddata = res.read()
            compressedstream = StringIO.StringIO(compresseddata)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
        else:
            data = res.read()
        return data

    @abstractmethod
    def send_post(self,post_data):
        cookie = cookielib.CookieJar()
        # 创建cookie处理器
        handler = urllib2.HTTPCookieProcessor(cookie)
        # 构建opener
        opener = urllib2.build_opener(handler)
        if not handler is None:
            opener.addheaders = self.handlers
        data = urllib.urlencode(post_data)  # 编码post数据为标准格式
        req = urllib2.Request(self.url, post_data)  # 做为data参数传给Request对象,此处也可以写成data=post_data
        response = opener.open(req)  #获取返回结果
        return response


    @abstractmethod
    def setHandlers(self,handlers):
        self.handlers = handlers


    @abstractmethod
    def get_cookie(self):
        cookie = cookielib.MozillaCookieJar()
        try:
            cookie.load(self.cookie_path, ignore_discard=True, ignore_expires=True)
        except IOError,e:
            pass
        return cookie

    @abstractmethod
    def getHtmlByPhantomJs(self):
        driver = webdriver.PhantomJS(
            executable_path=ConfigUtil.getConfig('host', 'PhantomJS'))
        driver.get(self.url)
        data = driver.page_source  # 获取整个页面的内容
        driver.quit()  # 关闭释放
        return data


    #保存cookie到文件
    @abstractmethod
    def save_cookie(self,cookie):
        # 声明一个MozillaCookieJar对象来保存cookie，之后写入文件
        # 保存cookie到文件
        # ignore_discard的意思是即使cookies将被丢弃也将它保存下来
        # ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
        cookie.save(self.cookie_path,ignore_discard=True, ignore_expires=True)



