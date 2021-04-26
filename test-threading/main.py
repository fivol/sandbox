import time
from concurrent.futures.thread import ThreadPoolExecutor
import click
import threading

threads = []


def waiter(my_index):
    i = 0
    while True:
        time.sleep(1)
        print(my_index, i)
        i += 1


@click.command('count')
def threads_count():
    print("Сейчас потоков", threading.active_count())


if __name__ == '__main__':
    threads_count()
    # with ThreadPoolExecutor() as executor:
    #     for i in enumerate(range(10)):
    #         task = executor.submit(waiter, i)
    #         threads.append(task)
