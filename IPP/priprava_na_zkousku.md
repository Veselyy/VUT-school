## 24-25

### 1.termín

Část I

1. **Detailně vysvětlete pojem rozsah platnosti proměnné (scope). (1 souvětí) Uvažte jazyk C a jazyk Python — pro každý jazyk popište jak to je s rozsahem platnosti proměnných, co je pro každý z jazyků typické stran tohoto pojmu. (stačí 2 souvětí, pro každý jazyk jedno, ale výstižně)**

2. **Popište rozdíl mezi statickou a třídní metodou v třídním objektově orientovaném jazyce (OOJ). Jaké je u nich omezení při použití instančních atributů a proč? (2 souvětí)**

3. **Mějme třídní OOJ s podporou výjimek, kde třída výjimky ExA má přímou podtřídu ExB a od ExB přímo dědí ExC. V hlavním těle programu mějme trojici bloků try-catch-finally (nazvěme je vnější) následovanou zbylým kódem, tzv. vnější epilog. Vnější catch-blok má formální parametr typu ExA. Uvnitř vnějšího try-bloku je trojice bloků try-catch-finally (nazvěme je vnitřní) a zbytek kódu vnějšího try-bloku označme jako vnitřní epilog. Vnitřní catch-blok má formální parametr typu ExC. Uvažujme, že na začátku vnitřního try-bloku dojde k vyvolání výjimky třídy ExB. Popište průběh ošetření výjimky v hlavním těle programu (až po případný návrat ke standardnímu modelu výpočtu), aby bylo jasné, které části kódu se vykonají a které ne a proč. (cca 4 souvětí)**

4. **Pomocí UML diagramu tříd navrhněte implementaci návrhového vzoru Pozorovatel (angl. Observer) pro staticky typovaný třídní OOJ s podporou abstraktních tříd. Variantu si vyberte dle libosti, ale uveďte kterou. U důležitých metod uveďte jejich pseudokód. Několika řádky kódu demonstrujte typické použití (instanciaci, provázání a použití) tohoto vzoru s využitím entit uvedených v UML diagramu. (UML diagram, ukázka kódu)**

5. **Definujte co je Hornova klauzule, zapište ji jak v Prologu, tak v predikátové logice. (2 výrazy s popiskama) Pro níže uvedené 2 dvojice termů, pro každou z nich zvlášť, uveďte nejobecnější unifikátor ke každé dvojici (pokud existuje) a term vzniklý aplikací tohoto nejobecnějšího unifikátoru. Dvojice jsou uvedeny pod sebou!**

- **ref(out(A), rtx(B), sin(14,99))**
- **ref(B, C, sin(A,99))**
- **sdsi(zdroj(X), nor(U,73), zem(V,Y))**
- **sdsi(U, nor(U,V), W)**

6. **Definujte pojem typové proměnné známé nejen z funkcionálních jazyků. Vysvětlete (stručně, ale přesně): co to je, k čemu to je/co to umožňuje, ukažte obecný příklad využití, jaká je obdoba v jazycích jako C++, Java, C#?**

7. **Stručně a výstižně definujte výčtem, co musí splňovat výstup kompilátoru modulárních programovacích jazyků, aby výsledný kód byl po „slinkování“ funkční — pozor, nemyslí se chyby v algoritmu, návrhu, implementaci, nebo v době linkování, ale vlastnosti kódu generovaného překladačem nutné pro správné propojení modulů. (Obecná věta plus cca 4-8 odrážky (dle detailu dělení). Všechny zkratky je nutné beze zbytku vysvětlit, ne jen rozvést, a přesně specifikovat jejich význam. Ne jen náznakem, nebo příkladem. Plně!)**

8. **Přesně definujte klíčové vlastnosti/jak lze charakterizovat uzavřený podprogram. (4 odrážky)**

9. **Proveďte a demonstrujte po krocích potřebné α-, β-konverze tak, aby zadaný λ-výraz neobsahoval β-redex. (λxz.xz(λz.z))(λxz.z)**

10. **Prémie: Máme-li dvoudimenzionální pole v jazyce C (bez modifikátorů, tedy se zarovnaným uložením), velikost dimenzí nechť je po řadě sizeX a sizeY — tedy a[sizeX][sizeY]. Prvkem pole je struktura s následujícími členy, po řadě: celé číslo, ukazatel, celé číslo, ukazatel, desetinné číslo, znak. Velikosti jsou: celé číslo 4 bajty (32 bitů), ukazatel 4 bajty, znak 1 bajt (8 bitů), desetinné číslo 8 bajtů (64 bitů). Vytvořte generický výraz pro určení adresy znaku na pozici a[i][j], když pole je umístěno od adresy A a architektura je 32bitová. Jak by se výraz změnil, kdyby byly zapnuty modifikátory pro těsné uložení struktury? Nejde o postup výpočtu, jde o jeden generický aritmetický výraz, do kterého když dosadíme konkrétní hodnoty pro dané konstanty a proměnné, tak dostaneme adresu v paměti.**

