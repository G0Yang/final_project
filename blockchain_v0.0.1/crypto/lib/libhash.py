# This Python file uses the following encoding: utf-8
import hashlib

class libhash():
    def __init__(self, *args, **kargs):
        self.data = None
        self.update(*args, **kargs)
        return

    def update(self, *args, **kargs):
        if args:
            self.data = args[0]
        return

    def getsha256(self):
        if self.data:
            return hashlib.sha256(self.data.encode("utf-8")).hexdigest().upper()
        else:
            return None
    
    def getsha3_512(self):
        if self.data:
            return hashlib.sha3_512(self.data.encode("utf-8")).hexdigest().upper()
        else:
            return None
        
    def getmd5(self):
        if self.data:
            return hashlib.md5(self.data.encode("utf-8")).hexdigest().upper()
        else:
            return None
