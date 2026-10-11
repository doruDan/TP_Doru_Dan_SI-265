# Laborator: funcții, metode și importuri pe web
# Student: <Doru Dan>
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time

#EX 1
import requests
print(requests.__version__)
import urllib.request
time.sleep(1)
# urllib este un modul integrat în biblioteca standard a limbajului, astfel 
# el vine preinstalat cu mediul de execuție python și nu necesită o instalare separată.
# În schimb, requests este o bibliotecă terță, astfel trebuie instalată manual, folosind 
# managerul de pachete pip.

#EX 2
r = requests.get(BASE_URL, timeout=TIMEOUT) #cu acest stil oricine citește linia știe de unde vine funcția get
print(r.status_code)        
time.sleep(1)

from requests import get #acest stil este mai concis, deoarece necesită mai puțină tapare
r = get(BASE_URL, timeout=TIMEOUT)
print(r.status_code)
time.sleep(1)

#EX 3
import requests as rq
r = rq.get(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
# un alias face codul mai greu de citit atunci când numele acestuia nu este reprezentativ sau ușor de înțeles
# în schimb, atunci când aliasul permite scrierea mai concisă și are un nume descriptiv, el face codul mai ușor
# de citit


#EX 4
req = urllib.request.Request(ECHO_URL,  headers={"User-Agent": "Mozilla/5.0 (student lab; Python urllib)"})

with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
    status = r.status
    data = r.read().decode("utf-8")
print(status)
print(data[:200])
time.sleep(1)

#EX 5
print(dir(requests))
# ConnectTimeout - clasă
# post - funcție
# packages - modul
time.sleep(1)

#EX 6
help(requests.get)
r = requests.get(BASE_URL, timeout=TIMEOUT)
print(r.status_code)
time.sleep(1)

#EX 7
start_time = time.perf_counter()
response = requests.get(BASE_URL, timeout=TIMEOUT)
end_time = time.perf_counter()
print(f"Timp cu perf_counter: {end_time - start_time}")
print(f"Timp cu response.elapsed: {response.elapsed.total_seconds()}")
time.sleep(1)

#EX 8
try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")

#Verificați-vă: Diferența dintre un modul, un pachet și o bibliotecă constă în faptul că modulul 
# e un singur fișier, pachetul e o directoare de module, iar biblioteca conține o multitudine de 
# fișiere sau pachete menite să soluționeze o problemă