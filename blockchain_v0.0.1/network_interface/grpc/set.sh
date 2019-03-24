#!bin/bash

#python -m pip install grpcio grpcio-tools

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. foodchain.proto