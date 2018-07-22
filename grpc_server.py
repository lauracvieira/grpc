from concurrent import futures

import time
import grpc

import dsid_pb2
import dsid_pb2_grpc
import random

smallStringResponse = "x5cHKQWH0Vsou5Ej"
bigStringResponse = "xo6TV5sSIHSSVeMvna5YPhuIjgBpIj9RG5u6j5QVPMgnUKDSfoL2YIjDoXmcQjeAknfRg03qc83Xo2npjEbyvDcQIlMgjJpuO91SC3wArcM7nnfvghSJROecz49hmCXNNGlTZ4gTEtT2kt1RN7GyjLBivIvXI2fFsr6HkHRiaskSzdgVPBbwTpSJ0Bbq8fiKWbZfqMmBqGqDrqHoAYIFGg3FCMnRzeBp8t4RM0J1pASiys5WCXdc9p2QEP8aqXjjCbgCMqRfufdWFewowKtlIDdSZmPARA0F4UwFDkD11J4T7eSrCbp3Ml6CG8Hoy1k7x9bcXrxBhpLE5yW9xxQdclrQYu1IVSTks8m5XSWbapMIFoq0lvgjuNWiXLz5vTyiHeOTheiBMstjK7SXNlW9zXEALeaX4m2XuMnIoDawEt8Xl5R7wNAhDiFW8nHdFUxBlyizSaOUHHtmz5ayaomemxoiiurQkOdalHiLj7sdZCevMtHwuAiehGcvmOWRnGm89sg8vlwI7Tsiizrgio84LGkYh9zAkzKwqdo5INixJzsjdMRmfU3Q1ZzxYItlKPcBv3r52wnJv5bq6dHVMUFciuc7B8p4jLp6wUectpi9XcuPFE21y1U8aSb99nAA7sy7uOgu14KUJALwNTiXBLT61QcxzsjQvmCXyHaFShSzDELOrV6LT2kjRszC5zy5lG9t2sad1Cg5BAxLfwQCBHCBBLwnjuqCaTxBABVRjJYGQGqMcoHQdU9pgjmzgWsZQZA8gDq2GTDDG8LEnDVQvXURjc7PI5MmmlkAlv44N65gIUKB87uSiTGHrLYG4CGKlgMW1LTEmGTJQousjed8bcmHnes02lClyOJtB4613annnKs2OHbAXnpeRatka81j4aGejhkazQolSNtHbSRkL1voLjyQXzcC1tTfczAVn0jZOM4c2dBanCY4XMtbTuJjwfgawySH6nqEmX7j8zcq4PMevnzRP1Hww50OQK4xwKdb8QyXurXS8blHt2lM7ZzH7zBN"
longResponse = 12345678988881011

objectResponse = dsid_pb2.Object()
objectResponse.longAttr = longResponse
objectResponse.stringAttr = smallStringResponse
objectResponse.booleanAttr = False

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GRPCServer(dsid_pb2_grpc.GRPCServicer):

    def VoidRequestVoid(self, request, context):
        print("VoidRequestVoid")
        return dsid_pb2.VoidResponse()

    def VoidRequestBigString(self, request, context):
        print("VoidRequestBigString")
        return dsid_pb2.StringResponse(response=bigStringResponse + str(random.randint(0, 9)))

    def StringRequestSameString(self, request, context):
        print("StringRequestSameString")
        return dsid_pb2.StringResponse(response=request.parameter + str(random.randint(0, 9)))

    def StringRequestBigString(self, request, context):
        print("StringRequestBigString")
        return dsid_pb2.StringResponse(response=bigStringResponse + str(random.randint(0, 9)))

    def LongRequestLong(self, request, context):
        print("LongRequestLong")
        return dsid_pb2.LongResponse(response=longResponse + random.randint(0, 9))

    def EightLongRequestLong(self, request, context):
        print("EightLongRequestLong")
        return dsid_pb2.LongResponse(response=longResponse + random.randint(0, 9))

    def LongListRequestLong(self, request, context):
        print("LongArrayRequestLong")
        return dsid_pb2.LongResponse(response=longResponse + random.randint(0, 9))

    def LongRequestObject(self, request, context):
        print("LongRequestObject")
        return dsid_pb2.ObjectResponse(response=objectResponse)

    def ObjectRequestLong(self, request, context):
        print("ObjectRequestLong")
        return dsid_pb2.LongResponse(response=longResponse + random.randint(0, 9))

    def ObjectRequestObject(self, request, context):
        print("ObjectRequestObject")
        return dsid_pb2.ObjectResponse(response=objectResponse)

    def BigIntegerList(self, request, context):
        print("IntegerListRequestMethod")
        return dsid_pb2.VoidResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dsid_pb2_grpc.add_GRPCServicer_to_server(GRPCServer(), server)
    server.add_insecure_port('[::]:8001')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    print('Starting the server...')
    serve()
    print('done.')
