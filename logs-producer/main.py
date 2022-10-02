import sys
from time import sleep, time

from loguru import logger


logger.remove()
logger.add(sys.stdout, serialize=True)


def main():
    i = 0
    while True:
        logger.info('Some message, {}', i)
        print('INFO Hello world')
        print(time(), 'DEBUG', 'Pihui')
        i += 1
        sleep(0.1)

# Make some changes
# Make another changes


if __name__ == '__main__':
    main()
