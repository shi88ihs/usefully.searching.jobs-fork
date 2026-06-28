#!/usr/bin/env python3
import argparse
import re
import json
import csv
import shutil
import time
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

URL_REGEX = re.compile(r'https?://[^\s<>"\'\]\[()]+')

def setup_session():
    session = requests.Session()
    retries = Retry(total=1, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    })
    return session

import signal

def handler(signum, frame):
    raise TimeoutError("Global URL timeout")

def check_url_with_timeout(session, url):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(15) # 15 seconds absolute max
    try:
        res = check_url(session, url)
        return res
    except TimeoutError:
        return {'status': 'timeout', 'final_url': url, 'code': None, 'reason': 'Global Timeout (tarpit)'}
    finally:
        signal.alarm(0)

def check_url(session, original_url):
    upgraded = False
    test_url = original_url

    if original_url.startswith('http://'):
        test_url = original_url.replace('http://', 'https://')
        upgraded = True

    def do_request(u):
        try:
            # Test using HEAD first as required
            res = session.head(u, timeout=5, allow_redirects=True)
            content = ""
            
            # If HEAD fails or is not allowed, use GET
            if res.status_code >= 400 or res.status_code == 405:
                res = session.get(u, timeout=5, allow_redirects=True, stream=True)
                content = next(res.iter_content(chunk_size=4096), b'').decode('utf-8', errors='ignore').lower()
            else:
                get_res = session.get(u, timeout=5, allow_redirects=True, stream=True)
                content = next(get_res.iter_content(chunk_size=4096), b'').decode('utf-8', errors='ignore').lower()
                res = get_res
                
            res.close()
            return res, content, None
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code if e.response else None
            return e.response, "", (code, str(e))
        except requests.exceptions.Timeout:
            return None, "", ("timeout", "Timeout")
        except requests.exceptions.SSLError:
            return None, "", ("ssl_error", "SSL Error")
        except requests.exceptions.ConnectionError:
            return None, "", ("dns_error", "Connection/DNS Error")
        except Exception as e:
            return None, "", ("unknown", str(e))

    res, content, err = do_request(test_url)

    # Fallback to http if https failed and it was an upgrade attempt
    if upgraded and (err or (res and res.status_code >= 400 and res.status_code not in [401, 403, 406, 429])):
        fallback_res, fallback_content, fallback_err = do_request(original_url)
        if not fallback_err and fallback_res and fallback_res.status_code < 400:
            res, content, err = fallback_res, fallback_content, fallback_err
            upgraded = False

    if err:
        err_type, msg = err
        if isinstance(err_type, int):
            if err_type in [401, 403, 406, 429]:
                return {'status': 'blocked', 'final_url': test_url, 'code': err_type, 'reason': msg}
            return {'status': 'dead', 'final_url': test_url, 'code': err_type, 'reason': msg}
        return {'status': err_type, 'final_url': test_url, 'code': None, 'reason': msg}

    if res.status_code >= 400:
        if res.status_code in [401, 403, 406, 429]:
            return {'status': 'blocked', 'final_url': res.url, 'code': res.status_code, 'reason': f'HTTP {res.status_code}'}
        return {'status': 'dead', 'final_url': res.url, 'code': res.status_code, 'reason': f'HTTP {res.status_code}'}

    # Suspicious logic (parked domains / ad farms)
    suspicious_keywords = [
        "buy this domain", "domain is parked", "hugedomains.com", 
        "this domain is for sale", "domain is for sale", "renew now"
    ]
    if any(kw in content for kw in suspicious_keywords):
        return {'status': 'suspicious', 'final_url': res.url, 'code': res.status_code, 'reason': 'parked/suspicious content'}

    if upgraded:
        return {'status': 'upgraded_to_https', 'final_url': res.url, 'code': res.status_code, 'reason': 'Success via HTTPS'}

    if res.history and res.url != original_url:
        return {'status': 'redirected', 'final_url': res.url, 'code': res.status_code, 'reason': f'Redirected to {res.url}'}

    return {'status': 'working', 'final_url': res.url, 'code': res.status_code, 'reason': 'OK'}

def main():
    parser = argparse.ArgumentParser(description="Link Audit Script")
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--apply", action="store_true", help="Apply fixes to the file")
    parser.add_argument("--remove", type=str, default="dead,timeout,dns_error,ssl_error", help="Comma-separated list of statuses to remove")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"File {args.input} not found.")
        return

    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_urls = URL_REGEX.findall(content)
    urls = sorted(list(set(raw_urls)))

    print(f"Found {len(urls)} unique URLs. Auditing...")
    session = setup_session()
    results = {}

    for i, u in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Checking {u} ... ", end="", flush=True)
        res = check_url_with_timeout(session, u)
        results[u] = res
        print(f"{res['status'].upper()} ({res['code'] or '-'})", flush=True)

    os.makedirs("reports", exist_ok=True)

    with open("reports/link-audit.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    with open("reports/link-audit.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Status", "Final URL", "Code", "Reason"])
        for u, r in results.items():
            writer.writerow([u, r["status"], r["final_url"], r["code"], r["reason"]])

    status_counts = {}
    for r in results.values():
        status_counts[r['status']] = status_counts.get(r['status'], 0) + 1

    with open("reports/link-audit.md", "w", encoding="utf-8") as f:
        f.write("# Link Audit Report\n\n")
        f.write("## Summary\n\n")
        for k, v in status_counts.items():
            f.write(f"- **{k}**: {v}\n")
        f.write("\n## Details\n\n")
        f.write("| URL | Status | Code | Final URL |\n")
        f.write("|---|---|---|---|\n")
        for u, r in results.items():
            f.write(f"| {u} | {r['status']} | {r['code'] or '-'} | {r['final_url']} |\n")

    print("\nReports saved to reports/link-audit.*")

    if args.apply:
        print("Applying changes...")
        shutil.copy(args.input, args.input.replace('.md', '.before-link-audit.md'))
        remove_statuses = [s.strip() for s in args.remove.split(',')]

        new_content = content
        for u, r in results.items():
            if r['status'] in remove_statuses:
                # Replace [Text](URL)
                md_link_pattern = re.compile(r'\[([^\]]+)\]\(' + re.escape(u) + r'\)')
                new_content = md_link_pattern.sub(r'\1 [link removed: ' + r['status'] + ']', new_content)
                # Replace remaining bare links
                new_content = new_content.replace(u, f'[link removed: {r["status"]}]')
            elif r['status'] == 'upgraded_to_https':
                new_content = new_content.replace(u, u.replace('http://', 'https://'))

        with open(args.input, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Changes applied. Backup saved.")

if __name__ == "__main__":
    main()