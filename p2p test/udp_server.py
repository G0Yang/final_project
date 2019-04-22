import logging
import socket
import sys

logger = logging.getLogger()
addresses = []


def main(host='192.168.137.254', port=9999):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((host, port))
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        logger.info("요청 받음 : %s", addr)
        addresses.append(addr)
        if len(addresses) >= 4:
            sock.sendto(str(addresses).encode(), addr)


            '''
            logger.info("%s 에게 %s 의 정보를 보냄.", addresses[0], addresses[1])
            sock.sendto(str(addresses[1]).encode(), addresses[0])
            
            logger.info("%s 에게 %s 의 정보를 보냄.", addresses[1], addresses[0])
            sock.sendto(str(addresses[0]).encode(), addresses[1])
            addresses.pop(1)
            addresses.pop(0)
            '''



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()
