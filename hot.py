import json, urllib.request, urllib.parse, ssl, re, os, sys
from datetime import datetime

W = os.environ.get('DINGTALK_WEBHOOK', '')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return r.read().decode('utf-8', errors='replace')
    except Exception as e:
        print('  err: ' + str(e))
        return None

def parse(html):
    if not html:
        return []
    results = []
    for m in re.finditer(r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]{4,80})</a>', html):
        link = m.group(1)
        title = m.group(2).strip()
        skip_words = ['login', 'rss', 'api', 'vip', 'app', 'home', 'about']
        if any(k in title.lower() for k in skip_words):
            continue
        if any(k in link for k in ['apple.com', 'github.com', 'google.com']):
            continue
        exists = False
        for r in results:
            if r['link'] == link:
                exists = True
                break
        if not exists:
            results.append({'title': title, 'link': link, 'hot': ''})
            if len(results) >= 10:
                break
    return results

def fetch_weibo():
    print('weibo...')
    try:
        d = get('https://weibo.com/ajax/side/hotSearch')
        if d:
            dd = json.loads(d)
            if dd.get('ok') == 1:
                items = []
                for it in dd.get('data', {}).get('realtime', [])[:10]:
                    w = it.get('word', '')
                    n = it.get('num', 0)
                    h = str(n // 10000) + 'wan' if n >= 10000 else str(n)
                    items.append({
                        'title': w,
                        'link': 'https://s.weibo.com/weibo?q=' + urllib.parse.quote(w),
                        'hot': h
                    })
                if items:
                    print('  ok ' + str(len(items)))
                    return items
    except Exception as e:
        print('  weibo err: ' + str(e))
    return parse(get('https://tophub.today/n/KqndgxeLl9'))

def fetch(name, tid):
    print(name + '...')
    r = parse(get('https://tophub.today/n/' + tid))
    print('  got ' + str(len(r)))
    return r

def fmt(name, items):
    if not items:
        return '### ' + name + '

> no data
'
    lines = ['### ' + name + '
']
    for i, it in enumerate(items, 1):
        t = it['title']
        if it.get('hot'):
            t = t + ' ' + it['hot']
        if it.get('link'):
            lines.append('> ' + str(i) + '. [' + t + '](' + it['link'] + ')')
        else:
            lines.append('> ' + str(i) + '. ' + t)
    return '
'.join(lines) + '
'

def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print('start: ' + now)

    weibo = fetch_weibo()
    zhihu = fetch('zhihu', 'mproPpoq6O')
    douyin = fetch('douyin', 'DpQvNABoNE')
    xhs = fetch('xhs', 'L4MdA5ldxD')
    kr = fetch('36kr', 'KqndgapoLl')
    ssp = fetch('sspai', 'Y2KeDGQdNP')[:5]

    src = [
        ('weibo', weibo),
        ('zhihu', zhihu),
        ('douyin', douyin),
        ('xhs', xhs),
        ('36kr', kr),
        ('sspai', ssp),
    ]

    total = sum(len(s[1]) for s in src)
    sections = '
---

'.join(fmt(n, items) for n, items in src)
    title = 'hot (' + now + ')'
    content = '# hot
> ' + now + ' | ' + str(total) + '
---
' + sections + '
---
> auto'

    if not W:
        print('NO WEBHOOK')
        sys.exit(0)

    data = {'msgtype': 'markdown', 'markdown': {'title': title, 'text': content}}
    payload = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(W, data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        res = json.loads(r.read().decode('utf-8'))
        if res.get('errcode') == 0:
            print('DINGTALK OK')
        else:
            print('DINGTALK FAIL: ' + str(res))

if __name__ == '__main__':
    main()
