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
        self.B_hash = None
        
        self.size = len(str(self.to_dict()))
        return

    def add(self, tx):
        self.body.append(tx)
        self.setHash()
        self.size = len(str(self.to_dict()))
        return True

    def setHash(self):
        h = libhash()
        h.update(str(self.to_dict()))
        self.B_Hash = h.getsha256()
        return


if __name__ == "__main__":
    b = block()

    a = b.add(123)

    print(a)

    print(b.to_dict())
    print(type(b.header))
