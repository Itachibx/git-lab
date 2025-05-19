# subdomain_finder.py
import requests

def get_subdomains(domain):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    try:
        r = requests.get(url, timeout=10)
        if "error" in r.text.lower():
            print("[-] Không tìm được dữ liệu từ HackerTarget.")
            return []
        lines = r.text.splitlines()
        subdomains = set()
        for line in lines:
            sub = line.split(',')[0].strip()
            if sub:
                subdomains.add(sub)
        return sorted(subdomains)
    except Exception as e:
        print("Lỗi khi truy vấn HackerTarget:", e)
        return []
if __name__ == "__main__":
    domain = "viettel.com.vn"
    subdomains = get_subdomains(domain)
    print(f"[+] Tìm thấy {len(subdomains)} subdomain:")
    for sub in subdomains:
        print(" -", sub)
    with open("viettel_all_subdomains.txt", "w") as f:
        for sub in subdomains:
            f.write(sub + "\n")
