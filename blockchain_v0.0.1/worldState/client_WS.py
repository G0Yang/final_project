# This Python file uses the following encoding: utf-8

import socket
import sys
import ast


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    return s.getsockname()[0]

def argvDecoder(argv):
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
            with open(result['filename'], 'rb') as r:
                result['file'] = r.read()
    return result

def eventHandler(argv): # client
    HOST = getIP()
    PORT = 14005
    print(HOST, PORT)
    argv = argvDecoder(argv)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(type(argv), argv)
        if len(str(argv)) == 2:
            return
        s.sendall(str(argv).encode())

    return

if __name__ == '__main__':
    eventHandler(sys.argv)