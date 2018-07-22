from __future__ import print_function

import dsid_pb2
import dsid_pb2_grpc
import log

import grpc

import time
import numpy as np

from sys import getsizeof

logger = log.setup_custom_logger('grpc_client_python')

_STRINGS_TO_TEST = {
    1: "a",
    2: "ab",
    4: "abcd",
    8: "abcdefgh",
    16: "x5cHKQWH0Vsou5Ej",
    32: "xv1lWaeDWxn48TTVEjMFeam74Dj7xaeB",
    64: "VPh1NLqEa80CUurgztYQawE0D6uJWuwqZK8hxrpxflfbkRb3MnoPqAhWFkgLd41p",
    128: "so5aM6kdJb7a9EYKgDtDbWgmW59pU3sQ6TnNjVtRFUVQiHLUNlPfGRbu2tEUnmMuASpmNOr0WnhzYwePiYe594n2eFqAA22jidu85wAz8wwR74PLHOg1412fojP98KcA",
    256: "uMfPDBeBAtELNFnYcAi4JFwST5OyaoJergMCzuueIbWGLlFXYwUPTW3EA7h9EghKSoWVfL2497Rqg3Hx8TCmKU9aAvWwS9FFfwTiMA0B33IqyvTLfj3Gj65jZolhTIv0dJS1YWxWQRNa6kwHyTLvhfThzOpgp5p4aYR1gR30UfdrKCc29EWF9qseIoJirHE9ju7N140Zw8wx4jRIPhC5Vx5JhxPCbarBSTvc1DSTXKzpxA2dEtpWEIIeWMjWGFnF",
    512: "w1E0dYaHTXJrR0rEn5pEQJgi0OqWPY4G72P8P7C2b6Pey0MnDGlretB7jZxxvjVKIB0H6C3DYQvzK10NhOxYONT0QfktCGIo40wXR8tyY2GUpVEH72VZEzLAmYnvgTbVo6ggJ2faKH0eNs73jtGBY2BD8ErhWwelevxsZfkjRqaA7CzyARK6MROfJEbkSf0TZUyGfl5RZhDQFRhOO9spsTLFHOq3wVUdOku9KGGDeTituLEzUjruNdpQ1oc7g29lD5QW0CDK7o3wD8NkcxVll1LgQMzd5105S6p3fpuiJLBWtd8GeFPm7chv1U1BZPhEQF6jdvymSYt7wDYltpt7HhxoHKpuc68eHljAsKH7noAtNYKJZuRCE5LbBUcMz4EX5N311a16zATLOZayiF1F042hpR0UJdcMkBA1f0kQMTRG7nnoTIEk5PLQrubmuwIdLixNxk6sXQMFmGPFolNQDWBPISd76RkiysoK8Ak1By0tuAu79kSEqfM6OWFAkEyZ",
    1024: "xo6TV5sSIHSSVeMvna5YPhuIjgBpIj9RG5u6j5QVPMgnUKDSfoL2YIjDoXmcQjeAknfRg03qc83Xo2npjEbyvDcQIlMgjJpuO91SC3wArcM7nnfvghSJROecz49hmCXNNGlTZ4gTEtT2kt1RN7GyjLBivIvXI2fFsr6HkHRiaskSzdgVPBbwTpSJ0Bbq8fiKWbZfqMmBqGqDrqHoAYIFGg3FCMnRzeBp8t4RM0J1pASiys5WCXdc9p2QEP8aqXjjCbgCMqRfufdWFewowKtlIDdSZmPARA0F4UwFDkD11J4T7eSrCbp3Ml6CG8Hoy1k7x9bcXrxBhpLE5yW9xxQdclrQYu1IVSTks8m5XSWbapMIFoq0lvgjuNWiXLz5vTyiHeOTheiBMstjK7SXNlW9zXEALeaX4m2XuMnIoDawEt8Xl5R7wNAhDiFW8nHdFUxBlyizSaOUHHtmz5ayaomemxoiiurQkOdalHiLj7sdZCevMtHwuAiehGcvmOWRnGm89sg8vlwI7Tsiizrgio84LGkYh9zAkzKwqdo5INixJzsjdMRmfU3Q1ZzxYItlKPcBv3r52wnJv5bq6dHVMUFciuc7B8p4jLp6wUectpi9XcuPFE21y1U8aSb99nAA7sy7uOgu14KUJALwNTiXBLT61QcxzsjQvmCXyHaFShSzDELOrV6LT2kjRszC5zy5lG9t2sad1Cg5BAxLfwQCBHCBBLwnjuqCaTxBABVRjJYGQGqMcoHQdU9pgjmzgWsZQZA8gDq2GTDDG8LEnDVQvXURjc7PI5MmmlkAlv44N65gIUKB87uSiTGHrLYG4CGKlgMW1LTEmGTJQousjed8bcmHnes02lClyOJtB4613annnKs2OHbAXnpeRatka81j4aGejhkazQolSNtHbSRkL1voLjyQXzcC1tTfczAVn0jZOM4c2dBanCY4XMtbTuJjwfgawySH6nqEmX7j8zcq4PMevnzRP1Hww50OQK4xwKdb8QyXurXS8blHt2lM7ZzH7zBN"
}

longParameter = 12345678988881011

numIterations = 50
objectParameter = dsid_pb2.Object()
objectParameter.longAttr = longParameter
objectParameter.stringAttr = _STRINGS_TO_TEST[16]
objectParameter.booleanAttr = False

rangesForBigRequest = [10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]


time_list = []
long_list = [longParameter, longParameter, longParameter, longParameter, longParameter, longParameter, longParameter,
             longParameter]

address = "localhost:8001"

