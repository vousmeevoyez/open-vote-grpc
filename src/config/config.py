"""
    Configuration File
    __________________
    register configuration like endpoints and base url here
"""
import os

SERVICES = {
    "BASE_URL" : os.environ.get("GRPC_ENDPOINT_URL") or "http://127.0.0.1:5000/api/v1/",
    "ENDPOINTS" : {
        "GET_ACCESS_TOKEN" :  "auth/login",
        "REVOKE_ACCESS_TOKEN" :  "auth/logout",
        "USER" :  "users/",
        "ENROLLMENT" :  "users/{}/enroll/",
        "ELECTION" :  "elections/",
        "CANDIDATE" :  "elections/{}/candidates/",
        "VOTE" :  "votes/{}",
    }
}