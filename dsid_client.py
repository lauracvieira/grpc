from __future__ import print_function

import grpc
import datetime

import dsid_pb2
import dsid_pb2_grpc

import client_log
logger = client_log.setup_custom_logger('root')

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
    response = stub.SendsBigLongResponse(dsid_pb2.BigLongRequest(parameter1=longvalue, parameter2=longvalue, parameter3=longvalue, parameter4=longvalue, parameter5=longvalue, parameter6=longvalue, parameter7=longvalue, parameter8=longvalue))
    end = datetime.datetime.now()
    logger.info("Received request response. Value: " + str(response.message))
    logger.info("Time elapsed: "+ str((end - start).total_seconds()))

    logger.info("Sending String request." )
    start = datetime.datetime.now()
    response = stub.SendsStringResponse(dsid_pb2.StringRequest(message="A"))
    end = datetime.datetime.now()
    logger.info("Received request response. Value: " + str(response.message))
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
