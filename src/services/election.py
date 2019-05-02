"""
    Election gRPC Servicer
    _______________________
"""
import grpc

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

from autogen import election_pb2
from autogen import election_pb2_grpc

from services.remote_call import remote_call

from config import config

SERVICES = config.SERVICES

class Election(election_pb2_grpc.ElectionServicer):
    """ subclass election servicer class """

    def CreateElection(self, request, context):
        """ Execute Create Election HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["ELECTION"]
        # retrieve access token
        access_token = request.header.access_token
        # extract request payload
        data = MessageToJson(request.body, preserving_proto_field_name=True)

        response = remote_call(
            "POST", url, election_pb2.CreateElectionResponse(),
            context, access_token, data
        )
        return response
    # end def

    def GetElection(self, request, context):
        """ Execute Get Election HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["ELECTION"]

        # append election id in url
        url = url + request.header.election_id
        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "GET", url, election_pb2.GetElectionResponse(),
            context, access_token
        )
        return response
    # end def

    def UpdateElection(self, request, context):
        """ Execute Update Election HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["ELECTION"]

        # append election id in url
        url = url + request.header.election_id
        # retrieve access_token
        access_token = request.header.access_token
        # retrieve data
        data = MessageToJson(request.body, preserving_proto_field_name=True)

        response = remote_call(
            "PUT", url, election_pb2.UpdateElectionResponse(),
            context, access_token, data
        )
        return response
    # end def

    def RemoveElection(self, request, context):
        """ Execute Remove Election HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["ELECTION"]

        # append election id in url
        url = url + request.header.election_id
        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "DELETE", url, election_pb2.RemoveElectionResponse(),
            context, access_token
        )
        return response
    # end def

    def GetElections(self, request, context):
        """ Execute Get Elections HTTP Request """
        url = SERVICES["BASE_URL"] + SERVICES["ENDPOINTS"]["ELECTION"]

        # retrieve access_token
        access_token = request.header.access_token

        response = remote_call(
            "GET", url, election_pb2.GetElectionsResponse(),
            context, access_token
        )
        return response
    # end def
