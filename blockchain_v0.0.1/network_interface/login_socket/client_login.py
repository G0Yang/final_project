# This Python file uses the following encoding: utf-8

# https://soooprmx.com/archives/8737

import socket, os, pathlib, sys, ast, time
 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from crypto.lib.libAES import libAES
from chaincode.smartContract import *

HOST = "chgoyang.iptime.org"
#HOST = "192.168.0.38"
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
        
        lastBlockHash = {}
        for i in chainList:
            chain = findContract(i)
            lastBlockHash[i] = chain['chains'][len(chain['chains'])-1]['B_Hash']

        s.sendall(str(lastBlockHash).encode())
        result = s.recv(1024).decode()
        if result == 'True':
            return True
        else:
            return False
    return False

def logout(ID = ""):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        logout = {
            'type' : 'logout',
            'ID' : ID
            }
        s.sendall(str(logout).encode())
        result = s.recv(1024).decode()
        result = ast.literal_eval(result)
        s.close()
        return result

    return False

def isOnline(ID = ''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        isOnline = {
            'type' : 'isOnline',
            'ID' : ID
            }
        s.sendall(str(isOnline).encode())
        result = s.recv(1024).decode()
        s.close()
        return result
    return



if __name__ == '__main__':  
    try:
        type = input("1 : login\n2 : logout\n : ")
        ID = 'id00124'
        PW = 'pw00124'
        if type == '1':
            #ID = input('ID : ')
            #PW = input('PW : ')
            result = login(ID = ID, PW = PW)
            print(result)
        elif type == '2':
            #ID = input('ID : ')
            result = logout(ID = ID)
            print(result)
        else:
            pass
    except Exception as e:
        print(e)
        pass
