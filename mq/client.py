#!/usr/bin/python

import socket
import select

class lg_mq_client:

    __sockfd = None
    __sockfd_list = []

    def conn(self, host):
        try:
            self.__sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.__sockfd.connect((host, 7701))
            self.__sockfd.setblocking(False)
            self.__sockfd_list.append(self.__sockfd)
        except:
            return None

    def __init__(self, host):
            self.conn(host)

    def push(self, key):
        try:
            data = "push1%04d" % len(key) + key
            self.__sockfd.send(data)
            select.select(self.__sockfd_list, [], [], 1)
            return self.__sockfd.recv(4096)
        except:
            return None
    
    def push2(self, key):
        try:
            data = "push2%04d" % len(key) + key
            self.__sockfd.send(data)
            select.select(self.__sockfd_list, [], [], 1)
            return self.__sockfd.recv(4096)
        except:
            return None

    def pop(self):
        try:
            self.__sockfd.send("__pop")
            select.select(self.__sockfd_list, [], [], 1)
            data = self.__sockfd.recv(4096)
            if data and data != "not data": return data
            return None
        except:
            return None

        def close(self):
            self.__sockfd.close()


# print mq.push("111")
# print mq.push("222")
# print mq.push("333")
# print mq.push("111")
# print mq.push("222")
# print mq.push("333")
#
# print mq.pop()
# print mq.pop()
# print mq.pop()
# print mq.pop()
#
# print mq.push2("111")
# print mq.push2("222")
# print mq.push2("333")
#
# print mq.pop()
# print mq.pop()
# print mq.pop()
# print mq.pop()



