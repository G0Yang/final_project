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
                
                if 'filename' in argv and 'filesize' in argv:
                    data = conn.recv(argv['filesize'])
                    print(data)
                    with open("recv_" + argv['filename'], "wb") as f:
                        f.write(data)
                        Q_event.put((argv, data))
                        continue
                    
                if 'ID' in  argv and 'PW' in argv:
                    if 'TYPE' in argv:
                        if argv['TYPE'] == "login":
                            Q_event.put((argv, "login"))
                else:
                    if 'TYPE' in argv:
                        if argv["TYPE"] == 'logout':
                            Q_event.put((argv, "logout"))
                    continue
                
        return

    def stop(self):
        self.running = False
        return

class EventHandler(threading.Thread): # client
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.online = False
        self.Identity = None

        return 

    def run(self):
        try:
            print('queue server start')
            while self.running:
                argv, type = Q_event.get()
                print('queue server', argv, "type", type)

                if 'ID' in argv and 'PW' in argv:
                    if type == 'login':
                        result = login(ID = argv['ID'], PW = argv['PW'])
                        print('로그인 결과', result)
                        loginState = result
                else:
                    if type == "logout":
                        print("로그아웃 시도")
                        result = logout(ID = argv['ID'])
                        print('로그아웃 결과 :', result)
                        loginState = result


                if not self.online:
                    pass
                pass
        except:
            pass
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

