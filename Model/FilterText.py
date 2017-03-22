#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
import logging.config
from BaseModel.BaseFilterText import *

class FilterText(BaseFilterText):
    def filterText(self, str):
        return super(FilterText, self).filterText(str)

    def __init__(self, filters=None):
        super(FilterText, self).__init__(filters)