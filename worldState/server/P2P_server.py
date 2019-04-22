import logging
import socket
import threading, queue
import sys, os, ast, time, random

logger = logging.getLogger()
addresses = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

# 오더링을 수행할 ip 갯수를 랜덤으로 추출하여 순번을 정해서 리스트로 반환
def makeOrderingList(hostNumder = 0):
    if not type(hostNumder) == type(int()):
        try:
            print("int가 아님")
            hostNumder = int(hostNumder)
        except:
            print("int 변환 실패")
            return False
    if hostNumder > 20:
        hostNumder = 20
    orderingList = []
    while len(orderingList) < (hostNumder-1)/2:
        num = random.randint(0, hostNumder)
        if num not in orderingList:
            orderingList.append(num)
    orderingList.sort()
    return orderingList

# 전체 리스트에서 오더링할 ip리스트를 반환
def orderingBindList(bindList, IP):
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
        if not bindList[i][1][0] == IP:
            orderingList.append(bindList[i])

    if not len(orderingList) == len(countList):
        return False

    return orderingList

'''
def main(host='192.168.0.12', port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    
    host = HOST
    print(host, port)
    sock.bind((host, port))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = data.decode()
        logger.info("connection from: %s, data : %s", addr, data)
        addresses.append(addr)
        if len(addresses) == 5:
            List = orderingBindList(addresses)
            print(List)
        if len(addresses) >= 2:
            logger.info("server - send client info to: %s", addresses[0])
            sock.sendto(str(addresses[1]).encode(), addresses[0])
            logger.info("server - send client info to: %s", addresses[0])
            sock.sendto(str(addresses[0]).encode(), addresses[1])
            addresses.pop(1)
            addresses.pop(0)
    return
'''  
            
# 외부 접속용 ip 서버 - ipList 반환 전용
class P2PServer(threading.Thread): # server
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True

        self.Q = Q
        

        self.HOST = s.getsockname()[0]
        self.PORT = 14102
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
                
                    self.Q.put((str(self.HOST), conn, addr, argv))
            except Exception as e:
                print(e)

        return

    def stop(self):
        print('databaseServer END')
        self.running = False



# P2P 서버
class P2PHandler(threading.Thread): # client
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.Q = Q
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.HOST = s.getsockname()[0]
        self.PORT = 14101

        self.sock.bind((self.HOST, self.PORT))
        
        self.ipList = []
        print(self.HOST, self.PORT)

        
        return 

    def run(self):
        print('log : queue server start')
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                data = data.decode()
                data = ast.literal_eval(data)
                print("받은 데이터 :", type(data), data)
                print("받은 연결 :", type(addr), addr)

                if "TYPE" in data:
                    print("이벤트 처리", type(data['TYPE']), data['TYPE'])
                    if data['TYPE'] == 'first connect':
                        print("log : ipList append")
                        self.appendAddr(data['ID'], addr)

                        #self.sock.sendto(str(addr).encode(), addr)

                        print(self.ipList)
                        continue

                    if data['TYPE'] == "giveIpList":
                        print("log : return ipList")
                        orderingList = orderingBindList(self.ipList, data['ID'])
                        self.sock.sendto(str(orderingList).encode(), addr)
                        continue
                
            except Exception as e:
                self.sock.bind((self.HOST, self.PORT))
                print(e)
        return

    # 노드의 로그아웃 요청시 ipList에서 노드의 정보를 제거함
    def delipList(self):
        return

    # ID 중복없이 ipList에 ID, addr 정보를 추가함
    def appendAddr(self, ID, addr):
        F_input = False
        for i in range(0, len(self.ipList)):
            if ID == self.ipList[i][0]:
                del self.ipList[i]
                self.ipList.append((ID, addr))
                F_input = True
                break

        if not F_input:
            self.ipList.append((ID, addr))
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
        print("start Thread")

        threads.append(P2PHandler(Q))

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
        

    '''
    print(random.randint(1,1000))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main(sys.argv)
    '''
