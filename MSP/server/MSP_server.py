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

 
# 명령어 처리를 위한 Queue호출 및 순환 루틴
class memberShipHandler(threading.Thread):
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.HOST = s.getsockname()[0]

        self.Q = Q

        return 

    def run(self):
        while self.running:
            try:
                HOST, conn, addr, argv = self.Q.get()

                # 매개변수에 type가 없으면 종료
                if 'type' not in argv:
                    conn.close()
                    continue

                # 원격 요청
                if HOST == s.getsockname()[0]:
                    self.handler_global(conn, addr, argv)

                # 로컬 요청
                if HOST == "localhost":
                    self.handler_localhost(conn, addr, argv)
                
                conn.close()
            except Exception as e:
                print(e)
        return

    def handler_localhost(self, conn, addr, argv):
        try:
            pass
        except Exception as e:
            print(e)
            return False
        else:
            return True
        return False


    def handler_global(self, conn, addr, argv):
        try:
            # 로그인 과정
            if argv['type'] == 'login' and "ID" in argv and "PW" in argv:
                S_chainList = getUserChains(argv['ID'])
                print(S_chainList, argv['ID'])
                conn.sendall((str(S_chainList).encode()))
                print('chain list send')
                C_chainList = conn.recv(1024*1024).decode()
                print(C_chainList, "recved")
                C_chainList = ast.literal_eval(C_chainList)

                WSLastBlockHash = {}

                for i in C_chainList:
                    block = getlastBlock(ID = argv['ID'], CHID = i)
                    WSLastBlockHash[i] = block['B_Hash']

                loginResult = login(argv['ID'], argv['PW'])
                print("log : loginResult : ", loginResult)

                if WSLastBlockHash == C_chainList and loginResult:
                    conn.sendall("True".encode())
                else:
                    conn.sendall("False".encode())
                print("log : end!!!")
                conn.close()
                return True

            # 로그아웃 과정
            if argv['type'] == 'logout' and "ID" in argv:
                print("시작")
                if logout(argv['ID']):
                    conn.sendall("True".encode())
                    print(True)
                    conn.close()
                else:
                    conn.sendall("False".encode())
                    print(False)
                    conn.close()

            # 이벤트 과정
            if argv['type'] == "event":
                pass

        except Exception as e:
            print(e)
            return False
        else:
            return True
        return False

    def stop(self):
        print("worldStateHandler END")
        self.running = False

# 외부 접속용 ip 서버
class memberShipServer(threading.Thread): # server
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
            try:
                print('databaseServer')
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    print('server start', (self.HOST, self.PORT))
                    s.bind((self.HOST, self.PORT))
                    s.listen(0)
                    conn, addr = s.accept()
                    argv = conn.recv(1024*1024).decode()
                    argv = ast.literal_eval(argv)
                
                    self.Q.put([str(self.HOST), conn, addr, argv])
            except Exception as e:
                print(e)

        return

    def stop(self):
        print('databaseServer END')
        self.running = False


if __name__ == '__main__':
    try:
        threads = []
        
        threads.append(memberShipHandler())
        threads.append(memberShipServer())

        for i in threads:
            print('start', i)
            i.start()

        time.sleep(60*60*24)
        
    except:
        for i in threads:
            i.stop()
            print('stop', i)

