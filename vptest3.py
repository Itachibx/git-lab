# check_alive_subdomains.py
import requests

def check_alive(url):
    try:
        r = requests.get(f"https://{url}", timeout=5)
        if r.status_code < 400:
            print(f"[✓] LIVE: {url}")
            return url
    except:
        pass
    return None

def run_check(input_file, output_file):
    with open(input_file, "r") as f:
        subdomains = [line.strip() for line in f.readlines()]
    alive = []
    for sub in subdomains:
        result = check_alive(sub)
        if result:
            alive.append(result)
    with open(output_file, "w") as f:
        for domain in alive:
            f.write(domain + "\n")

if __name__ == "__main__":
    run_check("viettel_all_subdomains.txt", "viettel_live_subdomains.txt")
