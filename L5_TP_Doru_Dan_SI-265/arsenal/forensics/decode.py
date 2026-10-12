import re, base64, hashlib, argparse, json
from urllib.parse import unquote
#A1
s = "Salut"
b = s.encode()          # bytes
print(b, b[0])          # b"Salut" 83
# TODO: tipareste b.hex() si refa bytes din hex
print(b.hex())
newbytes = bytes.fromhex(b.hex())

#A2
def ghici_strat(s):
    # TODO: daca are %xx -> "url"
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-f]+", s) and len(s) % 2 == 0: # TODO: daca doar 0-9 a-f si lungime para -> "hex"
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s): # TODO: daca doar A-Za-z0-9+/= -> "base64"
        return "base64"
    
    return "necunoscut"
print(ghici_strat("%2Fetc"))   # url
print(ghici_strat("48656c6c6f"))  # hex


#A3
def desfa(s):
    s = s.strip()
    strat = ghici_strat(s)
    # TODO: pentru fiecare strat, decodeaza
    match strat:
        case "base64":
            rezultat_bytes = base64.b64decode(s)
        case "hex":
            rezultat_bytes = bytes.fromhex(s)
        case "url":
            rezultat_bytes =  unquote(s).encode()
        case _:
            return strat, s.encode()
    
    return strat, rezultat_bytes
    
#A4
def citibil(b):
    return all(32 <= c < 127 for c in b)
 
val = "NTM1OTU3NTk="
for _ in range(8):
    strat, b = desfa(val)
    if strat not in ("base64", "hex", "url") or not citibil(b):
        print(val)
        break
    
    val = b.decode()

#A5
date = open("probe/xor.bin", "rb").read()
for k in range(256):
    clar = bytes(b ^ k for b in date)
    if citibil(clar):
        print("cheie:", k, clar.decode())
        break

#A6
tinta = open("probe/hashuri.txt").readline().strip()
print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256
for cuv in open("probe/wordlist.txt", encoding="latin1"):
    cuv = cuv.strip()
    # TODO: daca hashlib.md5(cuv.encode()).hexdigest()
    #       == tinta: print("gasit:", cuv); break
    match len(tinta):
        case 32:
            if hashlib.md5(cuv.encode()).hexdigest() == tinta:
                print("gasit:", cuv)
                break
        case 40:
            if hashlib.sha1(cuv.encode()).hexdigest() == tinta:
                print("gasit:", cuv)
                break
        case 64:
            if hashlib.sha256(cuv.encode()).hexdigest() == tinta:
                print("gasit:", cuv)
                break

#A7
def main():
    p = argparse.ArgumentParser()
    p.add_argument("intrare")          # sir sau cale
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()
    
    if a.fisier:
        with open(a.intrare, "rb") as file:
            val = file.read().decode().strip()
    else:
        val = a.intrare

    ultim = None
    for i in range(8):
        try:
            strat, b = desfa(val)
        except Exception:
            break
        if strat == "necunoscut" or not citibil(b):
            break
        ultim = (strat, b)
        val = b.decode()

    strat, b = ultim

    with open("arsenal/forensics/fisa.json", "w") as file:
        json.dump({"strat": strat, "rezultat": b.decode()}, file, indent=4)

if __name__ == "__main__":
    main()