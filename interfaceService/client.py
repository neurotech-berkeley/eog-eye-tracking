import grpc
import device_pb2 as pb
import device_pb2_grpc as pb_grpc
from enum import Enum

FILEPATH = ""

class Direction(Enum):
    CENTER = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def window(data):
   # TODO: write function to filter and window the data read in from bluetooth
   return data

def read(filepath):
   # TODO: write function to read data from bluetooth
   data = [1, 2, 3, 4, 5, 6] # dummy data
   out = window(data)
   return out

with grpc.insecure_channel("localhost:50051") as ch:
  stub = pb_grpc.EogSignalServiceStub(ch)
  data = read(FILEPATH)
  req = pb.EogClientRequest(deviceId="001", data=data)
  res = stub.Classify(req)
  print("request sent...")


  print("Received (ID): " + res.deviceId)
  print("Received (direction): " + str(res.direction) + ", " + str(Direction(res.direction)))
