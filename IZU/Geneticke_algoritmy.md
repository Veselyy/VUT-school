## Genetika
- Algoritmy jsou inspirovány přírodou.
- Používají se pro řešení optimalizačních úloh.

### Genetické algoritmy (GA)
- **Chromozomy a geny:** Každý jedinec má v buňkách **chromozomy** složené z genů, které mohou mít různé formy.
- **Genotyp a fenotyp:** Soubor všech forem určují vnější znaky jedince (**fenotyp**) jako je například barva očí.
- Buňky člověka mají **chromozomy**, který tvoří páry a v každém páru je jeden chromozon mateřského a druhý otcovského původu.
- **Mutace:** Náhodné změny genů způsobené vnějšími vlivy např. zářením.

### Princip GA
- Chromozomy jsou nejčastěji reprezentovány **řetězci znaků**, ale mohou být i grafy, matice, čísla, ....
- **Kombinace** jednotlivých znaků v chromozomu může být **optimální řešení** dané úlohy.
1. **Populace** je množina všech jedinců
   - **Jedinci** počáteční/výchozí populace **se generují náhodně**, ale může být i proto použita **heuristika**.
   - **Cílem** GA je najít chromozom, který je **(sub)optimálním řešením** dané optimalizační úlohy.
<p align="center">
  <img width="465" height="636" alt="image" src="https://github.com/user-attachments/assets/7dcc70de-4614-435d-a6c7-832c82399fce" />
  <br>
  <b>Obrázek 1:</b> <i>Model genetického algoritmu</i>
</p>

2. **Fitness funkce** udává kvalitu řešení chromozomu.
   - **Kvalita populace** je dána **průměrem fitness funkcí** všech jedinců populace a postupem času by se měla **zvětšovat**.
4. **Výběr rodičů:**
   - **Výběr elity:** Vyberou se podle nejlépe hodnocení jedinci.
   - **Turnajový výběr:** Z náhodně vybrané skupiny zvítězí nejlepší jedinec.
4. **Křížení:** Vytváření nových jedinců výměnou částí chromozomů rodičů v náhodně zvolených místech křížení.

<p align="center">
  <img width="315" height="158" alt="image" src="https://github.com/user-attachments/assets/b12fc971-6cb0-4289-b50f-f2438f6345b3" />
  <br>
  <b>Obrázek 2:</b> <i>Jednobodové křížení</i>
</p>

5. **Mutace:** Náhodná změna hodnoty vybraného genu u potomka.
6. **Nová populace:** K nahrazení staré populace se používají modely:
  - **generační** (výměna všech)
  - **inkrementační** (výměna jednoho)
  - modely **s překrytím** generací
### Ukončení výpočtu
1. Nalezení optimálního řešení.
2. Kvalita populace se po delší dobu nezvyšuje.
3. Dosažení maximálního stanoveného počtu iterací.

### Příklad
- Tento příklad demonstruje činnost genetického algoritmu na triviální úloze **hledání hodnoty proměnné x**, pro kterou **funkce y=5−x** prochází nulou.
- Zde je stručný popis postupu:
- **Nastavení**: Algoritmus pracuje s populací čtyř jedinců, jejichž chromozomy tvoří čtyři binární geny reprezentující celé kladné číslo **x**. Kvalita řešení se měří fitness funkcí definovanou jako **f=8−∣y∣**.
- **Počáteční stav**: První generace je vytvořena náhodně (hodnoty x: 12, 3, 7, 9) a její průměrná zdatnost (fitness) je vypočtena na 4,25.

<p align="center">
  <img width="443" height="224" alt="image" src="https://github.com/user-attachments/assets/5c6273c8-f867-407d-8f46-b22810eb912e" />
  <br>
  <b>Obrázek 3:</b> <i>1. krok</i>
</p>

- **Průběh:**
    - **Výběr:** Pomocí **turnajového výběru** jsou zvoleni rodiče pro novou generaci (vítězí jedinci s vyšší fitness).
    - **Křížení:** Dochází k výměně částí chromozomů rodičů v náhodně zvolených místech.
    - **Nová generace:** Vznikne nová populace, jejíž průměrná kvalita se v prvním kroku zvýšila na 4,5.

<p align="center">
  <img width="464" height="450" alt="image" src="https://github.com/user-attachments/assets/39e1a5bc-2512-4ead-aad2-8983a8a75eb2" />
  <br>
  <b>Obrázek 4:</b> <i>2. krok</i>
</p>

---

<p align="center">
  <img width="573" height="443" alt="image" src="https://github.com/user-attachments/assets/48456ca1-5a36-4196-a372-85ffd38ac221" />
  <br>
  <b>Obrázek 5:</b> <i>poslední krok</i>
</p>

  - **Výsledek:** Proces pokračuje dalšími turnaji a křížením, dokud není v další generaci nalezen chromozom **0101 (x=5)**, což je hledané optimální řešení s maximální hodnotou **fitness 8.** 
