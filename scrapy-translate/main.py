import func_timeout
import translators as ts

wyw_text = '季姬寂，集鸡，鸡即棘鸡。棘鸡饥叽，季姬及箕稷济鸡。'
chs_text = '季姬感到寂寞，罗集了一些鸡来养，鸡是那种出自荆棘丛中的野鸡。野鸡饿了唧唧叫，季姬就拿竹箕中的谷物喂鸡。'
text = """Translators is a library which aims to bring free, multiple, enjoyable translation to individuals and students in Python. It based on the translation interface of Google, Yandex, Microsoft(Bing), Baidu, Alibaba, Tencent, NetEase(Youdao), Sogou, Deepl, etc"""
# input languages
# print(ts.deepl(wyw_text)) # default: from_language='auto', to_language='en'

# professional field
# Работает
# print(ts.alibaba(text, to_language='ru'))  # ("general","message","offer")
# Не работает
# print(ts.baidu(text, professional_field='common', to_language='ru'))  # ('common','medicine','electronics','mechanics')

# print(ts.youdao(text, to_language='ru'))
# Работает
# print(ts.google(text, if_use_cn_host=True, to_language='ru'))
# Работает
# print(ts.bing(text, if_use_cn_host=False, to_language='ru'))

# detail result

# print(ts.sogou(text, if_use_cn_host=False,to_language='ru'))

# help
# from time import sleep, time
#
# def f():
#     b = time()
#     sleep(5)
#     return time() - b
#
#
# if __name__ == '__main__':
#     from concurrent.futures import ThreadPoolExecutor
#
#     with ThreadPoolExecutor() as executor:
#         threads = [
#             executor.submit(f)
#             for i in range(100)
#         ]
#         for thread in threads:
#             print(thread.result())

print(func_timeout.func_timeout(
    8, ts.google, args=('Hello world',), kwargs={
        'if_use_cn_host': True,
        'to_language': 'ru'
    }
))
