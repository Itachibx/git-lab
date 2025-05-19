import requests
import concurrent.futures
COMMON_BUCKET_SUBS = [
    "assets", "cdn", "media", "static", "storage", "files", "data", "content", "downloads"
]
EXTENSIONS = ["pdf", "docx", "xlsx", "txt", "log", "bak", "xml", "env", "zip", "rar"]
BASE_DOMAIN = "viettel.com.vn"
COMMON_FILE_NAMES = [
    "report", "backup", "log", "error", "sitemap", "robots", "test", "api", "doc", "data", "confidential"
]

def build_file_urls():
    urls = []
    for sub in COMMON_BUCKET_SUBS:
        for name in COMMON_FILE_NAMES:
            for ext in EXTENSIONS:
                full_url = f"https://{sub}.{BASE_DOMAIN}/{name}.{ext}"
                urls.append(full_url)
    return urls

def check_file_url(url):
    try:
        resp = requests.head(url, allow_redirects=True, timeout=5)
        if resp.status_code == 200:
            size = resp.headers.get('Content-Length', 'Unknown')
            print(f"[+] FOUND: {url} | Size: {size}")
            return (url, size)
        elif resp.status_code in [403, 401]:
            print(f"[-] Forbidden: {url}")
        else:
            print(f"[ ] Not Found: {url} | {resp.status_code}")
    except Exception as e:
        print(f"[x] Error: {url} -> {e}")
    return None

def scan_files():
    print(f"[+] Bắt đầu scan file public ở domain: {BASE_DOMAIN}")
    file_urls = build_file_urls()
    print(f"[+] Tổng số file cần kiểm tra: {len(file_urls)}\n")

    found_files = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        results = executor.map(check_file_url, file_urls)
        for result in results:
            if result:
                found_files.append(result)

    print(f"\n[✓] Tổng số file public tìm thấy: {len(found_files)}")
    with open("public_files_found.txt", "w") as f:
        for url, size in found_files:
            f.write(f"{url} | Size: {size}\n")

if __name__ == "__main__":
    scan_files()
