import logging
import socket
import sys, ast

logger = logging.getLogger()

def main(host='chgoyang.iptime.org', port=9999):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.sendto(b'00000', (host, port))
    
    '''
    data, addr = sock.recvfrom(1024)
    data = ast.literal_eval(data.decode())
    print(type(data), data)
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", data))
    sock.sendto(b'', (host, port))
    '''
    
    print(sock)

    while True:
        print("대기")
        data, addr = sock.recvfrom(1024)
        print('서버에게 받음 : {} {}'.format(addr, data))
        data = ast.literal_eval(data.decode())
        if type(data) == type(list()):
            addr = data
            for i in addr:
                print(type(i), i)
                sock.sendto(b'44444', ("0.0.0.0", i[1]))
                data, addr = sock.recvfrom(4096)
                data = data.decode()
                print(data)

        else:
            
            print(type(addr),addr)
            sock.sendto(str("잘 받44444").encode(), addr)
            


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()
