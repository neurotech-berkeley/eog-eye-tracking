# import statements
import grpc
import device_pb2 as pb
import device_pb2_grpc as pb_grpc

from concurrent import futures

# define servicer (not implemented in grpc generate protocol buffer)
class EogSignalServiceServicer(pb_grpc.EogSignalServiceServicer):
    def Classify(self, request, context):
        print("Request received")
        print (request.deviceId)
        print (request.data)
        classification = request.data[0]
        # TODO: write the classification algorithm here. 
        # request.data will come in 
        res = pb.EogServerResponse(deviceId = request.deviceId, direction = classification)
        return res



def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 100000000),
            ("grpc.max_receive_message_length", 100000000),
        ],
    )
    pb_grpc.add_EogSignalServiceServicer_to_server(
		EogSignalServiceServicer(), server
	)
    server.add_insecure_port('[::]:50051')
    print("server is running!")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
	serve()

