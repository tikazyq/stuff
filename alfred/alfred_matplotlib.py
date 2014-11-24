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
q = 'axis'
url = 'http://matplotlib.org/search.html?q=%s&check_keywords=yes&area=default' % q
# r = requests.get(url)
# soup = BeautifulSoup(r.content)
# ref = soup.select('.search li')
download('http://matplotlib.org/_static/logo2.png', '/Users/yeqing/tmp/matplotlib.png')


import dryscrape

search_term = 'dryscrape'

# set up a web scraping session
sess = dryscrape.Session(base_url=url)

# we don't need images
sess.set_attribute('auto_load_images', False)

# visit homepage and search for a term
# sess.visit('/')
# q = sess.at_xpath('//*[@name="q"]')
for link in sess.xpath('//a[@href]'):
  print link['href']
exit()
def get_docs():
    bu = 'http://scikit-learn.org/stable/modules/'
    icon = '/Users/yeqing/tmp/matplotlib.png'
    src = None
    for r in ref:
        f = r.select('a')[0].get_text()
        l = r.select('a')[0]['href']
        t = r.get_text()
        yield (f, t, l, bu, icon, src)


def iter_doc(item):
    func, text, link, bu, icon, src = item
    arg = '%s%s' % (bu, link)
    title = unicode(func) if func is not None else ''
    subtitle = unicode(text) if text is not None else ''

    item = alfred.Item(uid='1', arg=arg, title=title, subtitle=subtitle.encode('utf-8'))
    item.title = item.title.decode('utf-8')
    item.subtitle = item.subtitle.decode('utf-8')
    results.append(item)


results = []
for i, item in enumerate(get_docs()): iter_doc(item)


def _render(items):
    """
    Render a sequence of Alfred items into a complete XML document.
    """
    root = alfred.E.items(*[item.element() for item in items])
    return alfred.et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')


print _render(results)