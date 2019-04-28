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
            



        return

    def update(self, data):
        data.update(self.to_dict())
        self.from_dict(data)
        self.setHash()
        self.size = len(str(self.to_dict()))
        self.setHash()
        return 
    

    def getHash(self):
        h = libhash()
        dic = self.to_dict()
        h.update(str(dic))
        return h.getsha256()

if __name__ == "__main__":
    t1 = time.time()
    for i in range(0,10000):
        t = transaction()

        data = t.to_dict()

        #print(type(data))
        #print(data)

        data['TXID'] = "123"

        t.from_dict(data)


        data = t.to_dict()

        #print(type(data))
        #print(data)

        t.update(data)
    
        data = t.to_dict()

        #print(type(data))
        #print(data)
    
        t.getHash()
        t.to_dict()
    t2 = time.time()

    print("total time :", t2-t1)

    # 10000 benchmark
    # no self.h
    #1.2570581436157227
    #1.252007246017456
    #1.2400245666503906
    # avg = 1.25

    # with self.h
    #1.2690420150756836
    #1.2777152061462402
    #1.2991104125976562
    # avg = 1.28