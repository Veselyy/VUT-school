# Study guide — globální workflow

## Nový předmět

```bash
python3 tools/study-guide/new_subject.py IPK "IPK — Příprava na zkoušku" --web
```

### Ty edituješ

| Položka | Popis |
|---------|--------|
| `otazky.md` | Otázky, odpovědi, Mermaid |
| `vyskyty.txt` | Krátký název pro obsah + `14x` — jeden řádek = jedno `##` v MD (pořadí musí sedět). V HTML se obsah i otázky řadí podle počtu výskytů (sestupně). |
| `podklady/` | Poznámky, PDF |
| `obrazky/` | Obrázky |
| `predmet.json` | Titul, `github_pages.slug` |
| `predmet.css` | Volitelné extra CSS předmětu |

### Build vygeneruje

| Položka | Popis |
|---------|--------|
| `_build.json` | Auto config (needitovat) |
| `otazky.html` | Lokální náhled |
| `web/<slug>/` | Webová verze v repu |

```bash
python3 tools/study-guide/build.py IPK
make build-all
```

Vygenerované HTML se na konci buildu formátuje přes [Prettier](https://prettier.io) (`prettier` v PATH, jinak `npx prettier@3.5.3`). Konfigurace: `tools/study-guide/.prettierrc.json`.

Kontrola (pre-commit nebo ručně): `make check-html`.

## GitHub Pages

Build zapisuje do **`web/`** (intuitivní název).

GitHub vyžaduje složku **`docs/`**. `make build-all` ji naplní automaticky (`pages-sync`: kopie `web/` → `docs/`). Ručně jen při potřebě: `make pages-sync`.

Pak Settings → Pages → branch `main`, folder **`/docs`**. Po změně diagramů: `make build-all`, commit `docs/` (`git add -f docs/`), push.

## Styly (jen HTML)

Jeden globální soubor `tools/study-guide/theme.css`. Vygenerované HTML na něj jen odkazuje (`<link>`), CSS se do souboru nekopíruje.

| Otevření | Cesta k CSS |
|----------|-------------|
| `<KÓD>/otazky.html` | `../tools/study-guide/theme.css` |
| `web/<slug>/index.html` | `../assets/study-guide/theme.css` (kopie při buildu) |

Volitelně `<KÓD>/predmet.css` jako druhý `<link>`. Markdown v editoru bez vlastního CSS.

## IZG

Stejný workflow jako IPP: `otazky.md` + `vyskyty.txt` → `python3 tools/study-guide/build.py IZG` → `web/izg/`.

## Staré názvy

Build podporuje dočasně: `priprava_na_zkousku.md`, `cetnosti.txt`, `study.config.json`.