### 2. termín

1. **Sémantika**

2. **Aké položky obsahuje trieda (v Pythone)**

3. **Try-catch-finally**

4. **NV Decorator**

5. **Robinson (napísať algoritmus)**

6. **Strict evaluation**

7. **Tri typy predávania parametrov v štrukturálnych jazykoch**

8. **Konvencia u modulárnych jazykov (riadenie toku)**

9. **Lambda calculus**

### 3. termín (13.06.2025)

1. **Syntax, 4 odrazky, 2 chyby které nejsou sémantické ani syntaktické během překladu v Cčku**

2. **OOJ s jednoduchou dědičností — jak se ukládají atributy a metody v paměti (něco s VMT)**

3. **Try-catch-finally (inner–outer)**

4. **Prakticky Adapter (objektový), UML, kód**

5. **Co je Hornova klauzule (jak vypadají v Prologu a predikátové logice), unifikovat prakticky**

6. **Typová třída**

7. **Jak se řeší cyklické závislosti modulů? Dá se nepoužívat deklaraci v modulárních jazycích a proč?**

8. **Struct/záznam v C — jak se ukládá, jaký vliv má cílová architektura, výhody/nevýhody, omezení**

9. **Linker — důkladně popsat jak funguje**

10. **Lambda: `(λcd.c(λc.c)d)(λcd.d)`**

## 23-24

### Skupina A (asi radny)

1. **rozsah platnosti (scope) + popis jak je to v php a C**

2. **co je v pythonu definovane ve tride a ne az v jejich metodach**

3. **try catch**

4. **dekorator**

5. **robinson prakticky (unifikujte)**

6. **typove tridy**

7. **co musi byt vystup prekladace v modularnim jazyku pro linker**

8. **union v C popis jak se uklada, vyhody, nevyhody, rozdily v architekture**

9. **uzavreny podprogram**

10. **lambda kalkul**

11. **bonus 2D pole v C**

### Otazky 1. opravny termin 28. 5. 2024, byla jen jedna skupina

1. **doba zivota promenne (6)**

2. **rozdil mezi tridni a statickou metodou (4)**

3. **vnoreny try-catch-finally blok**

4. **NV Skladba**

5. **prakticky priklad na hledani MGU (asi 6)**

6. **lazy evaluation, jak se to realizuje, co to prinasi**

7. **rozdil vypocetniho modelu imperativnich a deklarativnich jazyku**

8. **jak se uklada struktura v c, vliv cilove architektury**

9. **nejaka blbost ze jak se da napodobit globalni promenna v pascalu nebo v c bez globalnich promennych**

10. **λ-kalkul jako vzdy (6)**

## 22-23

### Skupina A:

1. **Co je syntax, Chyby ktere neni ani syntakticke, ani semanticke (6b)**

2. **Rozdil mezi statickou a tridni metodou v OOJ.  (4b)**

3. **Try Catch (6b)**

4. **Dekorator + UML + kod (8b)**

5. **Prakticky Robinsov algo (6b)**

6. **Modularni jazyk s cyklem a jazyk cykly nepodporuje (3b)**

7. **Funkcionalni jazky, typova promenna, Garbage collector -> jak funguje, jake nevyhody a proc (9b)**

8. **Uzavreni podprogram (6b)**

9. **Lambda kalkul (λ x z . x z (λ z . z)) (λ x z . z)  (thanks @ JosefKuchar) (6b)**

10. **Dekarativni + imperativni (6b)**

11. **Bonus 2D pole v C (thanks @ Gargamel) (8b)**

via @D2ceCube :peepolove~1:

### Skupina B

1. **doba života proměnné + f(x) g(y) v C**

2. **instance a třída v OOJ atributy a metody rozdíly**

3. **Exception**

   **Vyhodí se Exception a má podtřídy Ex1 a ta má podtridu Ex2**

   **Dva catch bloky co chytají Ex1 a Ex2**

4. **Skladba UML kód popis**

5. **popsat linker a chyby**

6. **Robinson**

7. **strukturované jazyky čím se muže předat parametr**

8. **kontroly za běhu co nejsou typové ani existenční**

9. **lazy evaluation**

10. **lambda**

    **(\ab.a(a.a)b)(\ab.a)**

11. **Bonus 2D pole v C**

## 21-22

### Riadny

Bodmi si teraz nie som istý, ale cca by to malo sedieť

Thanks: gunter, Dosral som sa, tedro, penpem, ... <3

