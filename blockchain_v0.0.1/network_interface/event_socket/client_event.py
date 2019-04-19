# This Python file uses the following encoding: utf-8

import socket
import sys
import ast

def argvDecoder(argv):
    if not type(argv) == type(list()):
        return False
    result = {}

    for i in argv[1:]:
        try: result[i.split("=")[0].split("-")[1].upper()] = i.split("=")[1]
        except: pass

    if 'ID' in result and 'PW' in result:
        result['TYPE'] = 'login'
        return result

    return result

def eventHandler(argv): # client
    HOST = 'localhost'
    PORT = 14010
    argv = argvDecoder(argv)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(argv)
        if len(str(argv)) == 2:
            s.sendall("".encode())
        #if 'filename' in argv:
            #s.sendall(str(argv).encode())
            #with open(argv['filename'], 'rb') as filedata:
                #s.sendall(filedata.read())
        s.sendall(str(argv).encode())

    return

if __name__ == '__main__':
    eventHandler(sys.argv)
