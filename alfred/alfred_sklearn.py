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

# sklearn
url = 'http://scikit-learn.org/stable/modules/classes.html'
r = requests.get(url)
soup = BeautifulSoup(r.content)
ref_sk = soup.select('.section .docutils tr')
download('http://scikit-learn.org/stable/_static/scikit-learn-logo-small.png', '/Users/yeqing/tmp/sklearn.png')

# scipy
url = 'http://docs.scipy.org/doc/scipy/reference/genindex.html'
r = requests.get(url)
soup = BeautifulSoup(r.content)
ref_scipy = soup.select('.indextable a')
download('http://scipy.org/_static/images/scipy_med.png', '/Users/yeqing/tmp/scipy.png')


def get_docs_sk():
    bu = 'http://scikit-learn.org/stable/modules/'
    icon = '/Users/yeqing/tmp/sklearn.png'
    src = 'sklearn scikit-learn'
    for r in ref_sk:
        r = r.select('td')
        f = r[0].select('a')[0].get_text()
        l = r[0].select('a')[0]['href']
        t = r[1].get_text()
        yield (f, t, l, bu, icon, src)


def get_docs_scipy():
    bu = 'http://docs.scipy.org/doc/scipy/reference/'
    icon = '/Users/yeqing/tmp/scipy.png'
    src = 'scipy'
    for r in ref_scipy:
        f = r.get_text()
        l = r['href']
        t = None
        yield (f, t, l, bu, icon, src)


def get_docs():
    for i in get_docs_sk():
        yield i


items = []
q = '{query}'
# q = 'sparse'
words = q.split(' ')
for i, q in enumerate(words):
    for s in list(' _|.?!@$%^'):
        words[i] = words[i].replace(s, ' ')


def iter_doc(item):
    func, text, link, bu, icon, src = item
    arg = '%s%s' % (bu, link)
    title = unicode(func) if func is not None else ''
    subtitle = unicode(text) if text is not None else ''

    words_count = {word: 0 for word in set(words)}
    check = 0
    score = 1
    for word in words:
        if re.search(word, title) is not None:
            words_count[word] += 1
            check = 1
        if re.search(word, subtitle) is not None:
            words_count[word] += 1
            check = 1
        score /= 1 / (1 + exp(-words_count[word] * .5))
    if not check:
        return
    for word in words:
        if re.search(word, src):
            score *= 1.5

    item = alfred.Item(uid='1', arg=arg, title=title, subtitle=subtitle.encode('utf-8'))
    item.title = item.title.decode('utf-8')
    item.subtitle = item.subtitle.decode('utf-8')
    results.append((item, score))


results = []
for i, item in enumerate(get_docs_sk()): iter_doc(item)
# for i, item in enumerate(get_docs_scipy()): iter_doc(item)

results = sorted(results, key=lambda x: x[1], reverse=True)[:20]
for (item, count) in results:
    items.append(item)


def _render(items):
    """
    Render a sequence of Alfred items into a complete XML document.
    """
    root = alfred.E.items(*[item.element() for item in items])
    return alfred.et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')


print _render(items)