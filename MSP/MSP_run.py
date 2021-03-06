# This Python file uses the following encoding: utf-8

# WS run.py

import threading, time
import sys, os
import queue

from server.MSP_server import memberShipHandler, memberShipServer

Q = queue.Queue()

# 여기에서 큐를 사용하는 이유는 작업간의 원자성을 유지하기 위함이다.
# 큐를 사용하지 않고 각 서버가 독립적으로 사용한다면, DB를 사용함에 있어서 각 트랜잭션이 수행 속도에 따라 값이 달라질 염려가 있다.
# 큐는 내부 명령과 외부에서 오는 명령을 하나의 처리 프로세스로 뭉치게 만들어 DB에 접근하는 순서를 꼬이지 않도록 한다.



if __name__ == "__main__":
    try:
        print("MSP_run.py")
        threads = []
    
        threads.append(memberShipHandler(Q)) # 명령어 처리를 위한 Queue호출 및 순환 루틴
        threads.append(memberShipServer(Q)) # 외부 접속용 ip 서버

        for i in threads:
            i.start()


        print("main end")
        while True:
            time.sleep(10)
    except Exception as e:
        print('Exception', e)
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
        
