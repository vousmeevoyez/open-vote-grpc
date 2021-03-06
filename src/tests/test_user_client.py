import unittest
import grpc

from faker import Faker

from autogen import auth_pb2
from autogen import auth_pb2_grpc
from autogen import user_pb2
from autogen import user_pb2_grpc

from tests.test_base import TestBase

class TestUserClient(TestBase):

    def setUp(self):
        # connect to gRPC Server
        stub = auth_pb2_grpc.AuthStub(self.channel)
        request = auth_pb2.AccessTokenRequest()
        request.username = "admin"
        request.password = "p4ssw0rd"
        response = stub.GetAccessToken(request)
        self._access_token = response.body.access_token

        self._fake = Faker()

        # create dummy user here
        self._create_user()

    def _create_user(self):
        """ test create user """
        stub = user_pb2_grpc.UserStub(self.channel)
        request = user_pb2.CreateUserRequest()
        # set header
        request.header.access_token = self._access_token
        # payload
        original_name = self._fake.name()
        username = (original_name.lower()).replace(" ", "_")

        request.body.username = username
        request.body.name = original_name
        request.body.identity_id = str(self._fake.random_number(digits=12))
        request.body.msisdn = str(self._fake.random_number(digits=12))
        request.body.email = self._fake.email()
        request.body.role = "PARTICIPANT"
        request.body.password = "password"
        try:
            response = stub.CreateUser(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
            self.assertTrue(response.body.user_id)
            self._user_id = response.body.user_id
        # end try

    def test_get_user(self):
        """ test get user """
        stub = user_pb2_grpc.UserStub(self.channel)
        request = user_pb2.GetUserRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.user_id = self._user_id

        try:
            response = stub.GetUser(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)

    def test_get_users(self):
        """ test get users """
        stub = user_pb2_grpc.UserStub(self.channel)
        request = user_pb2.GetUsersRequest()
        # set header
        request.header.access_token = self._access_token

        try:
            response = stub.GetUsers(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)

    def test_update_users(self):
        """ test update users """
        stub = user_pb2_grpc.UserStub(self.channel)
        request = user_pb2.UpdateUserRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.user_id = self._user_id
        # request body
        original_name = self._fake.name()
        request.body.name = original_name
        request.body.identity_id = str(self._fake.random_number(digits=12))
        request.body.msisdn = str(self._fake.random_number(digits=12))
        request.body.email = self._fake.email()
        request.body.role = "PARTICIPANT"
        request.body.password = "password"

        try:
            response = stub.UpdateUser(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)

    def test_enroll_user(self):
        """ test enroll user """
        stub = user_pb2_grpc.UserStub(self.channel)
        request = user_pb2.EnrollUserRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.user_id = self._user_id
        request.header.candidate_id = "46112627-6073-4ce8-b289-83e67d5c9175"
        try:
            response = stub.EnrollUser(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)

    def test_remove_users(self):
        """ test remove user """
        stub = user_pb2_grpc.UserStub(self.channel)
        request = user_pb2.RemoveUserRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.user_id = self._user_id
        try:
            response = stub.RemoveUser(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
