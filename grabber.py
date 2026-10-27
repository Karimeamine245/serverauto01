import re
import urllib.request

SOURCES = [
    "https://dream4evertwo.info/pages/D4E/",
    "https://cccamia.com/cccamfree1/",
    "https://dhoom.org/testoscam/",
    "https://cccamiptv.tv/cccamfree-24h/",
    "https://cccam-premium.pro/free-cccam/",
    "https://cccamgalaxy.com/cccam-free/",
    "https://cccamhub.com/cccamfree/",
    "https://cccam.net/freecccame/",
    "https://cccam.eu/free-cccam-test/"
    "https://testious.com/old-free-cccam-servers/",
]

def run_grabber():
    active_lines = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("[*] Début de la récupération des lignes CCcam...")

    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                matches = re.findall(r'C:\s*([a-zA-Z0-9.-]+)\s+(\d{2,5})\s+([^\s]+)\s+([^\s]+)', content)
                for host, port, user, passwd in matches:
                    if '<' not in host and '>' not in host and len(port) < 6:
                        cline = f"C: {host} {port} {user} {passwd}"
                        active_lines.add(cline)
        except Exception as e:
            print(f"[!] Erreur sur {url}: {e}")

    # Ajout de la source de secours Dream4Ever garantie
    active_lines.add("C: dream4ever.ddns.net 33760 dream4evertwo.info dream4evertwo.info")

    output_filename = "Oscam line Grab"
    with open(output_filename, "w", encoding="utf-8") as f:
        for line in sorted(active_lines):
            f.write(line + "\n")

    print(f"[+] Succès ! {len(active_lines)} lignes enregistrées.")

if __name__ == "__main__":
    run_grabber()
