#!/usr/bin/python
# -*- coding:utf-8 -*-
from BaseModel.BaseModel import BaseModel
import sys
from bs4 import BeautifulSoup
sys.path.append("..")


class Index(BaseModel):

    def __init__(self,url):
        BaseModel.__init__(self,url)

    def getContent(self,soup):
        pc_column = soup.find(attrs={'class': 'nav nav-pc'})
        m_column = soup.find(attrs={'class': 'nav nav-m'})
        pc_list = self.link_parse(pc_column)
        m_column = self.link_parse(m_column)
        return pc_list

    def getInfo(self,soup):
        pass

    def saveContent(self,soup):
        pass

    def saveHtmlInfo(self, path, info):
        pass

    def img_parse(self,soup):
        pass

    def video_parse(self,soup):
        pass

    def link_parse(self, soup):
        return super(Index, self).link_parse(soup)

    def getSoup(self,html):
        soup = BeautifulSoup(html)
        return soup

    #删除标签
    def delSoupTag(self,soup,tags):
        for t in tags:
            [s.extract() for s in soup(t)]


if __name__ == '__main__':
    url = 'http://mir.17173.com'
    # url = sys.argv[1]
    a = Index(url)
    html = a.util.getHtmlByGet()
    soup = a.getSoup(html)
    print a.getContent(soup)