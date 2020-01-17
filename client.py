import socket
import time
from common.config import *
from common.utils import *
import sys
import threading

import logging
import log.log_client
from log.decorators import log

logger = logging.getLogger('client')


@log
def create_presence(account_name='Guest'):
    if not isinstance(account_name, str):
        raise TypeError
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return message


#@log
def ans_server(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            print(message)
            return message
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    raise ValueError


def read_messages(client, account_name):
    while True:
        message = get_message(client)
        print(message[MESSAGE])


def client_chat_message(message_to, text, account_name='Guest'):
    return {ACTION: MSG, TIME: time.time(), TO: message_to, FROM: account_name, MESSAGE: text}


if __name__ == '__main__':
    # create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        account_name = sys.argv[3]
        print(account_name)
    except IndexError:
        print('Укажите пользователя')

    # соединяемся с сервером
    client.connect((listen_address, listen_port))
    # Создаем сообщение серверу
    presence = create_presence(account_name)
    #отправляем сообщение серверу
    send_message(client, presence)
    # получаем ответ сервера
    response = get_message(client)
    # декодируем ответ
    response = ans_server(response)
    print(response)

    if response[RESPONSE] == 200:
        t = threading.Thread(target=read_messages, args=(client, account_name))
        t.start()

        while True:
            msg_str = input('>> ')
            if msg_str.startswith('message'):
                params = msg_str.split()
                try:
                    to = params[1]
                    text = ' '.join(params[2:])
                except IndexError:
                    print('Задайте получателя или текст.')
                else:
                    message = client_chat_message(to, text, account_name)
                    send_message(client, message)
            elif msg_str == 'help':
                print('message <sender> <text> - send message')
            elif msg_str == 'exit':
                break
            else:
                print('Wrong command, for info print <help>')
        client.disconnect()
