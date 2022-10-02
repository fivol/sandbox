import sys

from loguru import logger
from bestconfig import Config

config = Config()

logger.remove()
logger.add(sys.stderr, diagnose=True, serialize=False, level='INFO')
logger.add('logs.log', format='{time} {level:7} {message}', diagnose=False, serialize=True, level='WARNING')
logger.configure(activation=[('module1', False)])

logger.info('Hello loguru')

config = None

logger.debug('Configuration done')
