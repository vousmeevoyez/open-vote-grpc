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

def load_certificate(certificate_name, private_key_name):
    """ load certificate and return it"""
    with open(private_key_name, 'rb') as f:
        private_key = f.read()
    with open(certificate_name, 'rb') as f:
        certificate_chain = f.read()
    return private_key, certificate_chain
# end def

def start(is_ssl):
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
    if is_ssl:
        private_key, certificate_chain = load_certificate(
            os.environ.get("CERTIFICATE"),
            os.environ.get("PRIVATE_KEY")
        )

        server_credentials = grpc.ssl_server_credentials(
            ((private_key, certificate_chain,),)
        )
        endpoint = f"{host}:{port}"
        server.add_secure_port(endpoint, server_credentials)
        message = "Running gRPC with SSL at {}:{}"
    else:
        server.add_insecure_port("{}:{}".format(host, port))
        message = "Running gRPC withouth SSL at {}:{}"
    # end if

    server.start()
    print(message.format(host, port))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    start(os.environ.get("GRPC_SSL", False))
