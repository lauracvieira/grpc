from __future__ import print_function

import grpc
import datetime

import dsid_pb2
import dsid_pb2_grpc

import client_log
logger = client_log.setup_custom_logger('root')

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

def format_object_to_string(user):
    return "name: %s, lastname: %s, age: %s, nUSP: %s" % (user.name, user.lastname, user.age, user.nUSP);

def run():
    user = dsid_pb2.User()
    user.name = "Thyago"
    user.lastname = "Ribeiro"
    user.age = 23
    user.nUSP = 1234567

    channel = grpc.insecure_channel('localhost:50051')
    stub = dsid_pb2_grpc.DSIDStub(channel)

    logger.info("Sending Void request." )
    start = datetime.datetime.now()
    response = stub.SendsVoidResponse(dsid_pb2.VoidRequest())
    end = datetime.datetime.now()
    logger.info("Received request response.")
    logger.info("Time elapsed: "+ str((end - start).total_seconds()))

    longvalue = 12345678988881011
    logger.info("Sending Long request. Value: " + str(longvalue))
    start = datetime.datetime.now()
    response = stub.SendsLongResponse(dsid_pb2.LongRequest(message=longvalue))
    end = datetime.datetime.now()
    logger.info("Received request response. Value: " + str(response.message))
    logger.info("Time elapsed: "+ str((end - start).total_seconds()))

    logger.info("Sending 8 parameters Long request. Values: " + str(longvalue))
    start = datetime.datetime.now()
    response = stub.SendsLongResponse(dsid_pb2.BigLongRequest(parameter1=longvalue, parameter2=longvalue, parameter3=longvalue, parameter4=longvalue, parameter5=longvalue, parameter6=longvalue, parameter7=longvalue, parameter8=longvalue))
    end = datetime.datetime.now()
    logger.info("Received request response. Value: " + str(response.message))
    logger.info("Time elapsed: "+ str((end - start).total_seconds()))

    for size in _STRINGS_TO_TEST:
        logger.info("Sending String request. String size: " + str(size) )
        start = datetime.datetime.now()
        response = stub.SendsStringResponse(dsid_pb2.StringRequest(message=_STRINGS_TO_TEST[size]))
        end = datetime.datetime.now()
        logger.info("Received string request response")
        logger.info("Time elapsed: "+ str((end - start).total_seconds()))

    logger.info("Sending Object request. Value: " + format_object_to_string(user))
    start = datetime.datetime.now()
    response = stub.SendsObjectResponse(dsid_pb2.ObjectRequest(message=user))
    end = datetime.datetime.now()
    logger.info("Received request response. Value: " + format_object_to_string(response.message))
    logger.info("Time elapsed: "+ str((end - start).total_seconds()))
    logger.info("\n \n")

if __name__ == '__main__':
    run()
