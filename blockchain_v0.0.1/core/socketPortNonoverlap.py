# This Python file uses the following encoding: utf-8

import random, time

portList = []

# 49152 ~ 65535

def listappend(portList = []):
    print('init')
    port = random.randint(49152, 65535)
    #port = random.randint(0, 15)
    if not port in portList:
        return port
    return listappend(portList = portList)

if __name__ == '__main__':
    for i in range(0,10):
        num = listappend(portList = portList)
        print(num)
        portList.append(num)
        print(portList)