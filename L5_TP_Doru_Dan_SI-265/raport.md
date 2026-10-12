#Raport

#Obiectivul lucrării de laborator
    Obiectivul acestui laborator este construirea unor unelte de forensics și steganografie în Python, care să 
permită decodarea universală a unor șiruri, spargerea unor chei XOR sau hash-uri, precum și analiza fișierelor
prin identificarea semnăturilor binare, extragerea metadatelor EXIF și GPS, dezarhivarea fișierelor ascunse și
ascunderea sau dezvăluirea mesajelor prin tehnica LSB.

#Mersul lucrării
    Lucrarea de laborator a început prin etapa de pregătire, care a presupus activarea mediului virtual, 
instalarea bibliotecii Pillow și generarea fișierelor de lucru cu ajutorul scriptului dedicat. 
    În cadrul Lucrării A, am construit un decoder universal în Python capabil să recunoască straturi de 
codare precum base64, hex sau URL, să le desfacă iterativ, să spargă o cheie XOR prin forță brută și să descifreze un hash folosind un dicționar de parole, totul fiind integrat cu argumente în linie de comandă, salvarea rezultatului într-o fișă JSON și crearea unui test de verificare. 
    În cadrul Lucrării B, activitatea a continuat cu analiza forensică a fișierelor, implicând identificarea 
tipului real prin semnăturile binare (magic bytes), extragerea șirurilor de caractere, parsarea metadatelor EXIF și a coordonatelor GPS din imagini, extragerea unei arhive ZIP ascunse la coada unui fișier PNG prin file carving, precum și implementarea unui sistem de ascundere și dezvăluire a unui mesaj secret prin steganografie LSB pe canalele RGB. 

#Rezultatele obținute
    În urma efectuării lucrării de laborator am obținut următoarele rezultate:
Pentru partea A:
1. Mesajul cu straturi ascundea textul „SYWY”;
2. Cheia XOR găsită este 128;
3. Am spart parola „password”.
Pentru partea B:
1. Tipul real al fișierului era „jpeg”;
2. În metadate am găsit modelul telefonului care a făcut poza - Iphone 13, data și timpul când a fost efectuată poza - 14.09.2026, ora 10:30, producătorul telefonului - Apple și locația unde a fost făcută poza - 47° 1' 0" latitudine N și 28° 51' 27" longitudine E;
3. În arhiva ascunsă era textul: FLAG{ascuns_prin_carving};
4. Mesajul LSB dezvăluit este: FLAG{ascuns_in_pixeli}.

#Concluzii
    În concluzie, rezultatele obținute au confirmat eficacitatea uneltelor create, evidențiind capacitatea de a 
extrage informații critice din probele digitale, cum ar fi identificarea metadatelor EXIF și a coordonatelor GPS dintr-o imagine, recuperarea conținutului unei arhive ascunse prin tehnica de file carving și decodarea mesajelor secrete ascunse prin steganografie LSB. Astfel, această lucrare de laborator a facilitat aprofundarea și aplicarea practică a tehnicilor avansate de forensică digitală și steganografie prin dezvoltarea de scripturi în Python.