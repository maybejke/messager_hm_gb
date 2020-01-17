#запуск нескольких приложений

from subprocess import Popen, CREATE_NEW_CONSOLE
import time

#список заупщенных процессов

p_list = []

while True:
    user = input("Запустить сервер и клиентов (s) / Выйти (q)")

    if user == 's':
        # run server and add to proccess list (p_list)
        p_list.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
        print('Server stated.')
        time.sleep(1)
        for i in range(3):
            client_name = f'Console{i}'
            p_list.append(Popen(f'python client.py 127.0.0.1 8888 {client_name}', creationflags=CREATE_NEW_CONSOLE))
        print('Clients for read started.')

    elif user == 'q':
        print(f'Открыто окно процессов {len(p_list)}')
        for p in p_list:
            print(f'Killind proccess: {p}')
            p.kill()
        p_list.clear()
        print('Exit.')
        break