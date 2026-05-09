# IPP — přesná znění (PDF otázky/odpovědi) a definice z opor

Tento soubor slouží jako **jedno místo** pro doslovné citace z materiálů ve složce `IPP/`. Text je převzat z extrahovaného obsahu PDF (občas drobné kódování typu znak `ÿ` v originálu je zjednodušeno).

---

## 1. Z `all_questions_answers.pdf` (sbírka „IPP Půlsemestrálky – Otázky a odpovědi“)

### Záhlaví dokumentu

```text
IPP Půlsemestrálky – Otázky a odpovědi (všechny roky)
2025
```

### Deklarace vs. definice (blok A3 / obdobné ročníky)

```text
3) Deklarace vs definice.
Deklarace – vymezuje atributy entity (jméno, typ, signatura). Nealokuje paměť, neobsahuje tělo
funkce. Může být explicitní i implicitní.
Proměnná: extern int x;
Funkce: int f(int, double);
Definice – vymezuje atributy entity a navíc: u proměnné zahrnuje alokaci paměti (příp. inicializaci), u
funkce navíc tělo (implementaci).
Proměnná: int x = 54;
Funkce: int f(int i, double d) { return i + (int)d; }
V kontextu OOP: rozhraní obsahuje pouze deklarace metod, třída obsahuje definice metod.
```

### Sémantika + dvě věci za běhu v C (blok A4)

```text
3) Sémantika + 2 věci vyhodnocované za běhu v C.
Sémantika = popis/definice významu jednotlivých syntaktických konstrukcí, způsobu jejich vyhodnocení a
zpracování. Dělí se na statickou (při překladu) a dynamickou (za běhu).
2 věci vyhodnocované za běhu v C (dynamická sémantika):
Kontrola indexu pole – pokud je index dán výrazem, nelze ověřit při překladu, zda nepřekročí
hranice
Dereference ukazatele – zda ukazatel neukazuje na neplatnou/uvolněnou paměť (NULL, dangling
pointer)
```

### `struct` v paměti (blok B4)

```text
4) C struct v paměti + výhody/nevýhody.
Položky struktury se ukládají za sebou v pořadí deklarace jako souvislý blok paměti. Překladač může
vkládat výplňové bajty (padding) mezi položky kvůli zarovnání (alignment) – každá položka na adrese
dělitelné její velikostí (požadavek architektury procesoru).
Přístup k položce = bázová adresa struktury + offset dané položky. Rozdíl oproti přístupu k proměnné:
k proměnné přistupujeme přímo přes její adresu, u struktury je navíc krok výpočtu offsetu.
Výhody: logické seskupení souvisejících dat, efektivní přístup přes staticky známý offset, heterogenní
data v jednom celku. Nevýhody: padding může plýtvat pamětí, pořadí položek ovlivňuje velikost, nelze
dynamicky měnit strukturu.
```

### Šest vlastností proměnné + PHP za běhu (blok C4 / 2025)

```text
4) Vlastnosti proměnné + co ovlivnit za běhu v PHP.
6 vlastností proměnné: jméno, adresa/umístění v paměti, typ, hodnota, doba života, rozsah platnosti.

Za běhu v PHP lze ovlivnit:
Typ – přiřazením hodnoty jiného typu, PHP je dynamicky typovaný ( $x = 5; $x = "ahoj"; )
Hodnotu – přiřazením nové hodnoty
Dobu života – voláním unset($x) pro explicitní zrušení; deklarací static v rámci funkce pro
prodloužení
Rozsah platnosti – klíčové slovo global ve funkci zpřístupní globální proměnnou v lokálním
rozsahu
Nelze ovlivnit: jméno, adresu/umístění (řeší interpret).
```

### Union v C (odkaz v pdf např. „2024 E4“)

```text
4) Union v C.
Variantní záznam ukládá všechny položky přes sebe (na stejné adrese) – ne za sebou! Velikost = velikost
největší položky. Použití: úspora paměti (jen jedna aktivní položka v daný moment), reinterpretace
bitového vzoru hodnoty.
```

### Rozsah platnosti + Python (odkaz „2024 E5“)

```text
5) Rozsah platnosti + Python.
Rozsah platnosti = ta část programu, kde s proměnnou lze pracovat. Souvisí s viditelností – platná
proměnná může být skryta jinou stejného jména.
Python – pravidlo LEGB: Local (uvnitř funkce) → Enclosing (vnější funkce) → Global (modul) → Built-in
(vestavěné).
```

*(Oficiální znění zkouškové otázky FIT za konkrétní termín máš doslovně v `priprava_na_zkousku.md` u sekce **24–25**.)*

---

## 2. Z opory `IPP-I-ESF-1_1.pdf` (Kolář — klasifikace jazyků, strukturované jazyky, …)

