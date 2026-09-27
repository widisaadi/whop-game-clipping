import os
import re
import urllib.request
import urllib.parse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_myinstants(query):
    encoded = urllib.parse.quote(query)
    url = f"https://www.myinstants.com/en/search/?name={encoded}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for /media/sounds/... or play('...')
            matches = re.findall(r"play\('(/media/sounds/[^']+)'", html)
            if not matches:
                matches = re.findall(r'(/media/sounds/[^"\'\s]+\.mp3)', html)
            full_urls = [f"https://www.myinstants.com{m}" if m.startswith('/') else m for m in matches]
            return list(dict.fromkeys(full_urls))
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def download_file(url, out_path):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp, open(out_path, 'wb') as f:
        f.write(resp.read())
    print(f"Downloaded: {out_path} ({os.path.getsize(out_path)} bytes)")

def main():
    os.makedirs("assets/sfx", exist_ok=True)
    
    queries = {
        "whoosh": "whoosh",
        "pop": "pop",
        "vine_boom": "vine boom",
        "hitmarker": "hitmarker",
        "punch": "punch",
        "ding": "ding"
    }
    
    for key, q in queries.items():
        print(f"\nSearching for '{q}'...")
        results = search_myinstants(q)
        print(f"Results for '{q}': {len(results)}")
        if results:
            print(f"Top 3: {results[:3]}")
            out_file = f"assets/sfx/{key}.mp3"
            try:
                download_file(results[0], out_file)
            except Exception as e:
                print(f"Failed to download {results[0]}: {e}")

if __name__ == "__main__":
    main()
