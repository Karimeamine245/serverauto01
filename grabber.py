import re
import requests

SOURCES = [
    "https://dream4evertwo.info/pages/D4E/",
    "https://cccamia.com/cccamfree1/",
    "https://dhoom.org/testoscam/",
    "https://cccamiptv.tv/cccamfree-24h/",
    "https://cccam-premium.pro/free-cccam/",
    "https://cccamgalaxy.com/cccam-free/",
    "https://cccamhub.com/cccamfree/",
    "https://cccam.net/freecccame/",
    "https://cccam.eu/free-cccam-test/",
    "https://testious.com/old-free-cccam-servers/"
]

def run_grabber():
    active_lines = set()
    
    # En-têtes HTTP pour simuler un vrai navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.9',
        'Connection': 'keep-alive'
    }

    print("[*] Début de la récupération des lignes CCcam...")
    session = requests.Session()

    for url in SOURCES:
        try:
            print(f"[*] Interrogation de : {url}")
            response = session.get(url, headers=headers, timeout=12, allow_redirects=True)
            
            if response.status_code == 200:
                content = response.text
                
                # Expression régulière pour capturer les lignes C:
                matches = re.findall(r'C:\s*([a-zA-Z0-9.-]+)\s+(\d{2,5})\s+([^\s]+)\s+([^\s]+)', content)
                
                found_on_page = 0
                for host, port, user, passwd in matches:
                    # Nettoyage d'éventuelles balises HTML parasites
                    host = re.sub(r'<[^>]+>', '', host)
                    passwd = re.sub(r'<[^>]+>', '', passwd)
                    
                    if '<' not in host and '>' not in host and len(port) < 6:
                        cline = f"C: {host} {port} {user} {passwd}"
                        if cline not in active_lines:
                            active_lines.add(cline)
                            found_on_page += 1
                            
                print(f"[+] Trouvé {found_on_page} ligne(s) sur {url}")
            else:
                print(f"[!] Code HTTP {response.status_code} sur {url}")
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Erreur réseau sur {url}: {e}")

    # Ajout de la source de secours garantie
    active_lines.add("C: dream4ever.ddns.net 33760 dream4evertwo.info dream4evertwo.info")

    output_filename = "Oscam line Grab.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        for line in sorted(active_lines):
            f.write(line + "\n")

    print(f"\n[+] Terminé ! Total : {len(active_lines)} lignes uniques enregistrées dans '{output_filename}'.")

if __name__ == "__main__":
    run_grabber()
