#!/usr/bin/python

import os, sys
from SSDB import SSDB


class storage:
    __db = None

    def __init__(self):
        try:
            self.__db = SSDB('127.0.0.1', 8888)
        except Exception, e:
            print e
            exit(0)

    def set(self, key, value):
        shell = []
        shell.append(key)
        shell.append(value)
        return self.__db.request('set', shell)

    def get(self, key):
        shell = []
        shell.append(key)
        return self.__db.request('get', shell)

    def list_set(self, key, values):
        pass

    def list_get(self, key):
        pass

    def title_push(self, key, value):
        return self.set('1' + key, value)

    def title_pop(self, key):
        return self.get('1' + key)

    def conecnt_push(self, key, value):
        return self.set('2' + key, value)

    def conecnt_pop(self, key):
        return self.get('2' + key)


st = storage()
print st.set('k1', 'v1')
print st.get('k1')

print st.title_push('k2', 'v2')
print st.title_pop('k2')

print st.conecnt_push('k3', 'v3')
print st.conecnt_pop('k3')


