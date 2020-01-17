import socket
import time
from common.config import *
from common.utils import *
import sys

import logging
import log.log_client
from log.decorators import log

logger = logging.getLogger('client')

@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


@log
def ans_server(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: ok'
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    raise ValueError


def read_messages(client):
    while True:
        message = get_message(client)
        print(message)
        print(message[MESSAGE])


def client_chat_message(user, msg):
    return {'user': user, 'msg': msg}


def process_message(client):
    while True:
        text = input('Input message: ')
        if text == 'exit':
            break
        message = client_chat_message('#all', text)
        send_message(client, message)


def main():

    try:
        if '-p' in sys.argv:
            # listen to port, get second item in list == '-p' sys.argv[1]
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('After -\'p\' enter port!')
        exit(1)
    except ValueError:
        print('From 1024 to 65535')
        exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = DEFAULT_IP_ADDRESS
    except IndexError:
        print(' After -\'a\' enter server address!')
        exit(1)

    try:
        mode = sys.argv[3]
    except IndexError:
        mode = 'r'

    ADDRESS = (listen_address, listen_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
        # соединяемся с сервером
        transport.connect(ADDRESS)
        # Создаем сообщение серверу
        presence = create_presence()
        #отправляем сообщение серверу
        send_message(transport, presence)
        # получаем ответ сервера
        response = get_message(transport)
        # декодируем ответ
        response = ans_server(response)
        print(response)

        if response[RESPONSE] == '200: ok':
            if mode == 'r':
                read_messages(transport)
            elif mode == 'w':
                process_message(transport)
            else:
                raise Exception("Неправильный режим чтения/записи")


if __name__ == '__main__':
    main()