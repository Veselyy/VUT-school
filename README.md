# VUT-school

Studijní materiály FIT VUT — jednotný styl a build.

## Nový předmět

```bash
python3 tools/study-guide/new_subject.py IPK "IPK — Příprava na zkoušku" --web
```

**Ty edituješ:** `otazky.md`, `vyskyty.txt`, `podklady/`, `obrazky/`, `predmet.json`

**Build vygeneruje:** `_build.json`, `otazky.html`, `web/<slug>/`

```bash
make build-all
```

## Pre-commit (formát HTML)

```bash
pip install pre-commit   # jednorázově
pre-commit install
```

Před každým commitem se zkontrolují **všechny** `*.html` v repu (Prettier, stejná config jako build). Oprava: `make build-all` nebo `make check-html`.

## Složka `web/`

Online verze příprav (po buildu). Lokálně otevři `IPP/otazky.html` nebo `web/ipp/index.html`.

Pro **GitHub Pages** (vyžaduje `docs/`): `make pages-sync`

## Předměty

| Složka | Build |
|--------|-------|
| [IPP](IPP/) | `make build-ipp` |
| [IZG](IZG/) | `make build-izg` (stejný workflow jako IPP) |

[Dokumentace](tools/study-guide/README.md)
