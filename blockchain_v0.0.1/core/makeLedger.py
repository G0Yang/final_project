# This Python file uses the following encoding: utf-8

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from ledger_interface.chain import *
from chaincode.smartContract import *

def maketx(data = {}):
    if len(data) == 0:
        return False
    t = transaction()
    t.update(data)
    return t

def makeblock(tx = {}):
    if len(tx) == 0:
        return False
    b = block()
    b.add(tx)
    return b

def makechain(block = {}):
    if len(block) == 0:
        return False
    c = chain()
    c.add(block)
    return c

if __name__ == "__main__":
    try:
        data = {
            "name" : "kim",
            "phone" : "010-1234-5678"
            }

        tx = maketx(data)
        b = makeblock(tx.to_dict())
        c = makechain(b.to_dict())
        print(type(c))
        print(c)

        c.to_json(filename = "test.json", data = c.to_dict())


        print(listup())
    except Exception as e:
        print(e)