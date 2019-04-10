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
from core.makeLedger import *

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
                print('server start', (self.HOST, self.PORT))
                s.bind((self.HOST, self.PORT))
                s.listen(0)
                conn, addr = s.accept()
                argv = conn.recv(1024*1024).decode()
                print("------------", type(argv), argv)
                argv = ast.literal_eval(argv)
                
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
        print('queue server start')
        while self.running:
            try:
                argv = Q_event.get()
                print('queue server')

                for i in argv:
                    print(i, argv[i])

                if not 'TYPE' in argv:
                    continue

                self.login_out(argv)
                
                if argv["TYPE"] == 'event':
                    # 파일 읽기 argv[filename]
                    data = fileread(argv)
                    print("파일 읽기 :", type(data))
                    # 트랜잭션 생성
                    if type(data) is not type(dict()):
                        data = argv
                    data["ID"] = self.Identity
                    
                    tx = maketx(data)
                    
                    print("-------------------------")
                    
                    print(type(tx), type(tx.to_dict()))

                    tx.to_json(path = "C:\\Users\\milk1\\Downloads\\test\\", filename = "test_tx.json", data = tx.to_dict())
                    


                    print("-------------------------")
                    # 합의 - fms에게 합의 ip리스트를 받아와 p2p 수행
                    # 체인 저장 - 합의 결과에 따라 체인에 추가함.
                    # 마지막 블록 업로드 - WS에 업로드
                    pass
                
            except Exception as e:
                print(e)
        return

    
    def login_out(self, argv):
        try:
            if argv['TYPE'] == 'login':
                if self.loginState:
                    print('이미 로그인이 되있음', argv['ID'])
                    return False
                result = login(ID = argv['ID'], PW = argv['PW'])
                print('로그인 결과', result)
                result = ast.literal_eval(result)
                self.loginState = result
                self.Identity = argv['ID']

            elif argv['TYPE'] == 'logout':
                if not self.loginState:
                    print("로그인이 필요함")
                    return False
                result = logout(ID = argv['ID'])
                print('로그아웃 결과', result)
                result = ast.literal_eval(result)
                self.loginState = not result
                self.Identity = None

            if not self.loginState:
                print('로그인 하십시오.')
                return False
        except Exception as e:
            print(e)
            return False
        else:
            return True
        return False

    def stop(self):
        print("eventHandler end")
        if self.loginState:
            try: print("강제 로그아웃 실행", logout(ID = self.Identity))
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

