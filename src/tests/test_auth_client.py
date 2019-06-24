import grpc

from tests.test_base import TestBase

from autogen import auth_pb2
from autogen import auth_pb2_grpc

class TestAuthClient(TestBase):

    def test_get_access_token(self):
        """ test get access token"""
        stub = auth_pb2_grpc.AuthStub(self.channel)
        request = auth_pb2.AccessTokenRequest()
        request.username = "EVOTESUPERADMIN"
        request.password = "password"
        try:
            response = stub.GetAccessToken(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
        # end try

    def test_revoke_access_token(self):
        """ test revoke access token"""
        stub = auth_pb2_grpc.AuthStub(self.channel)
        request = auth_pb2.AccessTokenRequest()
        request.username = "EVOTESUPERADMIN"
        request.password = "password"
        try:
            response = stub.GetAccessToken(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
            access_token = response.body.access_token

            stub = auth_pb2_grpc.AuthStub(self.channel)
            request = auth_pb2.RevokeAccessTokenRequest()
            request.access_token = access_token
            response = stub.RevokeAccessToken(request)
            print(response)
