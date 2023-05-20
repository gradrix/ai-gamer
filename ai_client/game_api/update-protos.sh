#!/bin/bash

sudo apt update && sudo apt install protobuf-compiler golang-goprotobuf-dev

go get google.golang.org/grpc/cmd/protoc-gen-go-grpc
go get google.golang.org/protobuf/cmd/protoc-gen-go

go install google.golang.org/grpc/cmd/protoc-gen-go-grpc
go install google.golang.org/protobuf/cmd/protoc-gen-go

protoc --go_out=../ --go-grpc_out=../ --proto_path=../../common/rpc ../../common/rpc/gameapi.proto