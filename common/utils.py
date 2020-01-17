import json
from common.config import *


def get_message(client):
    # receive message
    enc_message = client.recv(MAX_NUMBER)
    if isinstance(enc_message, bytes):
        # decode message utf-8
        json_message = enc_message.decode(ENCODING)
        # transform message into json
        responce = json.loads(json_message)
        # return result
        if isinstance(responce, dict):
            return responce
        else:
            raise ValueError
    else:
        raise ValueError

def send_message(sock, message):
    # convert mes to json
    json_message = json.dumps(message)
    # encode mes utf-8
    encode_message = json_message.encode(ENCODING)
    # send enc_mes
    sock.send(encode_message)

