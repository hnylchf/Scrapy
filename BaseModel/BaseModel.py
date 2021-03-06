#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

sys.path.append("..")
import sys
from mq.client import *
import logging.config
from abc import ABCMeta, abstractmethod
import urllib2
from bs4 import BeautifulSoup
import ConfigUtil
from UrlUtil import *
from FileUtil import *
from BaseUtil import *
import xml.dom.minidom

class BaseModel(object):
    __metaclass__ = ABCMeta
    mq = None
    url = None
    urlInfo = None
    f = None
    logger = None
    main_md5 = None
    minor_md5 = None

    def __init__(self, url):
        self.url = url
        logging.config.fileConfig("../config/logging.conf")
        self.logger = logging.getLogger()
        self.mq = lg_mq_client(ConfigUtil.getConfig('host', 'mq_prot'))  # 获取mq链接
        self.urlInfo = UrlUtil(url)
        u = UrlUtil(url)
        self.f = FileUtil(ConfigUtil.getConfig('host', 'host_path'))
        self.f.initPath()  # 初始化路径
        self.main_md5 = getMd5(self.urlInfo.host)  # 主ID
        self.main_md5 = getMd5(self.urlInfo.path)  # 副ID

    #push到mq中内容不可重复
    def pushMq(self,msg):
        self.mq.push(msg)

    #push到mq中 内容可重复
    def pushMq2(self, msg):
        self.mq.push2(msg)

    #获取内容
    def getContent(self,soup):
        pass

    # 获取网页信息
    @abstractmethod
    def getInfo(self,soup):
        # 获取网页标题
        try:
            title = self.getUtf8Str(soup.title.string)
        except Exception, e:
            title = ''
        # 获取description
        meta = soup.meta
        try:
            description = self.getUtf8Str(soup.find(attrs={"name": "description"})['content'])
        except Exception, e:
            description = ''
        try:
            keywords = self.getUtf8Str(soup.find(attrs={"name": "keywords"})['content'])
        except Exception, e:
            keywords = ''
        return {'title': title, 'keywords': keywords, 'description': description}

    #链接
    @abstractmethod
    def link_parse(self,soup):
        a_list = soup.find_all('a')
        result = []
        for a in a_list:
            try:
                if a.attrs.has_key('href'):
                    a_url = self.getUtf8Str(a['href'])
                    join_url = self.urlInfo.urlJoin(self.url,a_url)
                    if self.urlInfo.isCheckUrlHost(join_url):  # 查看是否是一个主域名下的域名
                        result.append(join_url)
            except Exception, e:
                self.logger.error(e)
        return result

    #图片
    @abstractmethod
    def img_parse(self,soup):
        img_list = soup.find_all('img')
        result = []
        for img in img_list:
            try:
                if img.attrs.has_key('src'):
                    img_src = ''
                    if img.attrs.has_key('src'):
                        img_src = self.getUtf8Str(img['src'])
                    result.append(img_src)
            except Exception, e:
                logger.error(e)
        return result

    #视频
    @abstractmethod
    def video_parse(self,soup):pass

    @abstractmethod
    def text_parse(self,soup):
        result = []
        text = ''
        for element in soup:
            try:
                if not element is None:
                    # 内部是否包含img
                    try:
                        imgs = element.find_all('img')
                        if len(imgs) > 0:
                            result.append(['content', text])
                            text = ''
                            for i in imgs:
                                img_src = converUrl(i['src'])
                                result.append(['img', img_src])
                    except Exception, e:
                        pass
                    text = text + element.text + '\n'

            except Exception, e:
                logging.error(e)
        if not text is None and not text == '':
            article_result = ['content', text]
        return result

    #获取soup
    @abstractmethod
    def getSoup(self,html):
        soup = BeautifulSoup(html)
        return soup

    #删除soup中的标签注：tags是数组
    @abstractmethod
    def delSoupTag(self,soup,tags):
        for t in tags:
            [s.extract() for s in soup(t)]

    @abstractmethod
    def getUtf8Str(self,str):
        return str.encode('utf-8')

    @abstractmethod
    def deleteSoupByClassName(self,soup,class_name):
        try:
            for name in class_name:
                delete_list = soup.find(attrs={'class': name})
                delete_list.extract()
        except Exception,e:
            pass

    def generateXml(self,info_list,list):
        doc = xml.dom.minidom.Document()
        root = doc.createElement('data')
        doc.appendChild(root)
        info_manager = doc.createElement('info')
        title_nodeName = doc.createElement('title')
        title_nodeName.appendChild(doc.createTextNode(info_list['title']))

        keywords_nodeName = doc.createElement('keywords')
        keywords_nodeName.appendChild(doc.createTextNode(info_list['keywords']))

        description_nodeName = doc.createElement('description')
        description_nodeName.appendChild(doc.createTextNode(info_list['description']))

        info_manager.appendChild(title_nodeName)
        info_manager.appendChild(keywords_nodeName)
        info_manager.appendChild(description_nodeName)

        #添加到root中
        root.appendChild(info_manager)

        article_manager = doc.createElement('article')

        for str in list:
            article_node = None
            if str[0] == 'img':
                article_node = doc.createElement('img')
            elif str[0] == 'content':
                article_node = doc.createElement('content')

            if not article_node is None:
                article_node.appendChild(doc.createTextNode(str[1]))

            article_manager.appendChild(article_node)


        root.appendChild(article_manager)
        return doc