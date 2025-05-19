import requests
import tldextract
import concurrent.futures

# Các subdomain thường dùng làm CDN/bucket/static
COMMON_BUCKET_SUBS = [
    "assets", "cdn", "media", "static", "storage", "files", "data", "content", "downloads"
]

# Dải tên miền ngân hàng cần kiểm tra
BASE_DOMAIN = "vpbank.com.vn"

# Từ khóa nghi ngờ bucket public
PUBLIC_KEYWORDS = ["Index of", "<title>Index of", "sitemap.xml", "robots.txt", ".env", "access.log", "bucket"]

def check_endpoint(url):
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            for keyword in PUBLIC_KEYWORDS:
                if keyword.lower() in resp.text.lower():
                    print(f"[!!] Public Bucket? ==> {url} | Contains: {keyword}")
                    return url
        elif resp.status_code in [403, 401]:
            print(f"[-] Forbidden or Protected: {url}")
        else:
            print(f"[?] No public content: {url} | Status: {resp.status_code}")
    except Exception as e:
        print(f"[x] Error with {url}: {e}")
    return None

def scan_buckets():
    targets = []
    for sub in COMMON_BUCKET_SUBS:
        full_url = f"https://{sub}.{BASE_DOMAIN}/"
        targets.append(full_url)

    print(f"[+] Đang kiểm tra {len(targets)} URL khả nghi...")
    public_results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_endpoint, targets)
        for r in results:
            if r:
                public_results.append(r)

    print(f"\n[+] PHÁT HIỆN: {len(public_results)} endpoint có dấu hiệu public\n")
    for url in public_results:
        print("  ->", url)

    # Ghi ra file
    with open("vpbank_bucket_scan_result.txt", "w") as f:
        for url in public_results:
            f.write(url + "\n")

if __name__ == "__main__":
    print("[*] Bắt đầu scan public bucket cho:", BASE_DOMAIN)
    scan_buckets()
