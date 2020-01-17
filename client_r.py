import socket
import time
from common.config import *
from common.utils import *
import sys
from client import create_presence, ans_server, read_messages, process_message

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS = ((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
mode = 'r'
# соединяемся с сервером
client.connect(ADDRESS)
# Создаем сообщение серверу
presence = create_presence()
#отправляем сообщение серверу
send_message(client, presence)
# получаем ответ сервера
response = get_message(client)
# декодируем ответ
response = ans_server(response)
print(response)

if response[RESPONSE] == '200: ok':
    if mode == 'r':
        read_messages(client)
    elif mode == 'w':
        process_message(client)
    else:
        raise Exception("Неправильный режим чтения/записи")
