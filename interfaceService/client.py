import grpc
import example_pb2 as pb
import example_pb2_grpc as pb_grpc

with grpc.insecure_channel("localhost:50051") as ch:
  stub = pb_grpc.HelloServiceStub(ch)
  num1 = input("number 1: ")
  num2 = input("number 2: ")
  req = pb.HelloWorldRequest(text=num1, name=num2)
  res = stub.HelloWorld(req)

  print("Received: " + res.text)
