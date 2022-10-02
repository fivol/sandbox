from loguru import logger


def show():
    logger.warning('Something happened')
    try:
        1 / 0
    except:
        logger.exception('All Failed')
