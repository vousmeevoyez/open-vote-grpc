"""
    Base Unit Test
"""
import os
import unittest
from pathlib import Path

import grpc

class TestBase(unittest.TestCase):

    def setUp(self):
        self.channel = None
        self.certificate = "secrets/server.crt"

        # setup gRPC
        self._setup_rpc()

    def _load_certificate(self):
        """ load certificate and return it"""
        full_path = os.path.join(self._get_root_path(), self.certificate)
        with open(full_path, "rb") as file_:
            certificate = file_.read()

        credentials = \
        grpc.ssl_channel_credentials(root_certificates=certificate)
        return credentials
	# end def

    def _get_root_path(self):
        return Path(__file__).parent.parent.parent

    def _setup_rpc(self, credentials=None):
        if credentials is None:
            self.channel = grpc.insecure_channel("grpc.vousmeevoyez.xyz:5001")
        else:
            self.channel = grpc.secure_channel("localhost:5001", credentials)
