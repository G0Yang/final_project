# This Python file uses the following encoding: utf-8

import socket
import queue
import threading
import sys, os
import ast
import time

from couchDBHandler import *

Q_event = queue.Queue()


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    return s.getsockname()[0]


def eventPaser(argv):
    return argv

class EventServer(threading.Thread): # server
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.HOST = getIP()
        self.PORT = 14005   
        print(self.HOST, self.PORT)
        return

    def run(self):
        while self.running:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print('server start')
                s.bind((self.HOST, self.PORT))
                s.listen(0)
                conn, addr = s.accept()
                argv = conn.recv(1024*1024).decode()
                argv = ast.literal_eval(argv)
                Q_event.put((argv, conn, addr))
        return

    def stop(self):
        self.running = False
        return

class EventHandler(threading.Thread): # client
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.ID = 'admin'
        self.PW = 'admin'
        self.server = runServer("localhost", "5984", self.ID, self.PW)

        return 

    def run(self):
        try:
            print('queue server start')
            while self.running:
                argv, conn, addr = Q_event.get()
                print('queue server', argv)
                result = eventPaser(argv)
                conn.sendall(str(result).encode())
                pass
        except:
            pass
        return

    def stop(self):
        print("eventHandler end")
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
        
    except Exception as e:
        print(e)
        for i in threads:
            i.stop()
            print('stop', i)

