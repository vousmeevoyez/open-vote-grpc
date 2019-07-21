"""
    REMOTE CALL
    _______________________
"""
import requests
import json
import grpc


from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse

from config import config

SERVICES = config.SERVICES

def remote_call(verb, url, response, context, access_token=None, data=None):
    """ execute HTTP Request """
    headers = {
        "content-type": "application/json",
    }

    if access_token is not None:
        headers["Authorization"] = "Bearer {}".format(access_token)
    # end if

    r = requests.request(verb, headers=headers, url=url, data=data)

    if r.ok:
        if r.status_code == 204:
            response.status = "OK"
        else:
            if type(r.json()['data']) is dict:
                Parse(json.dumps(r.json()['data']), response.body)
            elif type(r.json()['data']) is list:
                # iterate here
                items = r.json()['data']
                for item in items:
                    Parse(json.dumps(item), response.body.add())
                # end for
            # end if
        # end if
    elif r.status_code == 401:
        context.set_details(r.json()['message'])
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)
    elif r.status_code == 400:
        # first check if there details or not
        response = r.json()
        if "details" in response:
            context.set_details(json.dumps(r.json()['details']))
        else:
            context.set_details(json.dumps(r.json()['error']))
        # end if
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
    elif r.status_code == 404:
        context.set_details(json.dumps(r.json()['error']))
        context.set_code(grpc.StatusCode.NOT_FOUND)
    elif r.status_code == 422:
        print("herer.....")
        context.set_details(json.dumps(r.json()['error']))
        context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
    # end if
    elif r.status_code == 500:
        context.set_details("Internal Server Error")
        context.set_code(grpc.StatusCode.UNKNOWN)
    # end if
    return response
