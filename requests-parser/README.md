
See [scrapy documentation](https://docs.scrapy.org/en/latest/intro/overview.html) (it is awesome) before study this project

Project was created with.
```
scrapy startproject sandbox
```
Create spyder
```
cd sandbox
scrapy genspider rates dollara.ru
```

Scrapy shell for developing\
```
scrapy shell http://quotes.toscrape.com/
```
Это просто великая вещь. Тут можно получать запросы, сразу их обрабатывать с помощью селекторов
прямо в интерактивной консоли. Запускать поучка и тд

Собственно начать кралить (парсить) с помощью паука
```
scrapy crawl quotes -O quotes.json
```
Здесь quotes - название паука (в папке spiders), quotes.json навание выходного файла с готовыми данными
crawl - команда scrapy

## Этот проект
Эта папка содержит модуль для экспериментов и тестов с парсингом.
Набор утилит.
В частности состоит из:

1. `sandbox_parser_utils.py` функции для парсинга и сохранения результата
2. `main.py` содержит main. Там писать весь код. Осатльное не трогать

Все писать в функции main. Там определено много полезного облегчающего работу.
