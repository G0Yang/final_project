# This Python file uses the following encoding: utf-8

import socket

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    return s.getsockname()[0]

#print(getIP())