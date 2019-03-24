# This Python file uses the following encoding: utf-8

import socket
import queue
import threading
import sys, os
import ast
import time

Q_event = queue.Queue()

class loginServer(threading.Thread): # server
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        self.HOST = s.getsockname()[0]
        self.PORT = 14003
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
                    Q_event.put((argv, "login"))
                    continue
                
        return

    def stop(self):
        self.running = False
        return

class loginHandler(threading.Thread): # client
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
                argv, data = Q_event.get()
                print('queue server', argv, "recv", data)
                if not data == 'login':
                    with open("recv_" + argv['filename'], 'wb') as f:
                        f.write(data)

                if 'ID' in argv and 'PW' in argv:
                    print(132214)
                    result = login(ID = argv['ID'], PW = argv['PW'])
                    print('로그인 결과', result)

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

        threads.append(loginServer())
        threads.append(loginHandler())

        for i in threads:
            print('start', i)
            i.start()

        time.sleep(60*60*24)
        
    except:
        for i in threads:
            i.stop()
            print('stop', i)

