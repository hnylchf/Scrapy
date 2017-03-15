#!/usr/bin/python
# -*- coding:utf-8 -*-
import ConfigParser
import os


def getConfig(section, key):
    try:
        config = ConfigParser.ConfigParser()
        # path = os.path.split(os.path.realpath(__file__))[0] + '/config/config.conf'
        config.read("../config/config.conf")
        return config.get(section, key)
    except Exception,e:
        print e

