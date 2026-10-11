# Laborator: funcții, metode și importuri pe web
# Student: <Doru Dan>


BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests
import time

#EX 9
response = requests.get(BASE_URL, timeout=TIMEOUT)
print(response.status_code) #atribut
print(response.ok) #atribut
print(response.url) #atribut
print(response.encoding) #atribut
print("\n")
time.sleep(1)

#EX 10
try:
    response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"Nu s-a putut accesa site-ul. Eroare: {e.response.status_code}")
    print("\n")
time.sleep(1)

#EX 11
response = requests.get(BASE_URL, timeout=TIMEOUT)
for name, value in response.headers.items():
    print(f"{name}: {value}")
print("\n")
time.sleep(1)

#EX 12
response = requests.get(BASE_URL, timeout=TIMEOUT)
server = response.headers.get("Server", "lipsește")
tip_content = response.headers.get("Content-Type", "lipsește")
print(f"\nServer: {server}")
print(f"Content-Type: {tip_content}")
time.sleep(1)

tip_content = response.headers.get("content-type", "lipsește")
print(f"\nContent-Type: {tip_content}")
print("\n")
time.sleep(1)
#Am observat că response.headers nu este case-sensitive

#EX 13
response = requests.get(BASE_URL, timeout=TIMEOUT)
print(f"Număr de cuvinte: {response.text.lower().count('cyber')}")
print("\n")
time.sleep(1)
#Pot înlănțui .lower() și .count(), deoarece output-ul funcției .lower() este un string, 
# ceea ce îmi permite să trimit output-ul deodată altei funcții

#EX 14
response = requests.get(BASE_URL, timeout=TIMEOUT)
start = response.text.find("<title>")
end = response.text.find("</title>")
text_extras = response.text[start + len("<title>"):end]
print(text_extras)
print("\n")
time.sleep(1)

#EX 15
response = requests.get(BASE_URL, timeout=TIMEOUT)
linii = response.text.splitlines()
print(f"Numărul liniilor: {len(linii)}")
print(f"Lungimea celei mai lungi linii: {len(max(linii, key=len))}")
print("\n")
time.sleep(1)

#EX 16
response = requests.get(BASE_URL, timeout=TIMEOUT)
securizat = response.url.startswith("https://")

if(securizat):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")
print("\n")
time.sleep(1)

#EX 17
response = requests.get("http://cybercor.org" , timeout=TIMEOUT)
for raspuns in response.history:
    print(f"Cod: {raspuns.status_code}")
    print(f"URL: {raspuns.url}")
print(f"Link final: {response.url}")
print("\n")
time.sleep(1)

#EX 18
response1 = requests.head(BASE_URL, timeout=TIMEOUT)
lungime_raspuns1 = len(response1.content)
time.sleep(1)

response2 = requests.get(BASE_URL, timeout=TIMEOUT)
lungime_raspuns2 = len(response2.content)

print(f"Lungimea răspunsului cu head: {lungime_raspuns1}")
print(f"Lungimea răspunsului cu get: {lungime_raspuns2}")

if (lungime_raspuns1 < lungime_raspuns2):
    print("Răspunsul cu get e mai lung")
elif (lungime_raspuns1 > lungime_raspuns2):
    print("Răspunsul cu head e mai lung")
else: 
    print("Răspunsurile au lungimi egale")

print("\n")
time.sleep(1)
#Lungimea răspunsului cu get va fi întotdeauna mai lung decât cel cu head, deoarece requests.get() descarcă atât antetele, cât și corpul paginii, 
#iar requests.head() descarcă doar antetele, astfel lungimea sa va fi întotdeauna 0

#EX 19
response = requests.get(BASE_URL, timeout=TIMEOUT)
if not response.cookies:
    print("Niciun cookie setat")
else: 
    for cookie in response.cookies:
        print(f"{cookie.name}, {cookie.secure}")
print("\n")

#EX 20
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-<Doru Dan>"})
response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print(response.json())

#Verificați-vă: Corpul răspunsului lui response.text nu are paranteze deoarece este un string, în timp ce răspunsul lui response.json() 
# este tratat de python drept un dicționar sau o listă, fiind folosite parantezele în corpul răspunsului