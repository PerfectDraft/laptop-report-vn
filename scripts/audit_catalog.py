#!/usr/bin/env python3
import argparse, json, re, urllib.error, urllib.request
from collections import Counter
from datetime import datetime, timezone

REQ = ('n', 'p', 'u', 's', 'c', 'r', 'g')
BAD = re.compile(r'(^$|\b(?:unknown|none|n/a)\b|[?])', re.I)

def issue(kind, item, detail):
    return {'type': kind, 'name': item.get('n',''), 'url': item.get('u',''), 'source': item.get('s',''), 'detail': detail}

def link_status(url, timeout):
    request = urllib.request.Request(url, method='HEAD', headers={'User-Agent':'laptop-report-vn-audit/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as error:
        return error.code, url
    except Exception:
        return 0, url

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='all_items.json')
    parser.add_argument('--output', default='reports/data-quality.json')
    parser.add_argument('--check-links', action='store_true')
    parser.add_argument('--limit', type=int, default=100)
    args = parser.parse_args()
    with open(args.input, encoding='utf-8') as file:
        items = json.load(file)
    issues = []
    seen = set()
    for item in items:
        for key in REQ:
            if key not in item or item[key] in (None, ''):
                issues.append(issue('missing_field', item, key))
        if not isinstance(item.get('p'), (int, float)) or item.get('p', 0) <= 0:
            issues.append(issue('invalid_price', item, str(item.get('p'))))
        for key in ('c','r','g'):
            if BAD.search(str(item.get(key, ''))):
                issues.append(issue('unverified_spec', item, key))
        fingerprint = (item.get('n','').strip().lower(), item.get('u',''))
        if fingerprint in seen:
            issues.append(issue('duplicate_record', item, 'duplicate name and URL'))
        seen.add(fingerprint)
    checked = []
    if args.check_links:
        for item in items[:args.limit]:
            status, resolved = link_status(item.get('u',''), 12)
            if status < 200 or status >= 400:
                issues.append(issue('broken_link', item, f'HTTP {status}'))
            checked.append({'url': item.get('u',''), 'status': status, 'resolved_url': resolved})
    counts = Counter(x['type'] for x in issues)
    result = {'generated_at': datetime.now(timezone.utc).isoformat(), 'total_items': len(items), 'checked_links': len(checked), 'summary': dict(counts), 'issues': issues, 'links': checked}
    import os
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps(result['summary'], ensure_ascii=False))

if __name__ == '__main__':
    main()
