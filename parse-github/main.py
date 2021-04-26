"""
Ищем валидные репозитории
В файле nicknames лежат претенденты на каждой строке
Код проверяет, валидные ли они выводит результат
"""
import re
from pathlib import Path

import requests
from time import time, sleep
import typing as t

input_file = 'nicknames.txt'
output_file = 'repositories.txt'
temp_file = '.tmp'


def get_usernames():
    with open(input_file, 'r') as f:
        text = f.read()

    return re.findall(r'[0-9a-zA-Z\-_.]+', text)


def check_username(username) -> t.Optional[str]:
    print('check username on github', username)
    url = f'https://github.com/{username}'
    response = requests.get(url)
    return response.status_code == 200 and url


def get_already_prepared():
    file = Path(temp_file)
    if not file.exists():
        file.touch()
    with file.open('r') as f:
        return f.read().split('\n')


def append_to_file(filename, string):
    file = Path(filename)
    if not file.exists():
        file.touch()
    with file.open('a') as f:
        f.write('\n' + string)


def main():
    usernames = get_usernames()
    prepared = get_already_prepared()
    for username in set(usernames) - set(prepared):
        sleep(5)
        link = check_username(username)
        append_to_file(temp_file, username)
        if link:
            print('Good link', link)
            append_to_file(output_file, link)


if __name__ == '__main__':
    main()
