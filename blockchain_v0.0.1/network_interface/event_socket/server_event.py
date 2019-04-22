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

from login_socket.client_login import login, logout # MSP에 통신하며 로그인하는 함수
from core.makeLedger import * # 트랜잭션, 블록, 체인을 만드는 함수모음
from core.fileToDict import fileToDict # 파일 이름으로 파일을 저장하고 불러오는 클래스
from p2p_socket.server_p2p import P2PServer, P2PHandler  # 합의를 위한 P2P모듈


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
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    print('log : server start', (self.HOST, self.PORT))
                    s.bind((self.HOST, self.PORT))
                    s.listen(0)
                    conn, addr = s.accept()
                    argv = conn.recv(1024*1024).decode()
                    argv = ast.literal_eval(argv)
                    print("log : 연결 정보 :",  type(argv), argv)
                
                    s.close()
                    conn.close()

                    Q_event.put(argv)   
            except Exception as e:
                print("error : class EventServer def run Exception")
                s.close()
                print(e)
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
        self.P2P_Q = queue.Queue()
        self.threads = []

        return 

    def run(self):
        print('log : queue server start')
        while self.running:
            try:
                argv = Q_event.get()
                print('log : queue server : ', type(argv), argv)


                if 'TYPE' in argv:
                    print("log : type detect : ", argv['TYPE'])


                    # 로그인
                    if argv['TYPE'] == 'login':
                        print("log : login start")
                        result = login(argv['ID'], argv['PW'])
                        print("log : login result :", result, type(result))
                        
                        # 로그인 성공 시 수행함
                        if result:
                            self.loginState = result
                            self.Identity = argv['ID']
                            
                            try:
                                self.threads.append(P2PServer(self.P2P_Q, self.Identity))
                                self.threads.append(P2PHandler(self.P2P_Q, self.Identity))

                                for i in self.threads:
                                    print('start', i)
                                    i.start()
                                print("log : P2P server running")
                            except:
                                pass


                    # 로그아웃
                    if argv['TYPE'] == 'logout':
                        print("log : logout start")
                        result = logout(self.Identity)
                        print("log : logout result :", result, type(result))

                        # 로그아웃 실패시 수행
                        if result:
                            self.loginState = not result
                            self.Identity = None
                            
                            for i in self.threads:
                                print("stop", i)
                                i.stop()



                    # 현재 상태 확인
                    if argv['TYPE'] == 'status':
                        print("----- Status -----")
                        print("로그인 상태 :", self.loginState)
                        print("로그인 유저 이름 :", self.Identity)
                        


                    # 트랜잭션 발생
                    if argv['TYPE'] == 'event':
                        if not "FILENAME" in argv:
                            print("log : not in filename")
                            continue
                        elif self.Identity == None:
                            print("log : needs login")
                            continue
                        f = fileToDict()
                        fileDic = f.fileread(argv["FILENAME"])
                        fileDic["Identity"] = self.Identity

                        tx = maketx(fileDic)
                        data = tx.to_dict() # 생성된 트랜잭션 데이터 (딕셔너리)
                        self.P2P_Q.put((data, self.Identity, None)) # 생성된 데이터를 별도 스레드로 넘겨 합의 알고리즘 수행

                        pass
                else:
                    continue


                
            except Exception as e:
                print("class EventHandler Error")
                print(e)
        return

    

    def stop(self):
        print("log : eventHandler end")
        if self.loginState:
            try: print("log : 강제 로그아웃 실행", logout(ID = self.Identity))
            except: pass
        self.running = False
        
        for i in self.threads:# 내부 p2p 서버 종료
            i.stop()
            print('stop', i)

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

