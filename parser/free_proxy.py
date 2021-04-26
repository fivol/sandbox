from grab import Grab, GrabError
from urllib import quote
import re

g = Grab()
g.go('http://www.google.ru/search?num=100&q=' + quote('free proxy +":8080"'))
rex = re.compile(r'(?:(?:[-a-z0-9]+\.)+)[a-z0-9]+:\d{2,4}')
for proxy in rex.findall(g.drop_space(g.css_text('body'))):
    g.setup(proxy=proxy, proxy_type='http', connect_timeout=5, timeout=5)
    try:
        g.go('http://google.com')
    except GrabError:
        print(proxy, 'FAIL')
    else:
        print(proxy, 'OK')