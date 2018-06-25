from concurrent import futures
import time
import grpc

import dsid_pb2
import dsid_pb2_grpc

import server_log
logger = server_log.setup_custom_logger('root')

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def format_object_to_string(user):
    return "name: %s, lastname: %s, age: %s, nUSP: %s" % (user.name, user.lastname, user.age, user.nUSP);

class DSIDServer(dsid_pb2_grpc.DSIDServicer):

    def SendsVoidResponse(self, request, context):
        logger.info("Sending server Void response")
        return dsid_pb2.VoidReply()

    def SendsLongResponse(self, request, context):
        long_response = 12345678988881011
        logger.info("Sending server Long response. Value: " + str(long_response))
        return dsid_pb2.LongReply(message=long_response)

    def SendsStringResponse(self, request, context):
        logger.info("Sending server String response. Value: A" )
        return dsid_pb2.StringReply(message=request.message)

    def SendsObjectResponse(self, request, context):
        user = dsid_pb2.User()
        user.name = "Laura"
        user.lastname = "Vieira"
        user.age = 23
        user.nUSP = 1234567
        logger.info("Sending server Object response. Value: " + format_object_to_string(user))
        return dsid_pb2.ObjectReply(message=user)
        logger.info("\n \n")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dsid_pb2_grpc.add_DSIDServicer_to_server(DSIDServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
