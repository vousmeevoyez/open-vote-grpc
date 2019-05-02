"""
    Auth gRPC Servicer
    _______________________
"""
import json
import grpc

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

from autogen import auth_pb2
from autogen import auth_pb2_grpc

from services.remote_call import remote_call

from config import config

SERVICES = config.SERVICES

class Auth(auth_pb2_grpc.AuthServicer):

    def GetAccessToken(self, request, context):
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["GET_ACCESS_TOKEN"]
        # convert request to JSON
        data = MessageToJson(request)
        response = auth_pb2.AccessTokenResponse()

        response = remote_call(
            "POST", url, auth_pb2.AccessTokenResponse(),
            context, data=data
        )
        return response
    # end def

    def RevokeAccessToken(self, request, context):
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["REVOKE_ACCESS_TOKEN"]

        access_token = request.access_token

        response = remote_call(
            "POST", url, auth_pb2.RevokeAccessTokenResponse(),
            context, access_token
        )
        return response
    # end def
