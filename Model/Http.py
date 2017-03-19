#!/usr/bin/python
# -*- coding:utf-8 -*-

from BaseModel.BaseHttp import *


class Http(BaseHttp):

    url = None
    handler = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
               ('Accept-Encoding','gzip, deflate, sdch'),
               ('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6'),
               ('Cache-Control','max-age=0'),
               ('Connection','keep-alive'),
               ('Host','www.yopai.com'),
               # ('Referer',''),
               ('Upgrade-Insecure-Requests',1),
               ('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
               ]

    def __init__(self,url,handler):
        self.url = url


        if not handler is None:
            self.handler = handler

        BaseHttp.__init__(self,url,self.handler,'cookie.txt')


    def save_cookie(self, cookie):
        super(Http, self).save_cookie(cookie)

    def get_cookie(self):
        return super(Http, self).get_cookie()

    def send_get(self,cookies = None):

        html = super(Http, self).send_get(self.get_cookie())

        return html


    def setHandlers(self, handlers):
        super(Http, self).setHandlers(handlers)

    def send_post(self, post_data):
        super(Http, self).send_post(post_data)

    def getHtmlByPhantomJs(self):
        return super(Http, self).getHtmlByPhantomJs()

