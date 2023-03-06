# import statements
import grpc
import example_pb2 as pb
import example_pb2_grpc as pb_grpc

from concurrent import futures

# define servicer (not implemented in grpc generate protocol buffer)
class HelloServiceServicer(pb_grpc.HelloServiceServicer):
    def HelloWorld(self, request, context):
        print("Request received")
        print(request.text + " " + request.name)
        reply = str(int(request.text) * int(request.name))
        res = pb.HelloWorldResponse(text = reply)
        return res



def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 100000000),
            ("grpc.max_receive_message_length", 100000000),
        ],
    )
    pb_grpc.add_HelloServiceServicer_to_server(
		HelloServiceServicer(), server
	)
    server.add_insecure_port('[::]:50051')
    print("server is running!");
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
	serve()

