build-protos:
	python -m grpc_tools.protoc -I protos/ --python_out=src/autogen/ --grpc_python_out=src/autogen/ protos/*.proto

build-container:
	docker build -t open-vote-grpc .

secret:
	openssl req -newkey rsa:2048 -nodes -keyout secrets/server.key -x509 -days 365 -out secrets/server.crt
