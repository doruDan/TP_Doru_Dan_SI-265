# Laborator: funcții, metode și importuri pe web
# Student: <Doru Dan>


BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests, time
from bs4 import BeautifulSoup

#EX 21 + 23
def fetch(url, timeout=10):
    """Returneaza obiectul răspuns"""
    response = requests.get(url, timeout=timeout)
    return response

print(fetch(BASE_URL).status_code)
time.sleep(1)

#EX 22
def get_status(url: str) -> int:
    """Returneaza codul de stare al url-ului"""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print(get_status(BASE_URL + "/"))
time.sleep(1)
print(get_status(BASE_URL + "/robots.txt"))
time.sleep(1)
print(get_status(BASE_URL + "/sitemap.xml"))
time.sleep(1)

#EX 23
print(fetch(BASE_URL).status_code)
print(fetch(BASE_URL, timeout=3).status_code)

#EX 24
def get_title(html):
    """Returneaza titlul paginii""" 
    soup = BeautifulSoup(html, "html.parser")
    if soup.title is None:
        return None
    return soup.title.get_text(strip=True)

print(get_title(fetch(BASE_URL).text))

#EX 25
print(help(get_title))

#EX 26
try: 
    print(get_status(123))
except requests.exceptions.MissingSchema as e:
    print(f"{e}")
#Adnotările nu mă opresc, întrucât python le ignoră la rulare

#EX 27
def page_exists(url):
    """Returneaza daca o pagina exista sau nu"""
    try:
        response = fetch(url)
        if response.ok:
            return True
    except requests.exceptions.RequestException:
        return False

print(page_exists("https://this-domain-does-not-exist.invalid"))

#EX 28
def check_paths(base, paths):
    """Returneaza un dictionar care contine toate caile si codurile de stare ale acestora"""
    dictionar = {}
    for path in paths:
        dictionar[f"{path}"] = get_status(base + path)
    return dictionar

print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

#EX 29
def get_header(url, name, default="lipseste"):
    """Returneaza un singur antet"""
    response = fetch(url)
    return response.headers.get(name)

print(get_header(BASE_URL, name="Server"))

#EX 30
def security_headers(url):
    """Verifica prezenta antetelor de securitate"""
    necesare = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    antete_verficate = {}

    response = fetch(url)
    for nume in necesare:
        antete_verficate[f"{nume}"] = nume in response.headers

    return antete_verficate

print(security_headers(BASE_URL))

#EX 31
def score_headers(results):
    """Scrie cate antete de securitate are url-ul"""
    count = 0
    for valoare in results.values():
        if valoare == True:
            count += 1

    return f"{count}/5"
        
print(score_headers(security_headers(BASE_URL)))

#EX 32
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

print(disallowed_paths(fetch_robots(BASE_URL)))

#EX 33
def repsonse_times(*urls):
    """Returneaza un dictionar care afiseaza url-ul si timpul necesar pentru al accesa"""
    dictionar = {}
    for url in urls:
        response = fetch(url)
        dictionar[f"{url}"] = response.elapsed.total_seconds()
    return dictionar

print(repsonse_times(BASE_URL, BASE_URL + "/robots.txt"))

#EX 34
def log(message, **details):
    parti = [message]
    for key, value in details.items():
        parti.append(f"{key}={value}")

    return " | ".join(parti)
print(log("verificat", url=BASE_URL, status=200)) 

#Verificați-vă: Diferenta consta in faptul ca print afișează o valoare pe ecran, iar return o trimite 
# înapoi celui care a apelat funcția, ca să o poată folosi mai departe