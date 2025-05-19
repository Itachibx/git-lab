# scan_sensitive_files.py
import requests

FILE_EXT = ["pdf", "docx", "xlsx", "txt", "xml", "log", "env", "bak", "zip", "rar"]
COMMON_NAMES = ["robots", "sitemap", "report", "data", "api", "config", "backup", "error"]

def check_url(url):
    try:
        r = requests.head(url, timeout=5)
        if r.status_code == 200:
            print(f"[+] Found: {url}")
            return url
    except:
        pass
    return None

def scan_subdomain_files(input_file):
    found = []
    with open(input_file, "r") as f:
        subs = [line.strip() for line in f.readlines()]
    for sub in subs:
        for name in COMMON_NAMES:
            for ext in FILE_EXT:
                full_url = f"https://{sub}/{name}.{ext}"
                if check_url(full_url):
                    found.append(full_url)
    with open("vpbank_sensitive_files.txt", "w") as f:
        for link in found:
            f.write(link + "\n")

if __name__ == "__main__":
    scan_subdomain_files("viettel_live_subdomains.txt")
