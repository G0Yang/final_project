# This Python file uses the following encoding: utf-8

# https://soooprmx.com/archives/8737

import socket, os, pathlib, sys, ast, time
 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from crypto.lib.libAES import libAES
from chaincode.smartContract import *

HOST = "192.168.10.81"
PORT = 14005

def login(ID = '', PW = ''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        login = {
            'type' : 'login',
            'ID' : ID,
            'PW' : PW
            }
        s.sendall(str(login).encode())
        
        chainList = s.recv(1024*1024).decode()
        chainList = ast.literal_eval(chainList)
        print('get chain list', chainList)

        localChainList = listup()

        lastBlockHash = {}

        for i in chainList:
            chain = findContract(i)
            lastBlockHash[i] = chain['chains'][len(chain['chains'])-1]['B_Hash']
        
        print(lastBlockHash)

        s.sendall(str(lastBlockHash).encode())

        print('send blockHash')

        result = s.recv(1024).decode()
        return result
    return

def logout(ID = ""):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        logout = {
            'type' : 'logout',
            'ID' : ID
            }
        s.sendall(str(logout).encode())
        result = s.recv(1024).decode()
        return result

    return

def isOnline(ID = ''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        isOnline = {
            'type' : 'isOnline',
            'ID' : ID
            }
        s.sendall(str(isOnline).encode())
        result = s.recv(1024).decode()
        return result
    return



if __name__ == '__main__':  
    try:
        ID = input('ID : ')
        result = logout(ID)
        print(result)

        #ID = input('ID : ')
        #PW = input('PW : ')
        #result = login(ID = ID, PW = PW)
        #print(result, type(result))
    except Exception as e:
        print(e)
        pass
