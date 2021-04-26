import csv
import requests
from bs4 import BeautifulSoup, Tag
import hashlib

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'accept': '*/*'
}

header_str = """Host: www.google.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://www.google.com/
Connection: keep-alive
Cookie: CGIC=Ikp0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLCovKjtxPTAuOA; NID=206=a-c_fke0XpDxVkoUJTSYctSymRdVFAGmdrk9u0mcrNBdK8-cs0JVwRCPb2lzSdaUSXBTy2L83VdHpymo79WrjXn_bIAi6GEQ-qwXn0xA9dK1V9sYb9wGSrcJ4ADVdXlXYUCYWpUp6at1ywLBLYNiEts75VaU5dd3ouaH8LA3xOuJS8am11v_nOeLZv4QCfUDcUoLrn2TgbWBfdd3lmg-h5v5MFmQYICukEJ1Ai75Con3S-OrOwjkeLxCzDSV0lnbs_GJq1AjNJf205HQiUxh3fKfrltbsN5pQColCt1UQSHmFIb8iBjJXWLStfr9xLjRw8AzBf7Tg18lfLAbFmyRqjuyFx4-c8KZSg; ANID=AHWqTUmLt1xWN8Y3RUhKcS-p0S5xIPUfwB4yZqKHmqosEO2bAwj8R3-pyL7Weq6H; SID=5gefQzm2O3Egarbwc7eP7RHZGaVZAWepcLT1IvKecB0CyQCquqLQ_9lrAvMMtC2XbC-Pyg.; __Secure-3PSID=5gefQzm2O3Egarbwc7eP7RHZGaVZAWepcLT1IvKecB0CyQCqxwFv61QttCxWOYPeT4XxQA.; HSID=A-5FQvRW-NruCaWwC; SSID=AiuBDujCm3_cCMYtn; APISID=v_IXcsI8MxJi3hOR/AEQA4t5CVIUDqhXRn; SAPISID=ZOmnnaeZM94KDX5m/Ai6eMv8k0nIeHSoE2; __Secure-3PAPISID=ZOmnnaeZM94KDX5m/Ai6eMv8k0nIeHSoE2; SIDCC=AJi4QfHb8ciYrN_JNEA01iVviMsgW1_U5D96UQ17QJdVQ7997Rhf2DxDFxvv24j08vPxf_SBbPU; CONSENT=YES+RU.ru+201910; SEARCH_SAMESITE=CgQIsZAB; __Secure-3PSIDCC=AJi4QfGwTYRT7D0S2X3wjyzGCXJc6rCcbPdGWsqcMX8Um2QL-Mcqu_vo_ErKb9LSgkOCjDuN5oI; 1P_JAR=2021-01-10-21; DV=k-WsCoa_ipclQIaWaSHSPtDTYwbjbtf6dVREdB5deQEAAAA
TE: Trailers"""

HEADERS = dict([(header.split(':')[0].strip(), header.split(':')[1].strip()) for header in header_str.split('\n')])
print(HEADERS)
# exit(0)


class GoogleParser:
    def __init__(self):
        self.url = 'https://google.com'

    def get(self, query_str, force=False):
        hash = hashlib.sha1(query_str.encode()).hexdigest()
        filename = f'{hash}.html'
        if not force:
            try:
                with open(filename, 'r') as f:
                    return f.read()
            except:
                pass

        url = f'{self.url}/search?q={query_str}'
        resp = requests.get(url, headers=HEADERS)
        content = resp.text

        with open(filename, 'w') as f:
            f.write(content)
        assert resp.status_code == 200

        return content

    def get_soup(self, html):
        return BeautifulSoup(html, 'html.parser')

    def parse(self, q):
        soup = self.get_soup(self.get(q))

        def target_element(tag: Tag):
            try:
                assert tag.has_attr('id')
                assert tag.has_attr('class')
                assert tag.name == 'div'
                assert 'container' in tag.get('id')
                assert len(tag.get('class')) == 2
                return True
            except AssertionError:
                return False

        def get_result(soup):
            block = soup.find(target_element)
            desc = block.contents[1].div.div.div.contents[1].div.div.div.span
            # print(desc.get_text())
            return desc.get_text()
        try:
            # nav = soup.find(id='main')
            # print(soup.find(id='main').find(id='center_col'))
            # print(nav)
            return get_result(soup)
        except:
            return None


def save_csv(filename, items):
    if not items:
        return
    from time import time
    with open(f'{filename}-{int(time())}.csv', 'w') as f:

        writer = csv.DictWriter(f, items[0].keys())
        writer.writeheader()
        for item in items:
            writer.writerow(item)


def main():
    terms = [
        'youtube',
        # 'google', 'yandex', 'сбербанк', 'lego', 'html', 'swagger', 'linux', 'debian', 'apple', 'lenovo',
        # 'oreo', 'python', 'c++', 'xiaomi', 'macbook', 'кровать', 'React', 'Википедия', 'TikTok'
    ]
    # with open('terms', 'r') as f:
    #     terms = f.read().split('\n')
    parser = GoogleParser()
    google_hints = []
    iteration = 1
    import threading

    def fetch_function(term):
        # print('Fetching', term)
        desc = parser.parse(term)
        # print('Result is', desc)
        google_hints.append({'query': term, 'desc': desc if desc else ''})

    while True:
        print('Итерация', iteration)
        threads = []
        google_hints = []
        for term in terms:
            threads.append(threading.Thread(target=fetch_function, args=(term, )))
            threads[-1].start()
        for thread in threads:
            thread.join()

        if all((item is None for item in google_hints)):
            print('Гугл умер на итерации', iteration)
            break
        iteration += 1
        break

    save_csv('google-hints', google_hints)


if __name__ == "__main__":
    main()
