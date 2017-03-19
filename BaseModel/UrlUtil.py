#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import urllib
from tld import get_tld
from urlparse import *
import logging
import logging.config
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath

logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger()
#url工具类
class UrlUtil():
    url = ''    #url
    host = ''   #host
    path = ''   #路径
    suffix = '' #后缀
    domaine = '' #全域名
    path_suffix = ''
    path2 = ''  #路径 以/结尾


    def __init__(self,url):
        #补全http
        if not url.startswith("http://") and not url.startswith('https://'):
            url = 'http://' + url
        self.url = url
        self.Analysis()

    def Analysis(self):
        self.host = get_tld(self.url)
        self.domaine = self.getDomaineHost()
        r = urlparse(self.url)
        self.path_suffix = r.path
        index = self.find_last(r.path,'.')
        if not index == -1:
            self.suffix = self.path_suffix[index:len(self.path_suffix)]
            self.path = self.path_suffix[0:index]
        else:
            self.path = self.path_suffix

    def find_last(self,string, str):
        last_position = -1
        while True:
            position = string.find(str, last_position + 1)
            if position == -1:
                return last_position
            last_position = position

    #检查域名是不是本站
    def isCheckUrlHost(self, url = None):
        try:
            if url == '':
                return False
            elif url.find('javascript:') >= 1:
                return False
            elif url == '#':
                return False
            elif not url.startswith("http://"):
                url = 'http://' + url

            tld_host = get_tld(url)
            r = urlparse(url)
            if self.host == tld_host:
                return True
        except Exception, e:
            return False


    def getDomaineHost(self):
        proto, rest = urllib.splittype(self.url)
        res, rest = urllib.splithost(rest)
        return "http://" + res


    def urlJoin(self,base, url):
        url1 = urljoin(base, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))