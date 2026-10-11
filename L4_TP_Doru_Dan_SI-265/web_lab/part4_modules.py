# Laborator: funcții, metode și importuri pe web
# Student: <Doru Dan>


BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests, urllib.parse, re, hashlib, json, socket, ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from bs4 import BeautifulSoup

#EX 35
def descompune_url(url):
    """Descompune url-ul primit si afiseaza .scheme, .netloc, .path, .query și .fragment"""
    rezultat = urllib.parse.urlparse(url)
   
    print(rezultat.scheme)
    print(rezultat.netloc)
    print(rezultat.path)
    print(rezultat.query)
    print(rezultat.fragment)
    
descompune_url("https://cybercor.org/path?x=1#top")

#EX 36
def compune_url(*legaturi: str):
    """Compune url-uri folosind ulr-ul de baza si restul legaturilor"""
    urluri = []
    for legatura in legaturi:
       url = urllib.parse.urljoin(BASE_URL, legatura) 
       urluri.append(url)
    return urluri

print(compune_url("/about", "contact.html", "../index.html"))

#EX 37
def extract_links(html):
    "Extrage toate legaturile de pe pagina principala si le afiseaza fara duplicate"
    soup = BeautifulSoup(html, "html.parser")
    legaturi = [tag["href"] for tag in soup.find_all("a", href=True)]
    return list(dict.fromkeys(legaturi))

#EX 38
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

#EX 39 
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
 
    def handle_starttag(self, tag, attrs):
        """Adauga fiecare src al unui tag img la o lista daca acesta nu este gol"""
        if tag == "img":
            src_value = dict(attrs).get("src")
            if src_value is not None:
                self.images.append(src_value)
        


response = requests.get(BASE_URL, timeout=TIMEOUT)
finder = ImageFinder()
finder.feed(response.text)
print(len(finder.images), "imagini găsite")
for src in finder.images:
    print(src)

print(response.text.lower().count("<img") )

#EX 40 
def page_fingerprint(url):
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()

print(page_fingerprint(BASE_URL))
print(page_fingerprint(BASE_URL))
#Răspunsurile sunt aceleași. Ele ar fi diferite dacă vreun byte al răspunsului ar fi diferit între cele 2 cereri,
#întrucât răspunsul se schimbă drastic chiar dacă doar un byte se schimbă

#EX 41
def antete_json(url):
    """Returneaza primul antet al unui url"""
    response = requests.get(url)
    
    with open("headers.json", "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2)

    with open("headers.json", encoding="utf-8") as file:
        headers = json.load(file)

    name, value = next(iter(headers.items()))
    return f"{name}: {value}"

print(antete_json(BASE_URL))

#EX 42
def resolve(hostname):
    """Returneaza IP-ul unui domeniu"""
    return socket.gethostbyname(hostname)

print(resolve("cybercor.org"))

#EX 43
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

print(cert_days_left("cybercor.org"))

#Verificați-vă: handle_starttag() este apelat de parser, în interiorul lui feed()