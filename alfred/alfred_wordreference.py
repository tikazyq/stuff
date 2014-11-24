import requests
from bs4 import BeautifulSoup as bs
import alfred

q = '{query}'
q = 'ind'

url = 'http://www.wordreference.com/2012/autocomplete/autocomplete.aspx?dict=enen&query=%s' % q

s = requests.Session()
r = s.get(url)


def fetch_autocomplete():
    words = []
    for line in r.content.split('\n'):
        row = line.split('\t')
        if len(row) >= 3:
            words.append([row[0], row[2]])
    return [w[0] for w in sorted(words, key=lambda x: x[1], reverse=True)[:10]]


def fetch_text(words):
    items = []
    for w in words:
        arg = 'http://www.wordreference.com/definition/%s' % w
        r = s.get(arg)
        text = ' '.join([x.get_text() for x in bs(r.content).select('div.entryRH .rh_def')])
        item = alfred.Item(uid='1', arg=arg, title=w, subtitle=text)
        items.append(item)
    return items


def _render(items):
    """
    Render a sequence of Alfred items into a complete XML document.
    """
    root = alfred.E.items(*[item.element() for item in items])
    return alfred.et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')


words = fetch_autocomplete()
items = fetch_text(words)
print _render(items)