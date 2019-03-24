# This Python file uses the following encoding: utf-8

# https://soooprmx.com/archives/8737

import socket, os, pathlib, sys, ast
 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from crypto.lib.libAES import libAES

HOST = 'localhost'
PORT = 5075

def p2p(ID = ''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(s.getpeername())

        login = {'type' : 'loginSync'}

        s.sendall(str(login).encode())

        key = s.recv(1024*1024).decode()

        aes = libAES(key = key)

        #PW = aes.encrypt(PW)
        PW = 'asdasd'

        login = {
            'type' : 'loginAck',
            'ID' : ID,
            'PW' : PW
            }
        s.sendall(str(login).encode())
        
        result = s.recv(1024*1024).decode()
        result = ast.literal_eval(result)
        s.close()
        return result


if __name__ == '__main__':  
    try:
        ID = input('ID : ')
        result = p2p(ID = ID)
        print(result, type(result))
    except Exception as e:
        print(e)
        pass
