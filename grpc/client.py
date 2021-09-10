"""Docs https://grpc.io/docs/languages/python/quickstart/
Generate protos

"""

import grpc
import proto


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = proto.helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(proto.helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)
    response = stub.SayHelloAgain(proto.helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
