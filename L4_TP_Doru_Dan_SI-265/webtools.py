# Laborator: funcții, metode și importuri pe web
# Student: <Doru Dan>

#EX 44-50

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
DEFAULT_HEADERS = {"User-Agent": "WebLab-<Doru Dan>"}

import requests, csv, urllib.parse , socket, ssl, re, json
from datetime import datetime, timezone

def fetch(url, timeout=10):
    """Returneaza obiectul răspuns"""
    response = requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)
    return response

def get_status(url: str) -> int:
    """Returneaza codul de stare al url-ului"""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

def get_title(html):
    """Returneaza titlul paginii"""
    start = html.find("<title>")
    end = html.find("</title>")
    text_extras = html[start + len("<title>"):end]
    return text_extras

def security_headers(url):
    """Verifica prezenta antetelor de securitate"""
    necesare = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    antete_verficate = {}

    response = fetch(url)
    for nume in necesare:
        antete_verficate[f"{nume}"] = nume in response.headers

    return antete_verficate

def check_paths(base, paths):
    """Returneaza un dictionar care contine toate caile si codurile de stare ale acestora"""
    dictionar = {}
    for path in paths:
        dictionar[path] = get_status(base + path)
    return dictionar

def save_report(results: dict[str, int], filename: str = "report.csv") -> None:
    """Salvează rezultatele check_paths() într-un fișier CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        for path, status in results.items():
            writer.writerow([path, status, datetime.now().isoformat()])

def resolve(hostname):
    """Returneaza IP-ul unui domeniu"""
    return socket.gethostbyname(hostname)

#######

def security_headers(url):
    """Verifica prezenta antetelor de securitate"""
    necesare = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    antete_verficate = {}

    response = fetch(url)
    for nume in necesare:
        antete_verficate[f"{nume}"] = nume in response.headers

    return antete_verficate

def redirect_chain(url):
    """Returneaza lantul de redirectionari ca lista de siruri."""
    response = fetch(url)
    return [f"{r.status_code} -> {r.headers.get('Location')}" for r in response.history]

def score_headers(results):
    """Scrie cate antete de securitate are url-ul"""
    count = 0
    for valoare in results.values():
        if valoare == True:
            count += 1

    return f"{count}/5"

def cert_days_left(hostname):
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            cert = secure_sock.getpeercert()

    expira = datetime.fromtimestamp(
        ssl.cert_time_to_seconds(cert["notAfter"]), tz=timezone.utc
    )
    acum = datetime.now(timezone.utc)
    return (expira - acum).days

def extract_links(html):
    "Extrage toate legaturile de pe pagina principala si le afiseaza fara duplicate"
    legaturi = re.findall(r'href="([^"]+)"', html) 
    return list(dict.fromkeys(legaturi))

def split_links(links, domain):
    """Imparte legaturile in legaturi externe si interne"""
    interne = []
    externe = []

    for link in links:
        url_complet = urllib.parse.urljoin(BASE_URL, link)
        netloc = urllib.parse.urlparse(url_complet).netloc

        if netloc == domain:
            interne.append(link)
        else:
            externe.append(link)
    return interne, externe

def fetch_robots(base):
    """Returneaza textul fisierului /robots.txt"""
    response = fetch(base + "/robots.txt")
    if response.status_code == 400:
        return None
    return response.text

def disallowed_paths(robots_text):
    """Returneaza o lista cu toate valorile Disallow:"""
    if robots_text is None:
        return []
    
    valori = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            valoare = line[len("disallow:"):].strip()
            valori.append(valoare)
    return valori

##################################################################################################
def site_report(url):
    """Salveaza informatiile despre url in report.json"""
    hostname = urllib.parse.urlparse(url).netloc
    report = {}

    response = fetch(url)
    report["Raport site:"] = response.url
    report["Cod de stare:"] = response.status_code

    report["Titlu:"] = get_title(response.text)

    report["Adresă IP:"] = resolve(hostname)

    report["Redirecționări:"] = redirect_chain(url)

    report["Scor securitate:"] = score_headers(security_headers(url))

    report["Certificat:"] = f"{cert_days_left(hostname)} de zile rămase"

    html = response.text
    links = extract_links(html)
    interne, externe = split_links(links, hostname)

    report["Legături:"] = f"{len(interne)} interne, {len(externe)} externe"

    report["Căi interzise:"] = disallowed_paths(fetch_robots(url))
    report["mesaj"] = "Salvat în report.json"

    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("Salvat în report.json")

site_report(BASE_URL)

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
#Când rulez fișierul webtools.py, Python îi dă lui __name__ valoarea de __main__, deci autotestul rulează,
# iar atunci când rulez fișierul main.py acesta primește valoarea de webtools, deci condiția este falsă și 
# autotestul nu rulează