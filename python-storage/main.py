from localStoragePy import localStoragePy

local_storage = localStoragePy('bot.local_storage', 'json')

local_storage.setItem('a', {1: 4})

print(local_storage.getItem('a'))
