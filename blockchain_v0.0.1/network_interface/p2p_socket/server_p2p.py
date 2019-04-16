
# This Python file uses the following encoding: utf-8

import logging
import socket
import threading, queue
import sys, os, ast, time, random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))

'''
logger = logging.getLogger()

def p2p(ID = ''):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = HOST
    sock.sendto(str(ID).encode(), (HOST, 9999))

    data, addr = sock.recvfrom(1024)
    print('client received: {} {}'.format(addr, data))
    addr = ast.literal_eval(data.decode())
    #file = open('2019학사일정.pdf', 'rb').read()
    file = "11111111\n-----".encode('utf-8')
    sock.sendto(file, addr)
    data, addr = sock.recvfrom(1024)
    print('client received: {} {}'.format(addr, data))

if __name__ == '__main__1':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    p2p("id00125")
'''

class P2PServer(threading.Thread):
    def __init__(self, Queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.Q = Queue
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.HOST = "chgoyang.iptime.org"
        self.HOST = "localhost"
        self.PORT = 14101
        self.sock.sendto(str( {"TYPE" : "first connect", "ID" : "id00124"} ).encode(), (self.HOST, self.PORT))
        return

    def run(self):
        while self.running:
            try:
                print('log : P2P server start', (self.HOST, self.PORT))
                argv = self.sock.recvfrom(1024)
                argv = ast.literal_evel(argv)
                self.Q.put(argv)
                pass

            
            except Excpetion as e:
                self.sock.sendto("first connect".encode(), (self.HOST, self.PORT))
                print(e)                
        return

    def stop(self):
        self.running = False
        return


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

# 로컬 명령어를 Queue에서 받아와 수행하는 루틴
class EventHandler(threading.Thread): # client
    def __init__(self, Queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.Q = Queue
        self.status = False
        
        return 

    def run(self):
        print('log : queue server start')
        while self.running:
            try:
                argv = Q.get()
                if not type(argv) == type(dict()):
                    continue
                
                if "TYPE" in argv:
                    if argv['TYPE'] == 'first connect':
                        self.first_connenct(argv)

                if not self.status:
                    continue

                
            except Exception as e:
                print(e)
        return

    def first_connect(self, argv):
        self.status = True

    

    def stop(self):
        print("log : eventHandler end")
        self.running = False

if __name__ == '__main__':
    try:
        threads = []
        Q = queue.Queue()

        threads.append(EventServer(Q))
        threads.append(EventHandler(Q))
        threads.append(P2PServer(Q))
        

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
        