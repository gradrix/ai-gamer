#!/bin/bash

python -m grpc_tools.protoc -I ./rpc --python_out=./rpc/ --grpc_python_out=./rpc/ ./rpc/gameapi.proto
