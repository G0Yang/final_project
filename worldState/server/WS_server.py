# This Python file uses the following encoding: utf-8

import socket
import threading
import sys, os
import ast
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database.databaseHandler import *

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

class worldStateHandler(threading.Thread):
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.HOST = s.getsockname()[0]

        self.Q = Q

        return 

    def run(self):
        try:
            while self.running:
                argvList = self.Q.get()

                if argvList[0] == self.HOST:
                    if argvList[3]['type'] == 'loginAck':
                        argvList[1].sendall(str(getUserChains(argvList[3]['ID'])).encode())
                        lastBlockHash = argvList[1].recv(1024*1024).decode()
                        lastBlockHash = ast.literal_eval(lastBlockHash)

                        WSLastBlockHash = {}

                        for i in lastBlockHash:
                            block = getlastBlock(ID = argvList[3]['ID'], CHID = i)
                            WSLastBlockHash[i] = block['B_Hash']


                        if isUserOnline(argvList[3]['ID']) == False:
                            if WSLastBlockHash == lastBlockHash and login(argvList[3]['ID'], argvList[3]['PW']) == "로그인 완료":
                                argvList[1].sendall("True".encode())
                            else:
                                argvList[1].sendall("False".encode())
                        else:
                            argvList[1].sendall("False".encode())
                        pass
                    if argvList[3]['type'] == 'logoutAck':
                        if logout(argvList[3]['ID']) == True:
                            argvList[1].sendall("True".encode())
                        else:
                            argvList[1].sendall("False".encode())
                        #print(argvList)
                    pass
                if argvList[0] == "localhost":
                    pass
                







        except:
            pass
        return

    def stop(self):
        print("worldStateHandler END")
        self.running = False


class databaseServer(threading.Thread): # server
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True

        self.Q = Q
        

        self.HOST = s.getsockname()[0]
        self.PORT = 14005
        return

    def run(self):
        while self.running:
            print('databaseServer')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print('server start', (self.HOST, self.PORT))
                s.bind((self.HOST, self.PORT))
                s.listen(0)
                conn, addr = s.accept()
                argv = conn.recv(1024*1024).decode()
                argv = ast.literal_eval(argv)
                
                self.Q.put([str(self.HOST), conn, addr, argv])
        return

    def stop(self):
        print('databaseServer END')
        self.running = False

class worldStateServer(threading.Thread): # server
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True

        self.Q = Q
        
        self.HOST = 'localhost'
        self.PORT = 14011
        return

    def run(self):
        while self.running:
            print('worldStateServer')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print('server start', (self.HOST, self.PORT))
                s.bind((self.HOST, self.PORT))
                s.listen(0)
                conn, addr = s.accept()
                argv = conn.recv(1024*1024).decode()
                argv = ast.literal_eval(argv)
                self.Q.put(["localhost", conn, addr, argv])
        return

    def stop(self):
        print('worldStateServer END')
        self.running = False
        return

if __name__ == '__main__':
    try:
        threads = []

        threads.append()

        for i in threads:
            print('start', i)
            i.start()

        time.sleep(60*60*24)
        
    except:
        for i in threads:
            i.stop()
            print('stop', i)

