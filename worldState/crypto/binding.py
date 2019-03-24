# This Python file uses the following encoding: utf-8

from signing import signing, designing, libRSA, os, ast
from lib.libAES import libAES, random

class binding():
    def __init__(self, *args, **kargs):
        if 'block' in kargs and 'pubkey' in kargs:
            s = signing(data = kargs['block'])
            self.pubkey = kargs['pubkey']
            
            self.key = ""
            while not len(self.key) == 16:
                print("not 16", self.key)
                self.key = str(int(random.random()*10000000000000000))
            print("en",self.key)
            
            
            print("1")
            r = libRSA()
            r.savekeys(pubkey = self.pubkey, pubname = "pub1.bit")

            self.sign = s.getsign()
            a = libAES(key = self.key)
            
            self.encsign = a.encrypt(str(self.sign))
            
            self.enckey = r.enc("pub1.bit", self.key.encode("utf-8"))
            os.remove('pub1.bit')
        else:
            return
        return

    def getbind(self):
        try:
            return {
                "encsign" : self.encsign,
                "enckey" : self.enckey
                }
            
        except Exception as e:
            print("getbind in binding")
            print(e)
            return False


class debinding():
    def __init__(self, *args, **kargs):
        if args:
            self.encsign = args[0]['encsign']
            self.enckey = args[0]["enckey"]
            self.pri = args[1]
        else:
            return
        return

    def debind(self):
        try:
            print("2")
            r = libRSA()
            r.savekeys(prikey = self.pri, priname = "pri1.bit")
            self.key = r.dec("pri1.bit", self.enckey)
            os.remove('pri1.bit')
            self.key = str(self.key)[2:18]
            print("de",self.key)

            a = libAES(key = self.key)
            signed = a.decrypt( self.encsign )
            
            signed = ast.literal_eval(signed)

            d = designing(signed)
            re = d.design()
            self.data = d.data
            if re:
                return True
            else:
                return False
        except Exception as e:
            print("debind in debinding")
            print(e)
        else:
            return True
        return False
        
if __name__ == "__main__":
    data = open("jn4583nh226632.json", "r")
    data = data.read()
    print(data)
    

    print("3")
    r = libRSA()
    pri, pub = r.makekeys()
    b = binding(block = data, pubkey = pub)
    
    d = debinding(b.getbind(), pri)
    re = d.debind()
    print("main re :", re)

    print()
    print()
    print(d.data)
    
