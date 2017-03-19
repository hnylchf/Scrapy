#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
import logging.config
from BaseModel.BaseScheduler import *
import os
import time
from mq.client import *
from BaseModel.ConfigUtil import *
import re


class Scheduler(BaseScheduler):
    client = lg_mq_client(getConfig('host','mq_prot'))
    def run(self):
        while True:
            fp = os.popen("ps ax | grep python | grep -v grep | wc -l")
            cnt = fp.read()
            print '当前执行量:' + cnt
            if int(cnt) < 10:
                print 'start'
                self.add_event()
                # time.sleep(1)
                print 'end'
            else:
                time.sleep(1)
                pass

    def add_event(self):
        url = self.client.pop()
        # url = 'http://wow.17173.com/news/wodnews.shtml'
        try:
            if not url == None:
                print "start:" + url
                logging.info('start:' + url)
                python_shell = ''
                if url.find('/content/') >= 1:
                    python_shell = "nohup python ./Content.py " + url + " & > /dev/null"
                elif len(re.findall(r"/[^\s]+\.(jpg|gif|png|bmp)", url)) >= 1:
                    python_shell = "nohup python ./ImageDown.py " + url + " & > /dev/null"
                elif url.find('/news/') >= 1:
                    python_shell = "nohup python ./List.py " + url + " & > /dev/null"
                    logging.info('shell-list:' + python_shell)
                os.popen(python_shell)
            else:
                self.logger.error('url is null')
        except Exception, e:
            self.logger.error(e)




if __name__ == '__main__':
    s = Scheduler()
    s.run()