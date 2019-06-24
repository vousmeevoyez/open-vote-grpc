import unittest
import grpc

from faker import Faker

from autogen import auth_pb2
from autogen import auth_pb2_grpc
from autogen import election_pb2
from autogen import election_pb2_grpc
from autogen import candidate_pb2
from autogen import candidate_pb2_grpc

from tests.test_base import TestBase

class TestCandidateClient(TestBase):

    def setUp(self):
        stub = auth_pb2_grpc.AuthStub(self.channel)
        request = auth_pb2.AccessTokenRequest()
        request.username = "admin"
        request.password = "p4ssw0rd"
        response = stub.GetAccessToken(request)
        self._access_token = response.body.access_token

        self._create_election()
        self._create_candidate()

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
            self.assertTrue(response.body.election_id)
            self._election_id = response.body.election_id
        # end try

    def _create_candidate(self):
        """ test create candidate """
        stub = candidate_pb2_grpc.CandidateStub(self.channel)
        request = candidate_pb2.CreateCandidateRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.election_id = self._election_id
        # set body
        request.body.name = "some candidate name"
        request.body.description = "some candidate description"
        request.body.order_no = "3"
        try:
            response = stub.CreateCandidate(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            self.assertTrue(response.body.candidate_id)
            self._candidate_id = response.body.candidate_id
        # end try

    def test_get_candidate(self):
        """ test get candidate """
        stub = candidate_pb2_grpc.CandidateStub(self.channel)
        request = candidate_pb2.GetCandidateRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.election_id = self._election_id
        request.header.candidate_id = self._candidate_id
        try:
            response = stub.GetCandidate(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            #print(response)
            pass
        # end try

    def test_update_candidate(self):
        """ test update candidate """
        stub = candidate_pb2_grpc.CandidateStub(self.channel)
        request = candidate_pb2.UpdateCandidateRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.election_id = self._election_id
        request.header.candidate_id = self._candidate_id
        # set body
        request.body.name = "updated candidate name"
        request.body.description = "updated candidate description"
        request.body.order_no = "3"
        try:
            response = stub.UpdateCandidate(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            self.assertEqual(response.status, "OK")
        # end try

    def test_cast_vote(self):
        """ test cast vote """
        stub = candidate_pb2_grpc.CandidateStub(self.channel)
        request = candidate_pb2.CastVoteRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.candidate_id = self._candidate_id
        try:
            response = stub.CastVote(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            self.assertEqual(response.status, "OK")
        # end try

    def test_get_candidates(self):
        """ test get candidates """
        stub = candidate_pb2_grpc.CandidateStub(self.channel)
        request = candidate_pb2.GetCandidatesRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.election_id = "8be81504-9772-4e69-95a3-0bb18e93d008"
        try:
            response = stub.GetCandidates(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            print(response)
        # end try

    def test_remove_candidate(self):
        """ test remove candidate """
        stub = candidate_pb2_grpc.CandidateStub(self.channel)
        request = candidate_pb2.RemoveCandidateRequest()
        # set header
        request.header.access_token = self._access_token
        request.header.election_id = self._election_id
        request.header.candidate_id = self._candidate_id
        try:
            response = stub.RemoveCandidate(request)
        except grpc.RpcError as error:
            print(error.code())
            print(error.details())
        else:
            self.assertEqual(response.status, "OK")
        # end try
