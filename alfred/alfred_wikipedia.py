import json
import requests
from bs4 import BeautifulSoup
import alfred
import re
from numpy import *
import shutil
import os
# -*- coding: utf-8 -*-

def download(url, path):
    if not os.path.exists(path):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)


q = '{query}'
# q = 'covariance'
base_url = 'http://en.wikipedia.org/w/api.php'
url = '%s?action=opensearch&search=%s&limit=10&namespace=0&format=json' % (base_url, q)
r = requests.get(url)
ref = json.loads(r.content)[1]
download('http://upload.wikimedia.org/wikipedia/en/b/bc/Wiki.png', '/Users/yeqing/tmp/wiki.png')


def get_docs():
    bu = 'http://en.wikipedia.org/wiki/'
    icon = '/Users/yeqing/tmp/wikipedia.png'
    src = 'wikipedia'
    for r in ref:
        f = r
        t = None
        l = '%s' % f
        yield (f, t, l, bu, icon, src)


items = []
words = q.split(' ')
for i, q in enumerate(words):
    for s in list(' _|.?!@$%^'):
        words[i] = words[i].replace(s, ' ')


def iter_doc(item):
    func, text, link, bu, icon, src = item
    arg = '%s%s' % (bu, link)
    title = unicode(func) if func is not None else ''
    subtitle = unicode(text) if text is not None else ''

    # words_count = {word: 0 for word in set(words)}
    # check = 0
    # score = 1
    # for word in words:
    # if re.search(word, title) is not None:
    # words_count[word] += 1
    #         check = 1
    #     if re.search(word, subtitle) is not None:
    #         words_count[word] += 1
    #         check = 1
    #     score /= 1 / (1 + exp(-words_count[word] * .5))
    # if not check:
    #     return
    # for word in words:
    #     if re.search(word, src):
    #         score *= 1.5

    item = alfred.Item(uid='1', arg=arg, title=title, subtitle=subtitle.encode('utf-8'))
    item.title = item.title.decode('utf-8')
    item.subtitle = item.subtitle.decode('utf-8')
    # results.append((item, score))
    results.append(item)


results = []
for i, item in enumerate(get_docs()): iter_doc(item)
# for i, item in enumerate(get_docs_scipy()): iter_doc(item)

# results = sorted(results, key=lambda x: x[1], reverse=True)[:20]
for item in results:
    items.append(item)


def _render(items):
    """
    Render a sequence of Alfred items into a complete XML document.
    """
    root = alfred.E.items(*[item.element() for item in items])
    return alfred.et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')


print _render(items)