# This Python file uses the following encoding: utf-8

from lib.libRSA import libRSA
from lib.libhash import libhash
from lib.libAES import libAES, random
import os, json, pathlib, ast

class signing():
    def __init__(self, *args, **kargs):
        try:
            if "data" in kargs:
                self.data = kargs['data']
                
                h = libhash(self.data)

                r = libRSA()
                self.pri, self.pub = r.makekeys()
                r.savekeys(pubkey = self.pub, pubname = "pub.bit")
                self.enc = r.enc("pub.bit", str(h.getsha256()).encode("utf-8"))
                os.remove('pub.bit')
            else:
                return 
        except Exception as e:
            print("__init__ in signing")
            print(e)
        return

    def getsign(self):
        try:
            #return ( self.data, str(self.enc).encode("utf-8"), str(self.pri).encode('utf-8') )
            
            return {
                "data" : self.data,
                "enc" : self.enc,
                "pri" : self.pri
                }
            
        except Exception as e:
            print("getsign in signing")
            print(e)
            return False


        
class designing():
    def __init__(self, *args, **kargs):
        if args:
            self.data = args[0]["data"]
            self.enc = args[0]["enc"]
            self.pri = args[0]["pri"]
        else:
            return
        return

    def design(self):
        try:
            r = libRSA()
            r.savekeys(prikey = self.pri, priname = "pri.bit")
            msg = r.dec("pri.bit", self.enc)
            os.remove('pri.bit')
            
            h = libhash(self.data)
            
            if not h.getsha256() == msg.decode():
                return False

        except Exception as e:
            print(e)
        else:
            return True
        return False


    

if __name__ == "__main__":
    file = pathlib.Path("block_4qynvowp656379.json")
    file_text = file.read_text(encoding='utf-8')
    block = json.loads(file_text)
    
    s = signing(data = str(block))
    re = s.getsign()
    print(type(re))

    
    



    
    key = str(int(random.random()*10000000000000000))
    a = libAES(key = key)
    encsign = a.encrypt(str(re))

    b = libAES(key = key)
    
    dec = a.decrypt( encsign )

    print("dec", type(dec), dec)

    dec = ast.literal_eval(dec)



    
        
    
    d = designing(dec)

    print(d.data)

    print("matched :", d.design())

