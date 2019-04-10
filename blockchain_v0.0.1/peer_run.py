# This Python file uses the following encoding: utf-8

# >> python run.py init -ID=ender35841 -PW=drgf35841
# >> login success
# >> chain_init
# >> init complete
# >> start Queue Daemon
# >> start eventSelector
# >> client init complete

# >> python event.py -type=upschedule -filename=2019학사일정.pdf
# >> eventSelector run
# >> event type : upschedule
# >> filename : 2019학사일정pdf
# >> file load done
# >> input queue done
# >> eventHandler run
# >> event type : upschedule
# >> file upload done
# >> event complete

import threading, time
import sys, os
import queue

from network_interface.event_socket.server_event import EventServer, EventHandler

Q = queue.Queue()

def chain_init(contractList = []):
    contract_list = []
    for i in contractList:
        contract_list.append(findContract(i))

    for i in contract_list:
        if not i:
            contract_list.remove(i)

    if len(contract_list) == 0:
        return False

    return contract_list

def main(argv):
    threads = []
    
    threads.append(EventServer())
    threads.append(EventHandler())

    for i in threads:
        i.start()

    return threads

if __name__ == "__main__":
    threads = []
    try:
        threads = main(sys.argv)
        while True:
            time.sleep(10)
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
        