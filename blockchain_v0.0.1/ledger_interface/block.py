# This Python file uses the following encoding: utf-8

import sys, os
sys.path.append(os.path.dirname(__file__))

from transaction import *
#from convert_json import *
from blockheader import blockheader

class block(PyJSON):
    def __init__(self, *argv, **kwargv):
        self.header = blockheader().to_dict()
        self.body = []
        self.B_Hash = None
        
        self.size = len(str(self.to_dict()))
        return

    def add(self, tx):
        self.body.append(tx)
        self.setHash()
        self.size = len(str(self.to_dict()))
        return True
    
    def setHash(self):
        h = libhash()
        dic = self.to_dict()
        dic['B_Hash'] = None
        dic['size'] = None
        h.update(str(dic))
        self.B_Hash = h.getsha256()
        return True

    def getHash(self):
        h = libhash()
        dic = self.to_dict()
        dic['B_Hash'] = None
        dic['size'] = None
        h.update(str(dic))
        return h.getsha256()


if __name__ == "__main__":
    t = transaction()

    data = {}

    data['TXID'] = "123"

    t.update(data)

    b = block()

    b.add(t)


    print(b.to_dict())
    print(type(b.header))
