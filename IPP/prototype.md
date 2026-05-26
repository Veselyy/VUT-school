
### **Příklad 1: Vnořené ošetření v dědičné hierarchii** 24+ výskytů

**Přesné zadání otázky:**
„Mějme třídní OOJ s podporou výjimek, kde třída výjimky **ExA** je přímou nadtřídou **ExB** a **ExB** je přímou nadtřídou **ExC**. V hlavním těle programu mějme trojici bloků `try-catch-finally` (vnější) následovanou kódem (vnější epilog). Vnější `catch` má formální parametr typu **ExA**. Uvnitř vnějšího `try`-bloku je vnořena trojice bloků `try-catch-finally` (vnitřní) následovaná kódem (vnitřní epilog). Vnitřní `catch` má parametr typu **ExC**. Uvažujme, že ve vnitřním `try`-bloku dojde k vyvolání výjimky třídy **ExB**. Popište přesně průběh ošetření výjimky (které části kódu se vykonají a které ne a proč).“

**Kódová podoba (pseudo-kód):**
```python
# Hierarchie: ExA -> ExB -> ExC
try: # VNĚJŠÍ
    try: # VNITŘNÍ
        raise ExB()              # 1. VYVOLÁNÍ VÝJIMKY
    catch ExC as e:              # 2. Vnitřní catch (typ ExC)
        print("Vnitřní ošetření")
    finally:                     # 3. Vnitřní finally
        print("Vnitřní finally")
    print("Vnitřní epilog")      # 4. Vnitřní epilog
catch ExA as e:                  # 5. Vnější catch (typ ExA)
    print("Vnější ošetření")
finally:                         # 6. Vnější finally
    print("Vnější finally")
print("Vnější epilog")           # 7. Vnější epilog
```

**Vypracování (vyřešení otázky):**
1.  **Vyvolání:** V bloku `try` vznikne **objekt (instance)** třídy `ExB`.
2.  **Vnitřní `catch(ExC)`:** Tento blok výjimku **nezachytí**, protože vyvolaná výjimka `ExB` není podtřídou `ExC` (v hierarchii je nad ní).
3.  **Vnitřní `finally`:** Tento blok se **vykoná vždy** (epilog ošetření), hned po neúspěšném pokusu o zachycení ve vnitřním bloku.
4.  **Vnitřní epilog:** Protože výjimka nebyla vnitřně ošetřena, **vnitřní epilog se neprovede** a výjimka se **propaguje** (šíří) do nadřazeného bloku.
5.  **Vnější `catch(ExA)`:** Vnější blok výjimku **úspěšně zachytí**, protože `ExB` je podtřídou `ExA` (do parametru se naváže instance výjimky).
6.  **Vnější `finally`:** Po opuštění vnějšího `catch` se opět **provede vnější `finally`**.
7.  **Vnější epilog:** Protože výjimka byla nyní ošetřena, model výpočtu se vrací do normálu a **vnější epilog se vykoná**.

---

### **Příklad 2: Propagace při znovu-vyvolání (Re-throw)** 24+ výskytů
Tento příklad se zaměřuje na situaci, kdy ošetřující kód výjimku záměrně propouští dále.

**Přesné zadání otázky:**
„Mějme metodu `m()`, ve které je struktura `try-catch-finally` následovaná dalším kódem (epilogem programu). V bloku `try` je volána metoda `k()`, která vyvolá výjimku **FileEx**. Třída **FileEx** dědí od třídy **Exception**. Blok `catch` specifikuje typ **Exception** a v jeho těle je příkaz `raise FileEx` (znovu-vyvolání). Popište, jakým způsobem se výpočet dokončí.“

**Kódová podoba (pseudo-kód):**
```python
def m():
    try:
        k()               # Metoda k() vyvolá FileEx
    catch Exception as e: # FileEx dědí od Exception
        raise FileEx()    # Znovu-vyvolání (re-throw)
    finally:
        printError()      # Finalizační blok
    
    print("Epilog m()")   # Epilog programu v rámci metody m
```

**Vypracování (vyřešení otázky):**
1.  **Vyvolání:** Metoda `k()` vyvolá výjimku `FileEx`. Standardní model výpočtu v `try` bloku je přerušen.
2.  **Zachycení:** Blok `catch Exception` výjimku **zachytí**, protože `FileEx` je podtřídou `Exception`.
3.  **Znovu-vyvolání:** Uvnitř `catch` bloku je výjimka pomocí `raise` vyvolána znovu. To znamená, že výjimka stále není považována za definitivně ošetřenou v rámci této metody.
4.  **Finalizace:** Následně se **vždy vykoná blok `finally`** (zavolá se `printError()`), i když z metody odchází neošetřená výjimka.
5.  **Výsledek:** Protože výjimka byla v `catch` bloku znovu vyvolána, **epilog programu (v rámci metody `m`) se neprovede**. Výjimka je **propagována** z metody `m()` do jejího volajícího prostředí.