
# This Python file uses the following encoding: utf-8

import logging
import socket
import threading, queue
import sys, os, ast, time, random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

from core.makeLedger import * 

TX_Q = queue.Queue()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]


class P2PServer(threading.Thread):
    def __init__(self, Queue, ID):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.Q = Queue
        self.ID = ID
        
        self.sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.HOST = "chgoyang.iptime.org"
        self.HOST = "192.168.0.5"
        #self.HOST = HOST
        self.PORT = 14101
        self.sock_server.sendto(str( {"TYPE" : "first connect", "ID" : self.ID} ).encode(), (self.HOST, self.PORT))

        self.Q.put(self.sock_server)
        return

    def run(self):
        while self.running:
            try:
                print('log : P2P server start', (self.HOST, self.PORT))

                argv, addr = self.sock_server.recvfrom(1024*1024)
                
                argv = ast.literal_eval(argv.decode())

                print("서버에서 받은 데이터", argv)

                

                if type(argv) == type(list()):
                    tx = TX_Q.get()
                    print("합의 요청 보냄",  tx)
                    agreeList = []
                    tmp_tx = maketx(tx)
                    tmp_Hash = tmp_tx.getHash()

                    for i, j in argv:
                        print(i, j)

                        self.sock_server.sendto(str( {"TYPE" : "sendAgree", "data" : self.ID, "TX" : tmp_tx.to_dict(),  "Hash" : tmp_Hash} ).encode(), j)
                        data, addr = self.sock_server.recvfrom(1024*1024)
                        data = data.decode()
                        print(data)
                        time.sleep(0.1)

        
                        pass
                else:            
                    print("합의 요청 받음")
                    print(type(addr),addr)
                    print("argv :", type(argv))

                    dataHash = argv['Hash']
                    tx = maketx(argv["TX"])
                    txdata = tx.to_dict()

                    aa = str(len(argv["TX"])) == str(len(txdata))
                    bb = len(argv["TX"]) == len(txdata)
                    result = aa and bb
                    print("Match :", result)

                    self.sock_server.sendto(str(result).encode(), addr)


                pass

            
            except Exception as e:
                print("class P2PServer def run Exception")
                print(e)                
        return

    def stop(self):
        self.running = False
        return

# 로컬 명령어를 Queue에서 받아와 수행하는 루틴
class P2PHandler(threading.Thread): # client
    def __init__(self, Queue, ID):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.Q = Queue
        self.status = False
        self.ID = ID
        self.sock_server = self.Q.get()
        self.serverAddr = ("192.168.0.5", 14101)
        
        print("Handler :", self.sock_server)
        return 

    def run(self):
        while self.running:
            try:
                print('log : queue server start')
                data, addr, sock = self.Q.get()
                
                # addr == self.ID 이면 합의 요청
                # else 합의 요청 반환

                if addr == self.ID:
                    print("합의 요청, ipList 받아오기")
                    self.sock_server.sendto(str({"TYPE" : "giveIpList", "ID" : self.ID}).encode(), self.serverAddr)
                    TX_Q.put(data)
                    

                    



            except Exception as e:
                print(e)
        return

    def stop(self):
        print("log : P2PHandler end")
        self.running = False
        
def P2P(argv, addr, sock):

    while True:
        data, addr = sock.recvfrom(1024)
        print('서버에게 받음 : {} {}'.format(addr, data))
        addr = ast.literal_eval(data.decode())
        if type(addr) == type(list()):
            for i in addr:
                print(type(i), i)
                sock.sendto(b'111111111111', i)

        else:
            print(type(addr),addr)


# 명령어를 받아들이는 소켓 서버 localhost
class EventServer(threading.Thread): # server
    def __init__(self, Queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.Q = Queue

        self.HOST = 'localhost'
        self.PORT = 14101
        return

    def run(self):
        while self.running:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print('log : local server start', (self.HOST, self.PORT))
                s.bind((self.HOST, self.PORT))
                s.listen(0)
                conn, addr = s.accept()
                argv = conn.recv(1024*1024).decode()
                argv = ast.literal_eval(argv)
                
                self.Q.put(argv)            
        return

    def stop(self):
        self.running = False
        return


class sendAgree(threading.Thread):
    def __init__(self, ID):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.ID = ID
        return 

    def run(self, tx):
        try:
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            HOST = "chgoyang.iptime.org"
            #HOST = "192.168.0.38"
            PORT = 14101
            sock.sendto(str( {"TYPE" : "giveIpList", "ID" : self.ID} ).encode(), (HOST, PORT))

            ipList, addr = sock.recvfrom(1024*1024)
            ipList = ast.literal_eval(ipList.decode())
            print(ipList)
            agreeResult = []


            for ID, addr in ipList:
                print("보내기 준비", len(str(tx)), ID, addr)
                sock.sendto("send ready".encode(), addr)
                print("원장 보내기")
                data = str(tx)
                while data:
                    sock.sendto(data[:4096].encode(), addr)
                    data = data[4096:]
                    print(len(data))
                    pass
                sock.sendto("send end".encode(), addr)
                print("합의 결과 받기")
                result, addr = sock.recvfrom(1024)
                print("결과 저장", result.decode())
                agreeResult.append(ast.literal_eval(result.decode()))
                print("다음.")
                pass

            print(ipList, type(ipList))


        except Exception as e:
            print("class P2PHandler def sendAgree Exception :", e)
        return False
    
    def stop(self):
        print("log : sendAgree end")
        self.running = False


class recvAgree(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        return 

    def run(self, argv, sock):
        try:
            data, addr = sock.recvfrom(int(data.decode()))
            data = ast.literal_eval(data.decode())
            recvTX = ""
            if data == "send ready":
                print("log : 받을 준비 완료")
                while True:
                    data, addr = sock.recvfrom(4096)
                    if data.decode() == "send end":
                        break
                    recvTX = recvTX + data.decode()

            print("end recv, start hashing", len(recvTX))
            sock.sendto("True".encode(), addr)


        except Exception as e:
            print("class P2PHandler def recvAgree Exception :", e)
        return False
    
    def stop(self):
        print("log : sendAgree end")
        self.running = False


if __name__ == '__main__':
    try:
        threads = []
        Q = queue.Queue()

        #threads.append(EventServer(Q))
        threads.append(P2PHandler(Q, "testID2"))
        threads.append(P2PServer(Q, "testID2"))
        

        for i in threads:
            print('start', i)
            i.start()

        time.sleep(60*60*24)
        
    except Exception as e:
        print('Exception')
        for i in threads:
            i.stop()
        print(e)
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        for i in threads:
            i.stop()
    except :
        print('Any Interrupt')
        for i in threads:
            i.stop()
    else:
        print('else')
        for i in threads:
            i.stop()
    print('feild end')
        