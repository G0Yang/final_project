# This Python file uses the following encoding: utf-8

import socket
import queue
import threading
import sys, os
import ast
import time

Q_event = queue.Queue()

loginState = False

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from login_socket.client_login import login, logout
from worldState.client_WS import eventHandler, argvDecoder

def eventSelector(argv):
    return

class EventServer(threading.Thread): # server
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True

        self.HOST = 'localhost'
        self.PORT = 14010
        return

    def run(self):
        while self.running:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print('server start', (self.HOST, self.PORT))
                s.bind((self.HOST, self.PORT))
                s.listen(0)
                conn, addr = s.accept()
                argv = conn.recv(1024*1024).decode()
                argv = ast.literal_eval(argv)
                
                Q_event.put(argv)                
        return

    def stop(self):
        self.running = False
        return

class EventHandler(threading.Thread): # client
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.loginState = False
        self.Identity = None

        return 

    def run(self):
        try:
            print('queue server start')
            while self.running:
                argv = Q_event.get()
                print('queue server')

                for i in argv:
                    print(i, argv[i])

                if not 'TYPE' in argv:
                    continue

                if argv['TYPE'] == 'login':
                    if self.loginState:
                        print('이미 로그인이 되있음', argv['ID'])
                        continue
                    result = login(ID = argv['ID'], PW = argv['PW'])
                    print('로그인 결과', result)
                    result = ast.literal_eval(result)
                    self.loginState = result
                    self.Identity = argv['ID']

                elif argv['TYPE'] == 'logout':
                    if not self.loginState:
                        print("로그인이 필요함")
                        continue
                    result = logout(ID = argv['ID'])
                    print('로그아웃 결과', result)
                    result = ast.literal_eval(result)
                    self.loginState = not result

                if not self.loginState:
                    print('로그인 하십시오.')
                    continue

                if argv["TYPE"] == 'event':
                    if 'filename' in argv:
                        argv['filedata'] = open(argv['filename'], 'rb').read()
                        argv['filesize'] = len(argv['filedata'])
                    pass

        except Exception as e:
            print(e)
        return

    def stop(self):
        print("eventHandler end")
        self.running = False

if __name__ == '__main__':
    try:
        threads = []

        threads.append(EventServer())
        threads.append(EventHandler())

        for i in threads:
            print('start', i)
            i.start()

        time.sleep(60*60*24)
        
    except:
        for i in threads:
            i.stop()
            print('stop', i)

