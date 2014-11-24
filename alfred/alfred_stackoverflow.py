import json, StringIO, gzip, alfred, urllib, urllib2, datetime


def voiteImg(votes):
    if votes < 0:
        imgStr = 'so--1.png'
    elif votes == 0:
        imgStr = 'so-0.png'
    elif votes > 0 and votes < 10:
        imgStr = 'so-1-1.png'
    elif votes >= 10 and votes < 50:
        imgStr = 'so-10.png'
    elif votes >= 50 and votes < 100:
        imgStr = 'so-50.png'
    elif votes >= 100 and votes < 500:
        imgStr = 'so-100.png'
    elif votes >= 500 and votes < 1000:
        imgStr = 'so-500.png'
    elif votes >= 1000:
        imgStr = 'so-1000.png'

    return imgStr


theQuery = u'{query}'
theQuery = urllib.quote_plus(theQuery)
url = 'https://api.stackexchange.com/2.1/search/advanced?order=desc&sort=votes&site=stackoverflow&q=%s' % theQuery

request = urllib2.Request(url)
request.add_header('Accept-encoding', 'gzip')
req_open = urllib2.build_opener()
conn = req_open.open(request)
req_data = conn.read()

data_stream = StringIO.StringIO(req_data)
gzip_stream = gzip.GzipFile(fileobj=data_stream)
actual_data = gzip_stream.read()

data = json.loads(actual_data)

results = []

for q in data['items']:
    arg = q['link']
    time = datetime.datetime.fromtimestamp(q['creation_date']).strftime('%Y-%m-%d %H:%M:%S')
    subtitle = "Votes:" + str(q['score']) + "   Answers:" + str(q['answer_count']) + "   View:" + str(
        q['view_count']) + "   Create At:" + time
    img = voiteImg(q['score'])

    item = alfred.Item({'uid': 1, 'arg': arg}, q['title'], subtitle.encode('utf-8'), (img, {'type': 'png'}))
    results.append(item)

xml = alfred.xml(results)
alfred.write(xml)