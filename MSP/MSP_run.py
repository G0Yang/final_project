# This Python file uses the following encoding: utf-8

import threading, time
import sys, os
import queue

from login_server import *


Q = queue.Queue()



def main(argv):
    
    threads = []
    
    threads.append()
    threads.append()

    for i in threads:
        i.start()


    print("main end")

    return threads

if __name__ == "__main__":
    thread = []
    try:
        thread = main(sys.argv)
        while True:
            time.sleep(10)
    except Exception as e:
        print('Exception')
        for i in thread:
            i.stop()
        print(e)
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        for i in thread:
            i.stop()
    except :
        print('Any Interrupt')
        for i in thread:
            i.stop()
    else:
        print('else')
        for i in thread:
            i.stop()
    print('feild end')
        