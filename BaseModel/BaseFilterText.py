#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

sys.path.append("..")
import logging.config
from abc import ABCMeta, abstractmethod


class BaseFilterText(object):
    __metaclass__ = ABCMeta
    filter = ['中国游戏第一门户站']

    def __init__(self, filters = None):
        if not filters is None:
            self.filter = filters

    @abstractmethod
    def filterText(self,str):
        for s in self.filter:
            str = str.replace(s, '')
        return str