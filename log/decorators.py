import log.log_client
import log.log_server
import logging
import sys


#проверка по названию файла
if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func):

    def log_save(*args, **kwargs):
        logger.info(f'Функция: {func.__name__}, - {args}, {kwargs}')
        re = func(*args, **kwargs)
        return re

    return log_save


