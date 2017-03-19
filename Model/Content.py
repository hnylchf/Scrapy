#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
import logging.config
from BaseModel.BaseModel import *
from Http import *
from BaseModel.BaseTranslation import*

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
        list = soup.find(attrs={'class': 'texts'})
        delete_list = soup.find(attrs={'id': 'zannum'})
        delete_list.extract()
        return list

    def video_parse(self, soup):
        super(Content, self).video_parse(soup)

    def translation(self, str):
        return super(Content, self).translation(str)


if __name__ == '__main__':
    url = 'http://www.yopai.com/show-2-177058-1.html'
    con = Content(url)
    http = Http(url, None)
    html = http.send_get()
    soup = con.getSoup(html)
    content = con.getContent(soup)
    text = con.text_parse(content)
    parse_text = con.translation(text)
    print text
    print parse_text