1. **Rozsah platnosti (scope) + čo určuje typ premennej (3 odrážky) (5b)**

2. **Exceptions (8b)**

   - Chceli popísať, čo presne sa stane - ktoré z funkcií x, z, k, m sa
     zavolajú a ktoré nie, a vysvetliť prečo (nejak stručne).
   - IOEx aj MathEx dedia od Exception.
   - Bolo to tam popísané slovne, ale to nedokážem zreprodukovať. Kód by
     vyzeral nejak takto:

```python
x(){
    try {
        throw new IOEx
        m()

    } catch Exception {
        throw new MathEx

    } finally {
        k()
    }
}

x();
z();
```

   - Slovný popis by penpem:

     Uvazujte volanie metody x() a z() v hlavnom tele funkcie. V
     metode x je trojica blokov try-catch-finally. V try bloku dochadza k
     vyvolaniu vynimky IOException. Za vyvolanim vynimky IOException je este
     volanie metody m. V catch bloku sa nachadza vyvolanie MathEx.
     Vo finally bloku je este nejake jedno volanie. Ku kazdemu
     volaniu metody uvedte ci sa uskutocni a preco ano/nie.

3. **Abstract factory - na čo je, UML, implementácia dôležitých metód (asi**

   **to napísať do UML diagramu ako je to v prednáškach), príklad**

   **použitia napr. v metóde klienta (9b)**

4. **Modulárne jazyky (7b):**

   - ako prekladače riešia cykly v strome modulov ak to jazyk nepodporuje
     (alebo také niečo)
   - štyri veci ktoré musí prekladač spĺňať aby dokázal správne riadiť tok
     programu alebo čo
   - môže existovať modulárny jazyk bez deklarácií? + 1/2 vety, prečo

5. **Imperatívne vs deklaratívne nielen z pohľadu programátora (5b)**

   - vraj ešte chceli ako sa líši model vyhodnocovania

6. **Strict evaluation (nielen vo funkcionálnych jazykoch) (7b)**

7. **Lambda kalkul - upraviť aby tam neostali žiadne Beta-redex či čo (6b)**

   **(\ab.ab(\b.b))(\ab.b)**

8. **Robinsonův algoritmus - na čo je, čo sú vstupy, čo výstupy a popísať**

   **krok po kroku ako funguje (ak dobre pamätám) (9b)**

9. **Napíš štyri rôzne sémantické chyby teoreticky zistiteľné dynamicky**

   **(počas behu) v jazyku C (áno, písalo tam "teoreticky") (4b)**

BONUS: (8b?)

Majme 2D pole (x * y) štruktúr:

    Int (4B), pointer (4B), pointer (4B), int (4B), char (1B), double (8B)

 - ak pole začína na adrese A, napíšte výpočet pre adresu doublu na [x][y]

 - popíš čo by sa zmenilo, ak by sa zapol nejaký kompaktný mód alebo čo.

   Proste že sa tie položky nejak užšie skladajú za seba alebo tak

### 1. opravný, není to popořade:

1. **Co je syntaxe, čím ji definujem a Cčko věci při překladu (syntakticky a sémanticky správně, ale překlad to zhodí)**

2. **Jednoduchá dědičnost [ahojjasomalex]**

3. **Máš jazyk s možností definování funkci uvnitř funkce (pascal) potom jazyk co umožňuje definovat proměně v sekcích (ci tak něco). Ani jeden však nemá možnost globálních proměnných. Existuje způsob jak uživatelsky nějaká používat něco jako globální proměně? Ve kterém z těchto jazyků? Proč? Jaké vlastnosti proměnných se používají [Vlček]**

4. **NV Dekorátor popsat + pseudokód**

5. **Strukturovaný jazyky? jak je struct v Cčku nebo tak něco**

6. **jak by se udělala globální proměnná v Pascalu a ANSI C, kde to jde udělat a jak [Křivoš]**

7. **Uzavřenej podprogram**

8. **unifikovat nějak chujoviny**

9. **Lambda**

10. **funkcionalní x logický jazyky charakteristický rysy**

11. **No bonus**

### Druhý opravný

1. **Co to je životnost proměně? Jaký máji vztah dvě proměně které jsou**

   **definovane v parametrů dvou funkci např f(x) a f(y). Napiš ke každému**

   **typu dvě až tři odrazky [6]**

2. **Popisat Rozhranie**

3. **Try catch catch finally viz dalsiu moju spravu**

4. **Adapter ale skorej prakticky**

5. **Linker**

6. **Funkcionalne jazyky z coho maju nazov garbage collector a tusim**

   **typova premenna**

7. **Predavanie parametru hodnotou**

8. **Lambda kalkul**

9. **SLD rezolucia**

