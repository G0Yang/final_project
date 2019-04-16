# This Python file uses the following encoding: utf-8

import socket
import sys
import ast

def argvDecoder(argv):
    if not type(argv) == type(list()):
        return False
    result = {}
    for i in argv[1:]:
        if '-ID=' in i:
            result['ID'] = i.split('-ID=')[1]
        elif '-PW=' in i:
            result['PW'] = i.split('-PW=')[1]
        elif '-type=' in i:
            result['TYPE'] = i.split('-type=')[1]
        #elif '-filename=' in i:
            #result['filename'] = i.split('-filename=')[1]
            #result['filesize'] = len(open(result['filename'], 'rb').read())
        
            #with open(result['filename'], 'rb') as r:
                #result['file'] = r.read()
    
    if 'ID' in result and 'PW' in result:
        result['TYPE'] = 'login'
        return result

    if len(result) == 0:
        return False

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
