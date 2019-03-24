# This Python file uses the following encoding: utf-8

import sys, os
sys.path.append(os.path.dirname(__file__))

from metadata import metadata
from block import *
#from convert_json import *

class chain(PyJSON):
    def __init__(self, *argv, **kargv):
        self.CHID = None
        self.chains = []
        self.C_Hash = None
        self.timeStamp = time.time()
        self.metadata = metadata
        return

    def add(self, block):
        try : block.header['blockNumber'] = len(self.chains) 
        except Exception as e : return False

        self.chains.append(block)
        self.setHash()
        return

    def setHash(self):
        h = libhash()
        h.update(str(self.to_dict()))
        self.C_Hash = h.getsha256()
        return


if __name__ == "__main__":
    c = chain()
    print(c.to_dict())
    print()
    b = block()
    print(b.to_dict())
    print()
    t = transaction()
    print(t.to_dict())
    print()
    print()
    print()

    print()

    b.add(t)
    c.add(b)
    
    print(c.to_dict())
    print()
    print(b.to_dict())
    print()
    print(t.to_dict())