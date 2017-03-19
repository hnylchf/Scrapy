#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
import logging.config
from BaseModel.BaseModel import *
from Http import *

class ListPage(BaseModel):

    def __init__(self, url):
        super(ListPage, self).__init__(url)

    def img_parse(self, soup):
        return super(ListPage, self).img_parse(soup)

    def translation(self, str):
        return super(ListPage, self).translation(str)

    def getSoup(self, html):
        return super(ListPage, self).getSoup(html)

    def getInfo(self, soup):
        return super(ListPage, self).getInfo(soup)

    def getUtf8Str(self, str):
        return super(ListPage, self).getUtf8Str(str)

    def link_parse(self, soup):
        h2_list = soup.findAll('h2')
        href_list = []
        for l in h2_list:
            href_list.append(super(ListPage, self).link_parse(l))
        return href_list
    def pushMq(self, msg):
        super(ListPage, self).pushMq(msg)

    def delSoupTag(self, soup, tags):
        super(ListPage, self).delSoupTag(soup, tags)

    def text_parse(self, soup):
        return super(ListPage, self).text_parse(soup)

    def pushMq2(self, msg):
        super(ListPage, self).pushMq2(msg)



    def getContent(self, soup):
        list = soup.find(attrs={'id': 'list_data'})
        return list

    def video_parse(self, soup):
        super(ListPage, self).video_parse(soup)

if __name__ == '__main__':
    # url = sys.argv[1]
    url = 'http://www.yopai.com/list-6-1.html'
    l = ListPage(url)
    http = Http(url,None)
    html = http.send_get()
    soup = l.getSoup(html)
    list = l.getContent(soup)
    href_list = l.link_parse(soup)
    for a in href_list:
        if not a == '' and not a is None:
            l.pushMq(a)
