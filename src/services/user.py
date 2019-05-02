"""
    User gRPC Servicer
    _______________________
"""
import grpc

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

from autogen import user_pb2
from autogen import user_pb2_grpc

from services.remote_call import remote_call

from config import config

SERVICES = config.SERVICES

class User(user_pb2_grpc.UserServicer):
    """ subclass user servicer class """

    def CreateUser(self, request, context):
        """ Execute Create User HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["USER"]
        # retrieve access token
        access_token = request.header.access_token
        # extract request payload
        data = MessageToJson(request.body, preserving_proto_field_name=True)

        response = remote_call(
            "POST", url, user_pb2.CreateUserResponse(),
            context, access_token, data
        )
        return response
    # end def

    def GetUser(self, request, context):
        """ Execute Get User HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["USER"]

        # append user id in url
        url = url + request.header.user_id
        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "GET", url, user_pb2.GetUserResponse(),
            context, access_token
        )
        return response
    # end def

    def UpdateUser(self, request, context):
        """ Execute Update User HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["USER"]

        # append user id in url
        url = url + request.header.user_id
        # retrieve access_token
        access_token = request.header.access_token
        # retrieve data
        data = MessageToJson(request.body, preserving_proto_field_name=True)

        response = remote_call(
            "PUT", url, user_pb2.UpdateUserResponse(),
            context, access_token, data
        )
        return response
    # end def

    def RemoveUser(self, request, context):
        """ Execute Remove User HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["USER"]

        # append user id in url
        url = url + request.header.user_id
        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "DELETE", url, user_pb2.RemoveUserResponse(),
            context, access_token
        )
        return response
    # end def

    def GetUsers(self, request, context):
        """ Execute Get Users HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["USER"]

        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "GET", url, user_pb2.GetUsersResponse(),
            context, access_token
        )
        return response
    # end def
