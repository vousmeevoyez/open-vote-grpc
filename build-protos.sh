#!/bin/sh
# to generate GRPC client & server code
python -m grpc_tools.protoc -I protos/ --python_out=src/autogen/ --grpc_python_out=src/autogen/ protos/*.proto
