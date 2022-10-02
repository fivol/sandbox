from loguru import logger


def f(a):
    logger.info(a)


def some_over_function(arg):
    logger.debug('Func arg is {}', arg)