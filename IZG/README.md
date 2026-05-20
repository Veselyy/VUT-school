# IZG – náhled na GitHubu

GitHub samotný `.html` soubor **nevyrenderuje jako stránku** (ukáže jen zdroják). Proto se náhled dělá přes **GitHub Pages**.

## Jak to spustit

1. Vygeneruj stránku:

```bash
python3 IZG/build_otazky.py
```

2. Na GitHubu zapni Pages:
- **Settings → Pages**
- **Build and deployment → Source: Deploy from a branch**
- **Branch: `main`**, **Folder: `/docs`**

3. Otevři náhled:
- adresa bude ve stylu `https://<user>.github.io/<repo>/izg/`

Generátor vytváří:
- `docs/izg/index.html`
- `docs/izg/images/…`

