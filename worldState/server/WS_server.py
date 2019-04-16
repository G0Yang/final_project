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

# 합의 알고리즘을 수행하는 루틴
class P2PAgreementHandler(threading.Thread):
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.HOST = s.getsockname()[0]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.bind((self.HOST, 9999))
        self.Q = Q

        self.maxAgreementNumber = 20

        self.connections = []

        return 

    def run(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                data = data.decode()
                if not data in self.connections:
                    self.connections.append((data, addr))
                print(self.connections)
            except Exception as e:
                print(e)
        return

    
    def makeOrderingList(self, hostNumder = 0):
        if not type(hostNumder) == type(int()):
            try:
                print("int가 아님")
                hostNumder = int(hostNumder)
            except:
                print("int 변환 실패")
                return False
        if hostNumder > self.maxAgreementNumber:
            hostNumder = self.maxAgreementNumber
        orderingList = []
        while len(orderingList) < (hostNumder-1)/2:
            num = random.randint(0, hostNumder)
            if num not in orderingList:
                orderingList.append(num)
        orderingList.sort()
        return orderingList

    def orderingBindList(self, bindList = []):
        if not type(bindList) == type(list()):
            try:
                print("list가 아님")
                bindList = ast.literal_evel(bindList)
            except:
                print("list 변환 실패")
                return False
        orderingList = []
        countList = makeOrderingList(len(bindList))
        for i in countList:
            orderingList.append(bindList[i])

        if not len(orderingList) == len(countList):
            return False

        return orderingList

    def stop(self):
        print("P2PAgreementHandler END")
        self.running = False
        
# 명령어 처리를 위한 Queue호출 및 순환 루틴
class worldStateHandler(threading.Thread):
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
                conn.close()
            else:
                conn.close()

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

            # 이벤트 과정
            if argv['type'] == "event":
                pass

        except Exception as e:
            print(e)
            conn.close()
            return False
        else:
            conn.close()
            return True
        return False

    def stop(self):
        print("worldStateHandler END")
        self.running = False

# 외부 접속용 ip 서버
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

# 내부 접속용localhost 서버
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
            try:
                print('worldStateServer')
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    print('server start', (self.HOST, self.PORT))
                    s.bind((self.HOST, self.PORT))
                    s.listen(0)
                    conn, addr = s.accept()
                    argv = conn.recv(1024*1024).decode()
                    argv = ast.literal_eval(argv)
                    self.Q.put(["localhost", conn, addr, argv])
            except Exception as e:
                print(e)
        return

    def stop(self):
        print('worldStateServer END')
        self.running = False
        return

if __name__ == '__main__':
    try:
        threads = []
        
        threads.append(worldStateHandler())
        threads.append(databaseServer())
        threads.append(worldStateServer())
        threads.append(P2PAgreementHandler())

        for i in threads:
            print('start', i)
            i.start()

        time.sleep(60*60*24)
        
    except:
        for i in threads:
            i.stop()
            print('stop', i)

