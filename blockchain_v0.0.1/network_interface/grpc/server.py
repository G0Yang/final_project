# This Python file uses the following encoding: utf-8

import grpc
import time, json, ast, sys, os
from concurrent import futures

sys.path.append(os.path.dirname(__file__))

import foodchain_pb2
import foodchain_pb2_grpc


class MaketxServicer(foodchain_pb2_grpc.MaketxServicer):
    def maketx(self, request, context):
        try:
            response = foodchain_pb2.Transaction()

            print(type(request.data), request.data)
            
            js = ast.literal_eval(request.data)

            print(type(js), js)

            response.data = str(js)
        except Exception as e:
            print(e)
        return response

def main_grpc_server(PORT = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    foodchain_pb2_grpc.add_MaketxServicer_to_server(MaketxServicer(), server)

    print('Starting server. Listening on port ' + str(PORT) + '.')
    server.add_insecure_port('[::]:'+str(PORT))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

    return

if __name__ == '__main__':
    main_grpc_server()