def run():
    logger.info(
        "Type of parameter | Size of parameter in bytes | Type of response | Size of response in bytes | average time in milliseconds | standard deviation | min time | max time | number of iterations: " + str(
            numIterations))

    
    # VoidRequestVoid
    for i in range(numIterations):
        start = time.time() * 1000
        channel = grpc.insecure_channel(address)
        stub = dsid_pb2_grpc.GRPCStub(channel)
        stub.VoidRequestVoid(dsid_pb2.VoidRequest())
        end = time.time() * 1000
        time_list.append(end - start)
    printResults("Void", 0, "Void", 0)

    # VoidRequestBigString
    for i in range(numIterations):
        start = time.time() * 1000
        channel = grpc.insecure_channel(address)
        stub = dsid_pb2_grpc.GRPCStub(channel)
        response = stub.VoidRequestBigString(dsid_pb2.VoidRequest())
        end = time.time() * 1000
        time_list.append(end - start)
    printResults("Void", 0, "String 1024 characters", getsizeof(response.response))

    # StringRequestSameString
    for key in _STRINGS_TO_TEST:
        for i in range(numIterations):
            start = time.time() * 1000
            channel = grpc.insecure_channel(address)
            stub = dsid_pb2_grpc.GRPCStub(channel)
            response = stub.StringRequestSameString(dsid_pb2.StringRequest(parameter=_STRINGS_TO_TEST[key]))
            end = time.time() * 1000
            time_list.append(end - start)
        printResults("String " + str(key) + " characters", getsizeof(_STRINGS_TO_TEST[key]), "Same String " + str(key) + " characters",
            getsizeof(response.response))
    
    # StringRequestBigString
    for key in _STRINGS_TO_TEST:
        for i in range(numIterations):
            start = time.time() * 1000
            channel = grpc.insecure_channel(address)
            stub = dsid_pb2_grpc.GRPCStub(channel)
            response = stub.StringRequestBigString(dsid_pb2.StringRequest(parameter=_STRINGS_TO_TEST[key]))
            end = time.time() * 1000
            time_list.append(end - start)
        printResults("String " + str(key) + " characters", getsizeof(getsizeof(_STRINGS_TO_TEST[key])), "Big String 1024 characters",
            getsizeof(response.response))

    # LongRequestLong
    for i in range(numIterations):
        start = time.time() * 1000
        channel = grpc.insecure_channel(address)
        stub = dsid_pb2_grpc.GRPCStub(channel)
        response = stub.LongRequestLong(dsid_pb2.LongRequest(parameter=longParameter))
        end = time.time() * 1000
        time_list.append(end - start)
    printResults("Long", getsizeof(longParameter) * 8, "Long", getsizeof(response.response))

    # EightLongRequestLong
    for i in range(numIterations):
        start = time.time() * 1000
        channel = grpc.insecure_channel(address)
        stub = dsid_pb2_grpc.GRPCStub(channel)
        response = stub.EightLongRequestLong(
            dsid_pb2.EightLongRequest(parameter1=longParameter, parameter2=longParameter, parameter3=longParameter,
                                      parameter4=longParameter, parameter5=longParameter, parameter6=longParameter,
                                      parameter7=longParameter, parameter8=longParameter))
        end = time.time() * 1000
        time_list.append(end - start)
    printResults("8 Long Parameters", getsizeof(longParameter) * 8, "Long", getsizeof(response.response))

    # LongListRequestLong
    for i in range(numIterations):
        start = time.time() * 1000
        response = stub.LongListRequestLong(dsid_pb2.LongListRequest(parameter=long_list))
        end = time.time() * 1000
        time_list.append(end - start)
    printResults("8 Long in List", getsizeof(long_list), "Long", getsizeof(response.response))

    # LongRequestObject
    for i in range(numIterations):
        start = time.time() * 1000
        response = stub.LongRequestObject(dsid_pb2.LongRequest(parameter=longParameter))
        end = time.time() * 1000
        time_list.append(end - start)
    printResults("Long", getsizeof(longParameter), "Object", getsizeof(response.response))

    # ObjectRequestLong
    for i in range(numIterations):
        start = time.time() * 1000
        response = stub.ObjectRequestLong(dsid_pb2.ObjectRequest(parameter=objectParameter))
        end = time.time() * 1000
        time_list.append(end - start)
    printResults("Object", getsizeof(objectParameter), "Long", getsizeof(response.response))

    # ObjectRequestObject
    for i in range(numIterations):
        start = time.time() * 1000
        channel = grpc.insecure_channel(address)
        stub = dsid_pb2_grpc.GRPCStub(channel)
        response = stub.ObjectRequestObject(dsid_pb2.ObjectRequest(parameter=objectParameter))
        end = time.time() * 1000
        time_list.append(end - start)
    printResults("Object", getsizeof(objectParameter), "Object", getsizeof(response.response))
    
    # BigIntegerListRequest
    for key in rangesForBigRequest:
        bigRequestParameter = list(range(key))
        for i in range(numIterations):
            start = time.time() * 1000
            channel = grpc.insecure_channel(address)
            stub = dsid_pb2_grpc.GRPCStub(channel)
            response = stub.BigIntegerList(dsid_pb2.IntegerListRequest(parameter=bigRequestParameter))
            end = time.time() * 1000
            time_list.append(end - start)
        printResults("Big Integer List Request", getsizeof(bigRequestParameter), "Void", getsizeof(response))

    
def printResults(parameter_type, parameter_size, response_type, response_size):
    global time_list
    logger.info(parameter_type + " | " + str(parameter_size) + " | " + response_type + " | " + str(
    response_size) + " | " + repr(np.mean(time_list)) + " | " + repr(np.std(time_list, ddof=1)) + " | " + repr(
        min(time_list)) + " | " + repr(max(time_list)))
    time_list = []

if __name__ == '__main__':
    run()
