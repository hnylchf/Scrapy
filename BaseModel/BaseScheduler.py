#!/usr/bin/python
# -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod
import logging.config
class BaseScheduler(object):

    __metaclass__ = ABCMeta
    logger = None
    def __init__(self):
        logging.config.fileConfig("../config/logging.conf")
        self.logger = logging.getLogger()

    @abstractmethod
    def run(self):pass

    @abstractmethod
    def add_event(self):pass


