#!/usr/bin/python
# -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod

class SchedulerModel(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):pass

    @abstractmethod
    def add_event(self):pass


