import socket
import sys
import select

from common.config import *
from common.utils import *

import logging
from log.decorators import log

logger = logging.getLogger('server')


def read_requests(r_clients, all_clients):
    """
    читаем запросы клиета
    :param r_clients: клиенты могут отправлять сообщения
    :param all_clients: все клиенты
    :return:
    """
    # list of incoming msg
    messages = []

    for sock in r_clients:
        try:
            # get inc mes
            message = get_message(sock)
            # add it to list
            messages.append((message, sock))
        except:
            print(f'Клиент отключился {sock.fileno()}, {sock.getpeername()}')
            all_clients.remove(sock)
    # return dict of msg
    return messages


@log
# check dict message from client and return answer{dict} to client
def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and isinstance(message[TIME], float):
        return {RESPONSE: 200}
    else:
        return {
            RESPONSE: 400,
            ERROR: 'bad request'
        }


def new_socket_listen(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # load ip, port
    sock.bind(address)
    # listen port
    sock.listen(MAX_CONNECTIONS)
    # таймайт для операций с сокетами
    sock.settimeout(0.5)

    return sock


# отправка сообщений всем
def write_responses(messages):

    for message, sender in messages:
        if message['action'] == MSG:
            to = message['to']
            sock = names[to]
            msg = message['message']
            send_message(sock, message)


print('Server started!')
if __name__ == '__main__':
    # load from command line

    # get port
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

    # address:

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        print(' After -\'a\' enter server address!')
        exit(1)
    sock = new_socket_listen((listen_address, listen_port))
    clients = []
    names = {}
    # run socket

    while True:
        try:
            # accept connection from client
            conn, client_address = sock.accept()
            # получаем сообщение
            presence = get_message(conn)
            # выделяем имя
            client_name = presence['user']['account_name']
            # формируем ответ
            response = process_client_message(presence)
            # отправляем оответ
            send_message(conn, response)
        except OSError as e:
            pass
        else:
            print(f"Получен запрос на соединение от {client_address}")
            names[client_name] = conn
            print(names[client_name])
            clients.append(conn)
        finally:
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            write_responses(requests)  # Выполним отправку ответов клиентам
