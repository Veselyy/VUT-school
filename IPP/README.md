# IPP — příprava na zkoušku

## Co edituješ

| Soubor | Účel |
|--------|------|
| `otazky.md` | Otázky a odpovědi |
| `vyskyty.txt` | Krátké názvy v obsahu + výskyty (`35x`), řádek = jedna otázka v `otazky.md`. V HTML se řadí podle výskytů. |
| `podklady/`, `obrazky/` | Materiály a obrázky |
| `predmet.json` | Titul a slug pro `web/ipp/` |

## Build

```bash
./build.sh
```

Vygeneruje `_build.json`, `otazky.html` a `web/ipp/`.

[Workflow](../tools/study-guide/README.md)
