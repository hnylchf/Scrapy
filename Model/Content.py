#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")
import logging.config
from BaseModel.BaseModel import *
from Http import *
from FilterText import *


class Content(BaseModel):
    def img_parse(self, soup):
        return super(Content, self).img_parse(soup)

    def getSoup(self, html):
        return super(Content, self).getSoup(html)

    def getInfo(self, soup):
        return super(Content, self).getInfo(soup)

    def getUtf8Str(self, str):
        return super(Content, self).getUtf8Str(str)

    def link_parse(self, soup):
        return super(Content, self).link_parse(soup)

    def pushMq(self, msg):
        super(Content, self).pushMq(msg)

    def delSoupTag(self, soup, tags):
        super(Content, self).delSoupTag(soup, tags)

    def text_parse(self, soup):
        return super(Content, self).text_parse(soup)

    def pushMq2(self, msg):
        super(Content, self).pushMq2(msg)

    def __init__(self, url):
        super(Content, self).__init__(url)

    def getContent(self, soup):
        list = soup.find(attrs={'class': 'article'})
        self.deleteSoupByClassName(list,['info','summary','font-size','summary'])
        return list

    def video_parse(self, soup):
        super(Content, self).video_parse(soup)

    def deleteSoupByClassName(self, soup, class_name):
        super(Content, self).deleteSoupByClassName(soup, class_name)

    def generateXml(self, info_list, list):
        return super(Content, self).generateXml(info_list, list)


if __name__ == '__main__':
    url = 'http://wow.17173.com/content/2017-03-20/20170320175907101.shtml'
    con = Content(url)
    filter = FilterText(['_17173.com', '17173', '中国游戏第一门户站'])
    http = Http(url, None)
    html = http.send_get()
    soup = con.getSoup(html)
    content = con.getContent(soup)
    info = con.getInfo(soup)

    for s in info:
        str = filter.filterText(info[s])
        info[s] = str
    text = filter.filterText(con.text_parse(content))
    doc = con.generateXml(info,text)
    str =  doc.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8")
    print str


