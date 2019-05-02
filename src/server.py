"""
    gRPC Server
    ___________________
    this is where we register servicer class and start gRPC Server
"""
from concurrent import futures
import os
import time
import grpc

from autogen import auth_pb2_grpc
from autogen import user_pb2_grpc
from autogen import election_pb2_grpc
from autogen import candidate_pb2_grpc

from services.auth import Auth
from services.user import User
from services.election import Election
from services.candidate import Candidate

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def start():
    """ start gRPC Server"""
    host = os.environ.get("GRPC_HOST", '0.0.0.0')
    port = os.environ.get("GRPC_PORT", '5001')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # register GRPC Servicer here
    auth_pb2_grpc.add_AuthServicer_to_server(Auth(), server)
    user_pb2_grpc.add_UserServicer_to_server(User(), server)
    election_pb2_grpc.add_ElectionServicer_to_server(Election(), server)
    candidate_pb2_grpc.add_CandidateServicer_to_server(Candidate(), server)
    # start
    server.add_insecure_port("{}:{}".format(host, port))
    server.start()
    print("Listening gRPC server at {}:{}".format(host, port))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    start()
