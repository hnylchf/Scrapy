#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import urllib
import hashlib
from ConfigUtil import *
from bs4 import BeautifulSoup
from UrlUtil import *
import json
import gzip
import StringIO
import logging
import logging.config
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import chardet


logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger()

import sys

#工具类
class Util():
    url = ''
    def __init__(self,url):
        self.url = url

    #get
    def getHtmlByGet(self):
        respone = urllib2.Request(self.url)
        respone.add_header("Accept", '	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        respone.add_header("Accept-Encoding", "gzip, deflate")
        respone.add_header("Accept-Language", "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3")
        respone.add_header("Connection", "keep-alive")
        respone.add_header("Host", self.getUrlHost())
        respone.add_header("User-Agent","Jwspider")
        respone.add_header('Upgrade-Insecure-Requests',1)

        h = urllib2.urlopen(respone)
        h = h.read()
        compressedstream = StringIO.StringIO(h)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data = gzipper.read()  # data就是解压后的数据
        return data

    #使用PhantomJs获取数据。如果需要返回页面中js执行后的结果用此方法
    def getHtmlByPhantomJs(self):
        driver = webdriver.PhantomJS(
        executable_path=getConfig('host','PhantomJS'))
        driver.get(self.url)
        data = driver.page_source  # 获取整个页面的内容
        driver.quit()#关闭释放
        return data


    def getSoup(self):
        html = self.getHtmlByGet()
        soup = BeautifulSoup(html)
        return soup

    def delSoupTag(self,soup):
        # 删除script标签
        [s.extract() for s in soup('script')]
        # 删除form标签
        [s.extract() for s in soup('form')]
        # 删除link标签
        [s.extract() for s in soup('link')]

    #查找页面中的a标签
    def getHtmlByTagA(self,soup,urlinfo = None):
        a_list = soup.find_all('a')
        result = []
        for a in a_list:
            try:
                if a.attrs.has_key('href'):
                    a_url = self.getUtf8Str(a['href'])
                    if not urlinfo is None:
                        if urlinfo.isCheckUrlHost(a_url):  # 查看是否是一个主域名下的域名
                            result.append(a_url)
                    else:
                        result.append(a_url)
            except Exception, e:
                logger.error(e)
        return result

    #查找页面中的img标签
    def getHtmlByTagImg(self, soup, urlinfo,f):
        img_list = soup.find_all('img')
        result = []
        for img in img_list:
            try:
                if img.attrs.has_key('src') or img.attrs.has_key('data-original'):
                    img_src = ''
                    if img.attrs.has_key('src'):
                        img_src = self.getUtf8Str(img['src'])
                    if img.attrs.has_key('data-original'):
                        img_src = self.getUtf8Str(img['data-original'])
                    result.append(img_src)
            except Exception, e:
                logger.error(e)
        return result

    def getUtf8Str(self,str):
        return str.encode('utf-8')

    def getMd5(self,str):
        m2 = hashlib.md5()
        m2.update(str)
        return m2.hexdigest()

    def converUrl(self,url):
        try:
            u = UrlUtil(url)
            if u.suffix == '':
                new_url = self.getMd5(u.host) + '_' + self.getMd5(u.path) + '.html'
            else:
                new_url = self.getMd5(u.host) + '_' + self.getMd5(u.path) + u.suffix
            return new_url
        except Exception, e:
            return ''

    def getFormat(self,str):
        str = str.lower()
        if str.endswith('.jpg') or str.endswith('.gif') or str.endswith('.png'):
            return 'img'
        elif str.endswith('.html') or str.endswith('.htm') or str.endswith('.shtml'):
            return 'htm'
        else:
            return ''

    def getInfo(self,soup):
        #获取网页标题
        title = self.getUtf8Str(soup.title.string)
        # 获取description
        meta = soup.meta
        try:
            description = self.getUtf8Str(soup.find(attrs={"name": "description"})['content'])
        except Exception,e:
            description = ''

        try:
            keywords = self.getUtf8Str(soup.find(attrs={"name": "keywords"})['content'])
        except Exception,e:
            keywords = ''
        return {'title':title,'keywords':keywords,'description':description}




    def getUrlHost(self):
        proto, rest = urllib.splittype(self.url)
        res, rest = urllib.splithost(rest)
        return res


    def deleteHtmlByTag(self,tag):
        return''

    #根据class删除
    def deleteHtmlByClassName(self,soup,class_name):
        for c in class_name:
            delete_list = soup.find(attrs={'class': c})
            delete_list.extract()

    #根据文本删除
    def deleteHtmlByHref(self,a_list,href):
        for a in href:
            a_list.remove(a)


    def getHtmlText(self,content,f):
        html = ''
        for element in content:
            try:
                if not element is None:
                    # 内部是否包含img
                    img = ''
                    try:
                        imgs = element.find_all('img')
                        if len(imgs) > 0:
                            for i in imgs:
                                img_src = self.converUrl(i['src'])
                                img = "[img]" + ".." + f.original_image + img_src + "[/img]"
                        else:
                            img = ''
                    except Exception, e:
                        img = ''
                    if not img == '':
                        html = html + img + "\n"
                    else:
                        html = html + element.text + "\n"

            except Exception, e:
                logging.error(e)
        return html


    def getHtmlImg(self,content):
        imgs = []
        for element in content:
            try:
                if not element is None:
                    # 内部是否包含img
                    try:
                        curr_imgs = element.find_all('img')
                        if len(curr_imgs) > 0:
                            for i in curr_imgs:
                                img_src = i['src']
                                imgs.append(img_src)
                    except Exception, e:
                        logger.error(e)
                else:
                    logger.error('未查询到文本内容')
            except Exception, e:
                logging.error(e)
        return imgs


