#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
import logging.config
from BaseModel.BaseModel import *

from Http import *


class Index(BaseModel):
    url = ''
    def __init__(self,url):
        BaseModel.__init__(self,url)

    def delSoupTag(self, soup, tags):
        super(Index, self).delSoupTag(soup, tags)

    def pushMq2(self, msg):
        super(Index, self).pushMq2(msg)

    def img_parse(self, soup):
        return super(Index, self).img_parse(soup)

    def pushMq(self, msg):
        super(Index, self).pushMq(msg)

    def link_parse(self, soup):
        return super(Index, self).link_parse(soup)

    def video_parse(self, soup):
        super(Index, self).video_parse(soup)

    def getSoup(self, html):
        return super(Index, self).getSoup(html)

    def getInfo(self, soup):
        return super(Index, self).getInfo(soup)

    def getContent(self, soup):
        list = soup.find(attrs={'class': 'categories J_newsListNavBar'})
        return list

    def translation(self, str):
        return super(Index, self).translation(str)

    def text_parse(self, soup):
        return super(Index, self).text_parse(soup)

    def getUtf8Str(self, str):
        return super(Index, self).getUtf8Str(str)


if __name__ == '__main__':
    # url = 'http://wow.17173.com/content/2017-03-14/20170314093844473_all.shtml#pageanchor1'
    url = 'http://www.yopai.com/list-6-1.html'
    a = Index(url)
    h = Http(url,None)
    html = h.send_get()
    soup = a.getSoup(html)
    content = a.getContent(soup)
    links = a.link_parse(content)


    for link in links:
        print link
        a.pushMq(link)
