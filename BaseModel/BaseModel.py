#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

sys.path.append("..")
import sys
from Util.ConfigUtil import *
from Util.FileUtil import *
from Util.Util import *
from Util.UrlUtil import *
from mq.client import *
import logging.config
from abc import ABCMeta, abstractmethod
import urllib2
from bs4 import BeautifulSoup


class BaseModel(object):
    __metaclass__ = ABCMeta
    mq = None
    url = None
    urlInfo = None
    f = None
    logger = None
    main_md5 = None
    minor_md5 = None
    util = None

    def __init__(self, url):
        self.url = url
        logging.config.fileConfig("../config/logging.conf")
        self.logger = logging.getLogger()
        self.mq = lg_mq_client(getConfig('host', 'mq_prot'))  # 获取mq链接
        self.urlInfo = UrlUtil(url)
        self.util = Util(url)
        self.f = FileUtil(getConfig('host', 'host_path'))
        self.f.initPath()  # 初始化路径
        self.main_md5 = self.util.getMd5(self.urlInfo.host)  # 主ID
        self.main_md5 = self.util.getMd5(self.urlInfo.path)  # 副ID

    #获取内容块
    @abstractmethod
    def getContent(self,soup): pass

    #保存内容信息
    @abstractmethod
    def saveContent(self, path , html): pass

    #保存页面title信息
    @abstractmethod
    def saveHtmlInfo(self, path, info):pass

    # 获取网页信息
    @abstractmethod
    def getInfo(self,soup): pass

    #链接
    @abstractmethod
    def link_parse(self,soup):
        a_list = soup.find_all('a')
        result = []
        for a in a_list:
            try:
                if a.attrs.has_key('href'):
                    a_url = self.util.getUtf8Str(a['href'])
                    join_url = self.urlInfo.urlJoin(self.url,a_url)
                    if self.urlInfo.isCheckUrlHost(join_url):  # 查看是否是一个主域名下的域名
                        result.append(a_url)
            except Exception, e:
                self.logger.error(e)
        return result

    #图片
    @abstractmethod
    def img_parse(self,soup):pass

    #视频
    @abstractmethod
    def video_parse(self,soup):pass

    #获取soup
    @abstractmethod
    def getSoup(self,html):pass

    @abstractmethod
    def delSoupTag(self,soup,tags):pass



