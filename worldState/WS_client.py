# This Python file uses the following encoding: utf-8

# https://soooprmx.com/archives/8737

import socket, os, pathlib, sys, ast, time
 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from crypto.lib.libAES import libAES
from chaincode.smartContract import *

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

HOST1 = s.getsockname()[0]
PORT1 = 14005

HOST = 'localhost'
PORT = 14011

def login(ID = '', PW = ''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        login = {
            'type' : 'loginAck',
            'ID' : ID,
            'PW' : PW
            }

        s.sendall(str(login).encode())

        chainList = s.recv(1024*1024).decode()
        chainList = ast.literal_eval(chainList)

        lastBlockHash = []
        localChainList = listup()

        if type(chainList) is not type(list()):
            return False
        else:
            for i in chainList:
                if i in localChainList:
                    lastBlockHash.append(i)

        print(localChainList)
        


def login1(ID = '', PW = ''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST1, PORT1))

        login = {
            'type' : 'loginAck',
            'ID' : ID,
            'PW' : PW
            }

        s.sendall(str(login).encode())
        
def decoder(argv):
    if not type(argv) == type(list()):
        return False
    result = {}
    for i in argv[1:]:
        if '-ID=' in i:
            result['ID'] = i.split('-ID=')[1]
        if '-PW=' in i:
            result['PW'] = i.split('-PW=')[1]
        if '-type=' in i:
            result['TYPE'] = i.split('-type=')[1]
        if '-filename=' in i:
            result['filename'] = i.split('-filename=')[1]
            result['filesize'] = len(open(result['filename'], 'rb').read())
    return result

def main(argv):
    argv = decoder(argv)


    return

if __name__ == '__main__':  
    try:
        ID = input('ID : ')
        PW = input('PW : ')
        #result = login(ID = ID, PW = PW)
        #print(result, type(result))
        result = login1(ID = ID, PW = PW)
        print(result, type(result))
    except Exception as e:
        print(e)
        pass
