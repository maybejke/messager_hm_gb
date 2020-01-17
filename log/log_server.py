import logging
import logging.handlers
import os


#создаем путь до файла
filename = 'server.log'
LOG_FOLDER = os.path.dirname(os.path.abspath(__file__))
SERVER_LOG_FILE_PATH = os.path.join(LOG_FOLDER, filename)
# print(SERVER_LOG_FILE_PATH)
logger = logging.getLogger('server')

server_handler = logging.handlers.TimedRotatingFileHandler(SERVER_LOG_FILE_PATH, when='d')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# fh = logging.FileHandler("server.log", encoding='utf-8')
# fh.setFormatter(formatter)
server_handler.setFormatter(formatter)

logger.addHandler(server_handler)
logger.setLevel(logging.INFO)

# if __name__ == '__main__':
#     console = logging.StreamHandler()
#     console.setFormatter(formatter)
#     logger.addHandler(console)
#     logger.debug('Test log')
