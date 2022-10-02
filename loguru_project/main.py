from loguru import logger
from config import config
from module1.pyfile import f, some_over_function
from module1.warnings import show

logger.debug(123)


if __name__ == '__main__':
    logger.debug('Main started')
    f('F arg')
    f('Argument2')
    some_over_function('Hello world')

    with logger.catch(message='Fail'):
        1 / 0

    show()
