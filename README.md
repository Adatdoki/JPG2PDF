2024.10.30.
A mostani kód a következő funkciókat és jellemzőket biztosítja:
EXIF Forgatás: A program az apply_exif_rotation függvény használatával automatikusan alkalmazza az EXIF adatok szerinti forgatást minden képen, mielőtt manuális beavatkozás történhetne.

Kérdés a Manuális Forgatásról: Az EXIF forgatás után a program választási lehetőséget kínál a felhasználónak a manuális forgatáshoz (Igen/Nem opció). Ez lehetővé teszi, hogy a felhasználó további módosításokat végezzen a képeken, ha szükséges.

Folyamatjelzés: A kód folyamatjelzéseket biztosít:

Az EXIF forgatás során kiírja a feldolgozott képek sorszámát. A PDF generálás során, amikor a képeket hozzáadja a PDF-hez, szintén kiírja a sorszámokat. A mentés előtt külön folyamatjelző jelenik meg, amely jelzi a PDF létrehozásának folyamatát. Időmérés: A program rögzíti a PDF generálási folyamat kezdetét és végét, és megjeleníti a teljes feldolgozási időt.

EXIF Információk a PDF-ben: A PDF minden oldalán megjelenik az EXIF orientációs információ és a kép létrehozási adatai.

Képmegjelenítés és DPI Kezelés:

A képek 300 pixeles magasságú előnézeti megjelenítéssel rendelkeznek. A thumbnail metódussal 300 DPI-re csökkenti a képeket, ha azok eredetileg nagyobb felbontásúak. Ez biztosítja a követelményeknek megfelelő méretet. Fájlnév Formátuma: Az eredményül kapott PDF fájl formátuma dinamikusan tartalmazza az aktuális dátumot és időt a YYMMDD-HHMM formátumban.

Képminőség Megőrzése: A 0 fokos forgatások nem vezetnek újramentéshez, így a képminőség megmarad.

Az output PDF fájl: "JPG2PDF_YYMMDD-HHMM.PDF" és a megadott mappába másolódik.
