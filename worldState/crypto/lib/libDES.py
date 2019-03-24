# This Python file uses the following encoding: utf-8

# http://blog.naver.com/PostView.nhn?blogId=jkf941&logNo=220782332149&parentCategoryNo=&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView

from Crypto.Cipher import DES3
from Crypto.Hash import SHA256 as SHA

class libDES():
    def __init__(self, *args, **kargs):
        if 'keytext' in kargs:
            keytext = kargs['keytext']
        else:
            keytext = ""
        if 'ivtext' in kargs:
            ivtext = kargs['ivtext']
        else:
            ivtext = ""
            
        hash = SHA.new()
        hash.update(keytext.encode('utf-8'))
        key = hash.digest()
        self.key = key[:24]

        hash.update(ivtext.encode('utf-8'))  
        iv = hash.digest()
        self.iv = iv[:8]
        return
    
    def make8String(self, msg):
        msglen = len(msg)
        filler = ''

        if msglen%8 != 0:
            filler = '0'*(8-msglen%8)
        msg += filler

        return msg 

    def enc(self, plaintext):
        plaintext = self.make8String(plaintext)
        des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        encmsg = des3.encrypt(plaintext.encode())

        return encmsg

    def dec(self, ciphertext):
        des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        decmsg = des3.decrypt(ciphertext)

        return decmsg



def main():

    keytext = 'samsjang'
    ivtext = '1234'
    msg = 'python36'



    myCipher = libDES(keytext = keytext, ivtext = ivtext)
    myCipher1 = libDES(keytext = keytext, ivtext = ivtext)

    ciphered = myCipher.enc(msg)

    deciphered = myCipher1.dec(ciphered)

    print('Original:\t%s' %msg)
    print('Ciphered:\t%s' %ciphered)
    print('Deciphered:\t%s' %deciphered.decode())

if __name__ == '__main__':
    main()
