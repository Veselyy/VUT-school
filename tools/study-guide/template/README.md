# {{CODE}} — příprava na zkoušku

## Co edituješ ty

| Soubor / složka | Účel |
|-----------------|------|
| `otazky.md` | Všechny otázky, odpovědi, Mermaid |
| `vyskyty.txt` | Krátký název do obsahu + kolikrát na zkoušce (`Název 14x`) |
| `podklady/` | Poznámky, PDF |
| `obrazky/` | Obrázky pro Markdown |
| `predmet.json` | Titul stránky, slug pro `web/` |
| `predmet.css` | Volitelné extra CSS |

## Co generuje build

| Soubor | Účel |
|--------|------|
| `_build.json` | Automatická konfigurace (needitovat) |
| `otazky.html` | Náhled v prohlížeči |
| `web/{{SLUG}}/` | Online verze (po push na GitHub) |

## Build

```bash
python3 tools/study-guide/build.py {{CODE}}
```

Globální styl: `tools/study-guide/theme.css`
