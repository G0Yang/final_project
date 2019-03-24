# This Python file uses the following encoding: utf-8

from threading import Thread, Lock
import queue

import socket, socketserver
import sys, os, time, ast, random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from getIP import getIP

from crypto.lib.libAES import libAES

HOST = getIP()
PORT = 14003

Q = queue.Queue()

contract_return = ['jn4583nh226632', 'tmpp1z95nfx380']

def switch(data = {}, conn = None, addr = None):
    if data['type'] == 'loginSync':
        pass
    return False

def thread_get():
    while True:
        print('thread_get init')
        conn, addr = Q.get()

        try:
            data = conn.recv(1024*1024).decode()
            data = ast.literal_eval(data)
        
            if type(data) is not type(dict()):
                continue

            if 'type' in data:
                result = switch(data = data, conn = conn, addr = addr)

            if not result:
                continue
        except Exception as e:
            print(e)
            continue
        else:
            Q.put((conn, addr))

        print('thread_get end')

    return


def thread_put(HOST, PORT):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(0)
            conn, addr = s.accept()
            Q.put((conn, addr))


            '''
            msg = conn.recv(1024)
            print(f'{msg.decode()}')
            conn.sendall(msg)
            conn.close()
            '''


def runP2PServer(HOST = HOST, PORT = PORT):
    #runServer(Host = HOST, Port  = PORT)
    
    threadPUT = Thread(target = thread_put, daemon = True, args = (HOST, PORT))
    threadGET = Thread(target = thread_get, daemon = True)

    threadPUT.start()
    threadGET.start()

    while True:
        time.sleep(60*60*24)

from urllib.request import urlopen
import re
def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'

    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data)#.group(1)

if __name__ == '__main__':
    print(socket.gethostbyname(socket.getfqdn()))
    print(socket.getfqdn())
    print(socket.gethostbyname(socket.gethostname()))
    print(socket.gethostbyname_ex(socket.gethostname()))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname())
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("255.255.255.255", 80))
    print(s.getsockname())

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("localhost", 80))
    print(s.getsockname())

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    print(s.getsockname())

    print(getPublicIp())



    #runP2PServer(HOST = HOST, PORT = PORT)