### Vlastnosti proměnné (výčet včetně scope)

```text
Nejdříve vyjmenujme studované vlastnosti proměnné:
• jméno;
• adresa a umístění/lokace v paměti;
• hodnoty, jichž může nabývat;
• typ;
• doba života;
• rozsah platnosti (scope).
```

### Definice 2.3.4 — doba života proměnné

```text
Definice 2.3.4 Doba života proměnné je časový interval, po který
je pro danou proměnnou alokována paměť.
Alokace opět může probíhat staticky, tj. před během programu,
nebo dynamicky. Dynamická alokace může být automatická (lokální
proměnné), nebo explicitně nějakým příkazem (dynamické proměnné
na haldě).
```

### Definice 3.3.1 — otevřený podprogram

```text
Definice 3.3.1 Otevřený podprogram je uložen v rámci hlavního
(často jediného) zdrojového textu. Nemá definované pevné rozhraní,
tzn. vstupní a výstupní bod, parametry, výsledek apod. Vstup se děje
skokem na příkaz, jímž má výpočet podprogramu začít, ukončení pod-
programu je dáno vyvoláním příslušného příkazu (nikoliv doběhnutím
výpočtu do/za určité místo).
```

### Uzavřené podprogramy (textová „definice“ spíše charakteristika v kapitole 4.3)

```text
• vznik uzavřených podprogramů — dramatický milník, který
zjednodušuje:
– rekurzi — vůbec první přímočará možnost implementace
rekurze;
– ukrytí implementace před ostatním programovým kó-
dem — nelze náhodně do kódu přistoupit, jediný vstupní
bod, jasně definované rozhraní vstupu/výstupu (parametry,
výsledek);
– odluka od hlavního toku programu — jednodušší a
bezpečnější modifikace, explicitní vyvolání, atd.;
```

---

## 3. Z opory `IPP-III-ESF-1_0.pdf` (Kolář — λ-kalkul, kapitola 3)

### Úvod ke kapitole λ-kalkul

```text
Kapitola 3
λ-kalkul
Lehký a stručný úvod do λ-kalkulu, který je formální bázi funk-
cionálních programovacích jazyků, je jediným obsahem této kapitoly.
```

### Definice 3.1.1 — syntaxe (BNF)

```text
Definice 3.1.1
<λ-výraz> ::= proměnná
| (<λ-výraz> <λ-výraz>)
| (λ<proměnná> . <λ-výraz>)
```

### Aplikace a abstrakce (volný výklad)

```text
λ-výraz tvaru (<λ-výraz> <λ-výraz>) nazýváme λ-aplikace, či apli-
kace, pokud nemůže dojít k záměně. [...]
Výraz tvaru (λ<proměnná> . <λ-výraz>) nazýváme λ-abstrakce, či
abstrakce. Tyto výrazy reprezentují funkce s jednou vázanou proměn-
nou (hlavičkou abstrakce) a tělem, které je opět tvořeno λ-výrazem;
pokud nějaká operace vyžaduje více parametrů, tak bezprostředním
vnořením λ-abstrakcí dosáhneme výsledku. Toto je jediný λ-výraz,
který je možné aplikovat (účelně).
```

### Redukce α, β, η (sekce 3.3)

```text
• α-konverze: libovolná abstrakce tvaru λV.E může být reduko-
vána na abstrakci λV ′.E[V ′/V ]. Zápis E[V ′/V ] označuje substi-
tuci proměnné V ′ za volné výskyty proměnné V ve výrazu E,
přičemž substituce musí být platná. Pojmem platná rozumíme,
že při substituci E[E′/V ] se žádná volná proměnná ve výrazu E′
nestane vázanou.
• β-konverze: libovolná aplikace tvaru (λV.E1)E2 může být redu-
kována na E1[E2/V ], pokud je substituce platná.
• η-konverze: libovolná abstrakce tvaru λV.(EV ), kde V není volné
v E, může být redukována na E.
```

### Redex

```text
Výraz, který je možné podle nějaké redukce změnit budeme na-
zývat redex podle zkratky z anglických slov „reducible expression“. redex
Jedná-li se o redex podle příslušné konverze, tak se nazývá α-, β-, či
η-redexem.
```

---

## 4. Opora `IPP-II-ESF-1_3b_hyperlinks.pdf`

Ve složce je **IPP-II** (OO principy, ς-kalkul, UML). Pro případné doplnění doslovných definic použij přímo PDF — kapitoly dle obsahu (např. základní pojmy OOP, minimální model výpočtu) nejsou v tomto souboru přepsány celé, aby nevznikala zbytečná duplicita k přednáškám.

---

*Citace odpovídají verzím PDF uvedeným v názvech souborů v repozitáři. Při aktualizaci opor zkontroluj stránkování a číslování definic v novější verzi.*
