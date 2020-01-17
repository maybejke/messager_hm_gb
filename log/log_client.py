import logging
import logging.handlers
import os

# путь до настоящего файла
filename = 'client.log'
LOG_FOLDER = os.path.dirname(os.path.abspath(__file__))
CLIENT_LOG_FILE_PATH = os.path.join(LOG_FOLDER, filename)
#создаем логгер и задаем его уровень
client_logger = logging.getLogger('client')
client_logger.setLevel(logging.INFO)
#создаем обработчик, место куда будет сохраняться и задаем его уровень
client_handler = logging.FileHandler(CLIENT_LOG_FILE_PATH, encoding='utf-8')
client_handler.setLevel(logging.INFO)
#создаем форму вывода и связываем ее с обработчком
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
client_handler.setFormatter(formatter)
#добавляем обработчик в логгер
client_logger.addHandler(client_handler)

