from concurrent.futures import ThreadPoolExecutor
import time
from functools import wraps
import asyncio


def timing(f):
    """From stackoverflow: https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator"""
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap


repeat = 100
sleep_time = 0.05


def plain_sleep():
    for i in range(repeat):
        time.sleep(sleep_time)


from threading import Thread


def thread_sleep():
    tasks = [
        Thread(target=time.sleep, args=(sleep_time,))
        for i in range(repeat)
    ]
    for t in tasks:
        t.start()

    for t in tasks:
        t.join()


def executor_sleep():
    with ThreadPoolExecutor() as executor:
        for i in range(repeat):
            executor.submit(time.sleep, sleep_time)


def async_sleep():
    tasks = [asyncio.sleep(sleep_time) for i in range(repeat)]
    loop = asyncio.new_event_loop()

    async def sleeper():
        await asyncio.gather(*tasks)
    loop.run_until_complete(sleeper())
    loop.stop()
    loop.close()


def get_diff():
    global sleep_time
    global repeat
    times = []
    for i in range(1, 300):
        print('Iteration', i)
        repeat = i
        t = time.time()
        async_sleep()
        t1 = time.time() - t
        t = time.time()
        thread_sleep()
        t2 = time.time() - t
        t = time.time()
        executor_sleep()
        t3 = time.time() - t
        times.append((t1, t2, t3))
    print(times)


if __name__ == '__main__':
    get_diff()
