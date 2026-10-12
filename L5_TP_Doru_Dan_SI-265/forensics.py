import re
from PIL import Image
from PIL.ExifTags import TAGS
import zipfile

#B1
def tip_real(cale):
    cap = open(cale, "rb").read(8)
    
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    
    return cap.hex()
print(tip_real("probe/foto.jpg"))

#B2
date = open("probe/ascuns.png", "rb").read()
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

#B3
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

gps_info = exif.get(34853)

lat = gps_info.get(2)
lat_reference = gps_info.get(1)
long = gps_info.get(4)
long_reference = gps_info.get(3)

print(f"{lat} {lat_reference}, {long} {long_reference}")

#B4
date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")
if i != -1:
    open("gasit.zip","wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)
# apoi dezarhiveaza si vezi ce era inauntru
    with zipfile.ZipFile("gasit.zip", "r") as zf:
        zf.extractall("extras-iesire")
        print("Arhiva a fost extrasă. Textu extras se găsește în fișierul sectre.txt din folderul extras-iesire.")