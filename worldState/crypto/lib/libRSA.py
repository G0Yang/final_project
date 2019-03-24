# This Python file uses the following encoding: utf-8

# https://pycryptodome.readthedocs.io/en/latest/src/examples.html#generate-public-key-and-private-key

# https://github.com/nemozqqz/pycrypto-sample/blob/master/RSA_PKCS.py

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class libRSA():
    def __init__(self, *args, **kargs):
        return

    def savekeys(self, *args, **kargs):
        try:
            if 'prikey' in kargs and 'priname' in kargs:
                if kargs['prikey'] and kargs['priname']:
                    file_out = open(kargs['priname'], "wb")
                    file_out.write(kargs['prikey'])
                    file_out.close()
            if 'pubkey' in kargs and 'pubname' in kargs:
                if kargs['pubkey'] and kargs['pubname']:
                    file_out = open(kargs['pubname'], "wb")
                    file_out.write(kargs['pubkey'])
                    file_out.close()
        except Exception as e:
            print("savekeys in libRSA")
            print(e)
        else:
            return True
        return False
        
    def makekeys(self, *args, **kargs):
        try:
            key = RSA.generate(2048)
            private_key = key.export_key()
            public_key = key.publickey().export_key()
        except Exception as e:
            print("makekeys in libRSA")
            print(e)
        else:
            return private_key, public_key
        return False, False

    def enc(self, pubkey, msg):
        try:
            ekey = RSA.importKey(open(pubkey).read())
            cipher = PKCS1_OAEP.new(ekey)
            ciphertext = cipher.encrypt(msg)
        except Exception as e:
            print("enc in libRSA")
            print(e)
        else:
            return ciphertext
        return False

    def dec(self, prikey, ctext):
        try:
            dkey = RSA.importKey(open(prikey).read())
            cipher = PKCS1_OAEP.new(dkey)
            msg = cipher.decrypt(ctext)
        except Exception as e:
            print("dec in libRSA")
            print(e)
        else:
            return msg
        return False

if __name__ == "__main__":
    pubkey = 'public_rsa.pem'
    prikey = 'private_rsa.pem'
    t = libRSA()
    pri, pub = t.makekeys()
    re = t.savekeys(prikey = pri, pubkey = pub, priname = prikey, pubname = pubkey)
    print(re)
    d = t.enc(pubkey, "asd".encode())
    print(d)
