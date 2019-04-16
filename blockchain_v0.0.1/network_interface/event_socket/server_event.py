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

# 파일을 읽어서 dict로 반환해주는 함수
def fileread(argv):
    if 'filename' in argv:
        with open(argv['filename'], 'rb') as file:
            filedata = file.read()
            filesize = len(filedata)
            return {
                "filename" : argv['filename'],
                "filedata" : filedata,
                "filesize" : filesize
                }
    return False

# 명령어를 받아들이는 소켓 서버 localhost
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
                print('log : server start', (self.HOST, self.PORT))
                s.bind((self.HOST, self.PORT))
                s.listen(0)
                conn, addr = s.accept()
                argv = conn.recv(1024*1024).decode()
                argv = ast.literal_eval(argv)
                print("log : 연결 정보 :", type(argv), argv)
                
                Q_event.put(argv)                
        return

    def stop(self):
        self.running = False
        return

# 로컬 명령어를 Queue에서 받아와 수행하는 루틴
class EventHandler(threading.Thread): # client
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.loginState = False
        self.Identity = None

        return 

    def run(self):
        print('log : queue server start')
        while self.running:
            try:
                argv = Q_event.get()
                print('log : queue server : ', type(argv), argv)

                if 'TYPE' in argv:
                    print("log : type detect : ", argv['TYPE'])
                    if argv['TYPE'] == 'login':
                        print("log : login start")
                        result = login(argv['ID'], argv['PW'])
                        print("log : login result :", result, type(result))
                        if result:
                            self.loginState = result
                            self.Identity = argv['ID']

                    if argv['TYPE'] == 'logout':
                        print("log : logout start")
                        result = logout(self.Identity)
                        print("log : logout result :", result, type(result))
                        if result:
                            self.loginState = not result
                            self.Identity = None

                    if argv['TYPE'] == 'status':
                        print("----- Status -----")
                        print("로그인 상태 :", self.loginState)
                        print("로그인 유저 이름 :", self.Identity)
                else:
                    continue


                
            except Exception as e:
                print(e)
        return

    

    def stop(self):
        print("log : eventHandler end")
        if self.loginState:
            try: print("log : 강제 로그아웃 실행", logout(ID = self.Identity))
            except: pass
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

