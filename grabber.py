import re
import urllib.request

SOURCES = [
    "https://cccam-premium.pro/free-cccam/",
    "https://cccamsate.com/free",
    "https://bosscccam.co/Test.php",
    "https://testious.com/",
    "https://testcline.com/free-cccam-server.php",
    "https://raw.githubusercontent.com/anow2008/cccam/refs/heads/main/server",
    "https://raw.githubusercontent.com/abedmryan/cccamlist/refs/heads/main/cccam"
]

def run_grabber():
    seen_lines = set()
    ordered_lines = []
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
                        # On évite les doublons tout en gardant l'ordre d'apparition par source
                        if cline not in seen_lines:
                            seen_lines.add(cline)
                            ordered_lines.append(cline)
        except Exception as e:
            print(f"[!] Erreur sur {url}: {e}")

    output_filename = "Oscam line Grab"
    with open(output_filename, "w", encoding="utf-8") as f:
        for line in ordered_lines:
            f.write(line + "\n")

    print(f"[+] Succès ! {len(ordered_lines)} lignes enregistrées dans l'ordre des sources.")

if __name__ == "__main__":
    run_grabber()