10. **Citanie hodnoty z bitoveho pola v assembleri - Měj me třetí položku**

    **struktury ze které chceme vyčíst první 4 bity z neznamenkoveho bitoveho**

    **pole. Položka je posunuta o 7 bitů. První plozka je 8 bajtova hodnota,**

    **druhá 4 bajtova. Pracuje v systému s 32 bitovou architekturou a little**

    **endia. Začátek struktury je na adrese A. Použité operace z jazyka c aby**

    **jsem dostali požadovanou adresu. Nepracuje však v jazyku c! Používat**

    **pouze jeho operace.**

Poradie je inak hlavne ku koncu

## 20-21

### Jakoze. Nepamatuju si to moc 😄

1. **scope + ty věci okolo**

3. **robinson ten kod**

4. **try catch**

5. **dekorator**

6. **Rozdíl imperativní/deklarativní**

7. **Strict evoluation**

8. **Lambda**

9. **Něco s dvojrzormernym polem**

modulární jazyky, nějaký ty otázky okolo cyklení

Dynamické semanticke analýzy  4 příklady

### Zhruba si to pamatuji...

1. **doba zivota promenne**

2. **adapter na konkretnim prikladu**

3. **try-catch-finally**

4. **linker, jak funguje, mozny chyby**

5. **pseudoassmebler, struktura, bitfield**

6. **garbage collector ve funkcionalnich jazycich, jak funguje, nevyhody**

7. **popsat algoritmus SLD rezoluce**

8. **lambda**

9. **bonus popsat python**

### Další termín

1. **syntax, 4 odrážky ktorými ho môžme definovať, 2 chyby v C ktoré sa**

   **daju zachytiť pri preklade a niesu syntaktické ani sémantické**

2. **problémy pri ukladaní inštancií pri viacnásobnej dedičnosťi**

3. **Ako je definovaná štruktúra/záznam (nebolo to s rekurzivným použitím,**

   **niečo iné) + ešte nejaké veci vysvetliť**

4. **výnimky Exception s dvomi podtriedami ExA, ExB**

4a. **Exception, klasický try-catch-finally**

4b. **ExA, co ak sa pri obsluhe catch vyhodi dalsia vynimka?**

5. **robinson príklad**

6. **rysy pre funkcionalne a logické jazyky (2x3)**

7. **adapter (UML, kod) popis**

8. **uzavretý podprogram, 4 odrážky**

9. **Máme dva jazyky, jeden podporuje definiciu funkcie uprostred**

   **definicie funkcie a druhy podporuje len lokalne premenne a lokalne**

   **definicie funkcii... v ktorom z nich mozno na uzivatelskej urovni akosi**

   **"simulovat" pouzivanie globalnych premennych a aka vlastnost jazyka to**

   **povoluje (rozsah platnosti premennych)**

10. **lambda výraz (\s.(\ w u.w) s t)(\ z.z)**

### Další termín

1. **definice semantiky, 4 typove ruzne semanticke chyby ktere C detekuje pri prekladu (5b)**

2. **vlastnosti tridy OOJ s jednoducho ded. (4b)**

3. **try-catch (6b)**

4. **NV observer - nebyl konkretni priklad jen nakreslit UML + kod na zakladni funkcionalitu. Mohli jsme si vybrat jaky**

   **typ observera (8b)**

5. **2 vety o tom jak se vzajemne ovlivnuji moduly. Vybrat 1 a popsat prikladem? (4?b)**

6. **jak se predavajim parametry do podprogramu. Strucne ale vystizne jednotlive popsat**

7. **prakticky robinson (8b)**

#1

read(X, hi(S), nieco(V, U) )

read(256, U, nieco(X, Y) )

"read(256, hi(S), nieco(256, hi(S) )"

"read(256, hi(S), nieco(256, hi(S) )"

mgu = [256/X] o [hi(S)/U] o [256/V] o [hi(S)/Y]

#2

gain( mod(L,22), V, neviem(V, L) )

gain( X, X, neviem(V, L) )

"gain(mod(L,22), mod(L,22), neviem(mod(L,22), L) )"

"gain(mod(L,22), mod(L,22), neviem(mod(L,22), L) )"

mgu = [mod(L,22) / X] o [mod(L,22) / V]

8. **co je to ukazatel (3 slova). Jak ukazatel ovlivnuje architektura (3 odrazky max 10 slov celkem), co nese ukazatel**

   **(4b)**

9. **32bit architektura, pole {char, char, int}, kolik zabere mista v pameti se zarovnanim, kolik na tesno. Jak se**

   **dostaneme k intu (vypocet) (6b)**

10. **lambda kalk (6b)**

(\xy.xxy)(\xy.y)

(\y.(\xy.y)(\xy.y)y)

(\y.(\y.y)y)

\y.y
