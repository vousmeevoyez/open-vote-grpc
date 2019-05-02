"""
    Candidate gRPC Servicer
    _______________________
"""
import grpc

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

from autogen import candidate_pb2
from autogen import candidate_pb2_grpc

from services.remote_call import remote_call

from config import config

SERVICES = config.SERVICES

class Candidate(candidate_pb2_grpc.CandidateServicer):
    """ subclass candidate servicer class """

    def CreateCandidate(self, request, context):
        """ Execute Create Candidate HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["CANDIDATE"]
        url = url.format(request.header.election_id)
        # retrieve access token
        access_token = request.header.access_token
        # extract request payload
        data = MessageToJson(request.body, preserving_proto_field_name=True)

        response = remote_call(
            "POST", url, candidate_pb2.CreateCandidateResponse(),
            context, access_token, data
        )
        return response
    # end def

    def GetCandidate(self, request, context):
        """ Execute Get Candidate HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["CANDIDATE"]
        url = url.format(request.header.election_id)
        url = url + request.header.candidate_id
        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "GET", url, candidate_pb2.GetCandidateResponse(),
            context, access_token
        )
        return response
    # end def

    def UpdateCandidate(self, request, context):
        """ Execute Update Candidate HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["CANDIDATE"]
        url = url.format(request.header.election_id)
        url = url + request.header.candidate_id

        access_token = request.header.access_token
        # retrieve data
        data = MessageToJson(request.body, preserving_proto_field_name=True)

        response = remote_call(
            "PUT", url, candidate_pb2.UpdateCandidateResponse(),
            context, access_token, data
        )
        return response
    # end def

    def RemoveCandidate(self, request, context):
        """ Execute Remove Candidate HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["CANDIDATE"]
        url = url.format(request.header.election_id)
        url = url + request.header.candidate_id
        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "DELETE", url, candidate_pb2.RemoveCandidateResponse(),
            context, access_token
        )
        return response
    # end def

    def GetCandidates(self, request, context):
        """ Execute Get Candidates HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["CANDIDATE"]
        url = url.format(request.header.election_id)

        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "GET", url, candidate_pb2.GetCandidatesResponse(),
            context, access_token
        )
        return response
    # end def

    def CastVote(self, request, context):
        """ Execute cast vote HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["VOTE"]
        url = url.format(request.header.candidate_id)

        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "POST", url, candidate_pb2.CastVoteResponse(),
            context, access_token
        )
        return response
    # end def
