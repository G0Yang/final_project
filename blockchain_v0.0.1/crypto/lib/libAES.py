# This Python file uses the following encoding: utf-8

# https://code.i-harness.com/ko-kr/q/bf1dc2

import base64, re
from Crypto.Cipher import AES
from Crypto import Random
import random

class libAES:
    def __init__(self, *args, **kargs):
        if 'key' in kargs:
            self.key = kargs['key']
        else:
            self.key = str(int(random.random()*10000000000000000)) #16
        if 'blk_sz' in kargs:
            self.blk_sz = kargs['blk_sz']
        else:
            self.blk_sz = 32

    def encrypt( self, raw ):
        if raw is None or len(raw) == 0:
            raise NameError("No value given to encrypt")
        raw = raw + '\0' * (self.blk_sz - len(raw) % self.blk_sz)
        raw = raw.encode('utf-8')
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key.encode('utf-8'), AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ).decode('utf-8')

    def decrypt( self, enc ):
        if enc is None or len(enc) == 0:
            raise NameError("No value given to decrypt")
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, iv )
        return re.sub(b'\x00*$', b'', cipher.decrypt( enc[16:])).decode('utf-8')

if __name__ == "__main__":
    aes = libAES(key = "1234567890123456")
    aes1 = libAES(key = "1234567890123456")
    encryp_msg = aes.encrypt( 'ppppppppppp2pppppppppppppppppppppppppppppppppppppppppppp' )
    print(encryp_msg)
    msg = aes1.decrypt( encryp_msg )
    print("'{}'".format(msg))
