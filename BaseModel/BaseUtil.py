#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import hashlib
from UrlUtil import *

def getMd5( str):
    m2 = hashlib.md5()
    m2.update(str)
    return m2.hexdigest()

def converUrl(url):
    try:
        u = UrlUtil(url)
        if u.suffix == '':
            new_url = getMd5(u.host) + '_' + getMd5(u.path) + '.html'
        else:
            new_url = getMd5(u.host) + '_' + getMd5(u.path) + u.suffix
        return new_url
    except Exception, e:
        return ''