# This Python file uses the following encoding: utf-8

import grpc, json, ast, time

import foodchain_pb2
import foodchain_pb2_grpc

#from function import transaction

def main_grpc_client(IP = 'localhost', PORT = 50051):
    try:
        
        time1 = time.time()

        host = IP + ':' + str(PORT)

        channel = grpc.insecure_channel(host)

        stub = foodchain_pb2_grpc.MaketxStub(channel)

        data = str({
            'TXID' : "123",
            'name' : 'kim'
            }
            )

        data = foodchain_pb2.Transaction(data=data)

        response = stub.maketx(data)

        response = ast.literal_eval(response.data)

        print(type(response), response)

        time2 = time.time()

        print(time2-time1)

    except Exception as e:
        print(e)
    return

if __name__ == '__main__':
    while True:
        main_grpc_client()