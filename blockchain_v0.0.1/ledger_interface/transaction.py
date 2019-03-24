# This Python file uses the following encoding: utf-8

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from convert_json import *
from crypto.lib.libhash import libhash

class transaction(PyJSON):
    def __init__(self, *argv, **kwargv):
        if 'TXID' in kwargv:
            self.TXID = kwargv['kwargv']
        else:
            self.TXID = None

        if 'timeStamp' in kwargv:
            self.timeStamp = kwargv['timeStamp']
        else:
            self.timeStamp = time.time()
            
        if 'name' in kwargv:
            self.name = kwargv['name']
        else:
            self.name = None
            
        if 'T_Hash' in kwargv:
            self.T_Hash = kwargv['T_Hash']
        else:
            self.T_Hash = self.setHash()

        if 'size' in kwargv:
            self.size = kwargv['size']
        else:
            self.size = len(str(self.to_dict()))



        return

    def update(self, data):
        self.from_dict(data)
        self.setHash()
        self.size = len(str(self.to_dict()))
        return 

    def setHash(self):
        h = libhash()
        h.update(str(self.to_dict()))
        self.T_Hash = h.getsha256()
        return

if __name__ == "__main__":
    t = transaction()

    data = t.to_dict()

    print(type(data))
    print(data)

    data['TXID'] = "123"

    t.from_dict(data)


    data = t.to_dict()

    print(type(data))
    print(data)

    t.update(data)
    
    data = t.to_dict()

    print(type(data))
    print(data)
