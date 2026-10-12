#EX 5
from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}" + b"\x00"
biti = "".join(f"{x:08b}" for x in mesaj)

if len(biti) > len(px) * 3:
    raise ValueError("Mesajul este prea lung pentru această imagine!")

px_nou = []
index_bit = 0
total_biti = len(biti)

for p in px:
    r, g, b = p

    if index_bit < total_biti:
        bit = int(biti[index_bit])
        r = (r & ~1) | bit  
        index_bit += 1

    if index_bit < total_biti:
        bit = int(biti[index_bit])
        g = (g & ~1) | bit  
        index_bit += 1

    if index_bit < total_biti:
        bit = int(biti[index_bit])
        b = (b & ~1) | bit  
        index_bit += 1

    px_nou.append((r, g, b))

img.putdata(px_nou)
img.save("stego.png")
print("Mesajul a fost ascuns cu succes în 'stego.png'!")

#EX 6
px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""

for (r, g, b) in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

mesaj_bytes = bytearray()
for i in range(0, len(biti), 8):
    octet_biti = biti[i:i+8]
    
    if len(octet_biti) < 8:
        break
        
    valoare = int(octet_biti, 2)
    
    if valoare == 0:
        break
        
    mesaj_bytes.append(valoare)

mesaj_final = mesaj_bytes.decode("utf-8", errors="ignore")
print("Mesajul ascuns este:", mesaj_final)
