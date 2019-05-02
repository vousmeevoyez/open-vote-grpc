import unittest
import grpc

from faker import Faker

from autogen import auth_pb2
from autogen import auth_pb2_grpc
from autogen import election_pb2
from autogen import election_pb2_grpc

class TestElectionClient(unittest.TestCase):

    def setUp(self):
        # connect to gRPC Server
        #self.channel = grpc.insecure_channel('127.0.0.1:6001')
        self.channel = grpc.insecure_channel('0.0.0.0:5001')

        stub = auth_pb2_grpc.AuthStub(self.channel)
        request = auth_pb2.AccessTokenRequest()
        request.username = "EVOTESUPERADMIN"
        request.password = "password"
        response = stub.GetAccessToken(request)
        self._access_token = response.body.access_token

        self._create_election()

    def _create_election(self):
        """ test create election """
        stub = election_pb2_grpc.ElectionStub(self.channel)
        request = election_pb2.CreateElectionRequest()
        # set header
        request.header.access_token = self._access_token
        # payload
        request.body.name = "some election name"
        request.body.description = "some description"
        try:
            response = stub.CreateElection(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
            self.assertTrue(response.body.election_id)
            self._election_id = response.body.election_id
        # end try

    def test_get_election(self):
        """ test get election """
        stub = election_pb2_grpc.ElectionStub(self.channel)
        request = election_pb2.GetElectionRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.election_id = self._election_id
        try:
            response = stub.GetElection(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
        # end try
    
    def test_update_election(self):
        """ test update election """
        stub = election_pb2_grpc.ElectionStub(self.channel)
        request = election_pb2.UpdateElectionRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.election_id = self._election_id
        # set body
        request.body.name = "new election name"
        request.body.description = "new description"
        try:
            response = stub.UpdateElection(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
            self.assertEqual(response.status, "OK")
        # end try

    def test_remove_election(self):
        """ test remove election """
        stub = election_pb2_grpc.ElectionStub(self.channel)
        request = election_pb2.RemoveElectionRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.election_id = self._election_id
        try:
            response = stub.RemoveElection(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
            self.assertEqual(response.status, "OK")
        # end try
