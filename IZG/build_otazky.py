#!/usr/bin/env python3
"""Generate otazky.html from otazky.txt and IZG Ultimate Guide content."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC_HTML = ROOT / "otazky.html"
OUT = ROOT / "otazky.html"
TOPICS_FILE = ROOT / "otazky.txt"

# Styl textu odpovědí: uprostřed vět nepoužívat středník (;).
# Místo něj čárka, tečka, nová věta nebo další odrážka.

TABLE_CSS = """
    table { width: 100%; border-collapse: collapse; margin: 1em 0; }
    th, td { border: 1px solid #cbd5e1; padding: 0.4em 0.6em; }
    section.answer h3 {
      margin: 1.5rem 0 0.5rem;
      font-size: 1.12rem;
      font-weight: 700;
      color: #0f172a;
    }
    section.answer h3:first-of-type { margin-top: 0; }
"""

FIGURE_MAX_CSS = """
    section.figures {
      max-width: 750px;
      margin-left: auto;
      margin-right: auto;
    }
    figure img {
      width: auto;
      height: auto;
      max-width: min(750px, 100%);
      max-height: 350px;
      object-fit: contain;
      margin-left: auto;
      margin-right: auto;
    }
    .figure-grid figure img {
      max-width: 100%;
      max-height: 350px;
    }
"""

_CURRENT_FIGURE_MAX_CSS = re.compile(
    r"\s*section\.figures \{\s*max-width: 750px;[^}]+\}\s*"
    r"figure img \{[^}]+\}\s*"
    r"\.figure-grid figure img \{[^}]+\}",
    re.DOTALL,
)

_OLD_FIGURE_MAX_CSS = re.compile(
    r"\s*section\.figures,\s*section\.answer figure \{[^}]+\}\s*"
    r"section\.figures img,\s*section\.answer figure img \{[^}]+\}",
    re.DOTALL,
)

_PER_TOPIC_FIGURE_CSS = re.compile(
    r"\s*#q(?:05-opengl-pipeline|14-rgb-cmyk|28-multisampling-supersapling)"
    r"(?: \.figures| section\.answer figure)(?:[^{]|\n)*\{[^}]+\}"
    r"(?:\s*#q(?:05-opengl-pipeline|14-rgb-cmyk|28-multisampling-supersapling)"
    r"(?: \.figures img| section\.answer figure img)\s*\{[^}]+\})*",
    re.DOTALL,
)

TOPIC_IDS = [
    "q01-maticov-operace-vypo-t-n-sou-adnic-podle",
    "q02-raytracing",
    "q03-phong",
    "q04-st-nov-n",
    "q05-opengl-pipeline",
    "q06-jak-poznat-p-ivr-cenou-odvr-cenou-stranu",
    "q07-z-buffer",
    "q08-dkov-vyplnov-n",
    "q09-textury-u-3d-model",
    "q10-pined-v-algoritmus",
    "q11-vertex-fragment-shader",
    "q12-radiozita-vs-raytracing",
    "q13-aplikace-vytvo-en-operace-v-p-edchoz-m-b",
    "q14-rgb-cmyk",
    "q15-dda-s-fixed-point-aritmetikou",
    "q16-aditivni-substraktivni-model",
    "q17-pseudokod-vykresleni-krivky",
    "q18-alias",
    "q19-b-rep",
    "q20-mip-mapping",
    "q21-brassenham-v-algoritmus",
    "q22-parametrick-sm-rnicov-tvar-p-mky",
    "q23-algoritmus-de-casteljau",
    "q24-o-ez-weiler-artheton",
    "q25-textury-u-trojuhelniku",
    "q26-texturovac-sou-adnice",
    "q27-shannon-v-vzorkovac-teor-m",
    "q28-multisampling-supersapling",
    "q29-grafick-kontext",
    "q30-halftoning-dithering",
    "q31-perspektivni-vs-paralelni-projekce",
    "q32-barycentricke-souradnice",
    "q33-lambertuv-osvetlovaci-model",
    "q34-rovnice-k-ivky",
    "q35-paramertick-tvar-k-ivky",
]


def tier(count: int) -> str:
    if count >= 7:
        return "high"
    if count >= 3:
        return "medium"
    return "low"


def parse_topics() -> list[tuple[str, int]]:
    topics = []
    for line in TOPICS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(.+?)\s+(\d+)x\s*$", line, re.I)
        if not m:
            raise ValueError(f"Invalid topic line: {line!r}")
        topics.append((m.group(1).strip(), int(m.group(2))))
    if len(topics) != 35:
        raise ValueError(f"Expected 35 topics, got {len(topics)}")
    return topics


def extract_head_through_style() -> str:
    text = SRC_HTML.read_text(encoding="utf-8")
    end = text.find("</style>")
    if end == -1:
        raise ValueError("Missing </style> in otazky.html")
    head = text[: end + len("</style>")]
    if "table { width: 100%" not in head:
        head = head.replace("</style>", TABLE_CSS + "\n  </style>", 1)
    elif "section.answer h3" not in head:
        h3_css = """
    section.answer h3 {
      margin: 1.5rem 0 0.5rem;
      font-size: 1.12rem;
      font-weight: 700;
      color: #0f172a;
    }
    section.answer h3:first-of-type { margin-top: 0; }
"""
        head = head.replace("</style>", h3_css + "\n  </style>", 1)
    head = _PER_TOPIC_FIGURE_CSS.sub("", head)
    head = _OLD_FIGURE_MAX_CSS.sub("", head)
    if _CURRENT_FIGURE_MAX_CSS.search(head):
        head = _CURRENT_FIGURE_MAX_CSS.sub(FIGURE_MAX_CSS, head)
    elif "max-height: 350px" not in head:
        head = head.replace("</style>", FIGURE_MAX_CSS + "\n  </style>", 1)
    return head


P = "images/pdf/"
I = "images/"

# (answer_html, [(image_path, caption), ...])
TOPIC_DATA: list[tuple[str, list[tuple[str, str]]]] = [
    (
        """<p><strong>Transformace</strong> — zobrazení z jednoho prostoru do druhého.</p>
<ul>
<li><strong>Lineární transformace</strong> zachovává lineární kombinaci vektorů.</li>
<li><strong>Afinní transformace</strong> zachovává kolinearitu a dělící průměr, je to lineární transformace + posun.</li>
<li><strong>Homogenní souřadnice 2D:</strong> bod <code>[x, y]</code> → <code>[x, y, w]</code>, platí <code>x = X/w</code>, <code>y = Y/w</code>. Váha <code>w</code> určuje typ (bod/vektor).</li>
<li><strong>2D operace:</strong> posun, rotace, změna měřítka, zkosení — každá jako matice 3×3.</li>
<li><strong>Homogenní 3D:</strong> <code>[x, y, z, w]</code>, kde <code>w = 1</code> pro bod, <code>w = 0</code> pro vektor.</li>
<li><strong>3D operace:</strong> posun, rotace, měřítko, zkosení, viewport transformace.</li>
</ul>
<p>Aplikace na bod: násobení souřadnic translační/rotační maticí, po transformaci vydělit homogenní souřadnicí <code>w</code> (perspektiva).</p>""",
        [
            (f"{P}page05-img01.png", "Matice 2D transformací (posun, rotace, měřítko, zkosení)"),
        ],
    ),
    (
        """<p><strong>Poznámka k názvům:</strong> <em>casting</em> <em>vyslat / vrhnout</em> paprsek z kamery (jako „cast a ray“). <em>Tracing</em> pak opravdu znamená <em>sledovat / trasovat</em> další cestu světla po odrazu nebo lomu. Oba postupy paprsky vysílají, liší se hloubkou toho, co po prvním zásahu ještě počítají.</p>
<p>U obou metod jde o to, že z kamery (nebo pro každý pixel) vystřelíme paprsek do scény a zjistíme, na co narazí. To je společný základ.</p>
<p><strong>Ray casting</strong> u toho většinou zůstane u prvního zásahu: co je nejblíž, to vykreslíme, případně ještě zkontrolujeme stín (jestli na bod svítí zdroj, nebo je něco před ním). Jde hlavně o to <em>určit, co je vidět</em>, ne o složité chování světla.</p>
<p><strong>Ray tracing</strong> na tom staví víc vrstev: po dopadu paprsku posíláme další paprsky a barvu bodu skládáme i z odrazů a lomů. Výsledek vypadá věrohodněji, ale počítá se dál a déle.</p>
<p>Paprsky u ray tracingu (podle pořadí):</p>
<ul>
<li><strong>Primární</strong> — vycházejí z kamery, najdou první průsečík se scénou (co je na pixelu vidět).</li>
<li><strong>Sekundární</strong> — vycházejí z místa dopadu primárního paprsku po odrazu nebo lomu (zrcadlo, sklo, odlesk).</li>
<li><strong>Terciární</strong> — vycházejí z místa, kam dopadl sekundární paprsek, tedy další „odraz“ ve stromu paprsků (reálně může pokračovat i hlouběji, dokud nedosáhneme limitu).</li>
</ul>
<p>Zjednodušeně: ray casting = „co vidím“, ray tracing = navíc „co se tam ještě odráží a prosvítá“. V konverzaci se pojmy občas pletou, ray tracing je širší a ray casting je v něm často jen první krok.</p>""",
        [],
    ),
    (
        """<h3>Phongův osvětlovací model</h3>
<p>Empirický model — tři složky intenzity:</p>
<ol>
<li><strong>Ambientní</strong> — světelný šum, rozptýlené světelné pozadí (konstantní příspěvek).</li>
<li><strong>Difúzní (Lambert)</strong> — odraz do všech směrů, závisí na normále <code>N</code> a směru ke světlu <code>L</code> (<code>N · L</code>).</li>
<li><strong>Spekulární</strong> — lesklá složka podle zákona odrazu, závisí na směru odrazu a směru k pozorovateli, koeficient <code>R<sub>s</sub></code>, ostrost <code>N<sub>s</sub></code>.</li>
</ol>

<h3>Phong shading</h3>
<p>Při rasterizaci se <strong>interpolují normály</strong> z vrcholů po ploše polygonu. Osvětlovací model (Lambert, spekulární složka, …) se počítá <strong>pro každý pixel</strong> z interpolované normály v daném bodě. Velmi kvalitní výsledek, v OpenGL typicky přes fragment shadery (náročnější než Gouraud).</p>

<h3>Gouraud shading</h3>
<p>Osvětlení se počítá <strong>jen ve vrcholech</strong> trojúhelníku — u každého vrcholu normála a směr ke světlu, výsledek např. <code>Lambert(D+A)</code> (difúzní + ambientní složka). Barvy ve vrcholech se pak <strong>interpolují</strong> po ploše pomocí barycentrických vah <code>λ<sub>a</sub>, λ<sub>b</sub>, λ<sub>c</sub></code>. Rychlejší a jednodušší než Phong shading, ale u velkých ploch může být vidět Machův pruh (lesk se „rozmazá“ mezi vrcholy).</p>""",
        [
            (f"{I}phong-shading.png", "Phong shading — osvětlení se počítá pro každý pixel"),
            (f"{I}gouraud-shading.png", "Gouraud shading — osvětlení ve vrcholech, interpolace barev po ploše"),
        ],
    ),
    (
        """<p>Porovnání metod stínování polygonů:</p>
<table>
<thead><tr><th>Metoda</th><th>Princip</th><th>Kvalita / HW</th></tr></thead>
<tbody>
<tr><td><strong>Flat shading</strong></td><td>Barva z osvětlení ve středu polygonu, celý polygon konstantní</td><td>Nezohledňuje zakřivení, lehké, OpenGL</td></tr>
<tr><td><strong>Gouraud shading</strong></td><td>Osvětlení ve vrcholech, interpolace barev po ploše</td><td>Zakřivení ano, průměrné normály ve vrcholech, OpenGL</td></tr>
<tr><td><strong>Phong shading</strong></td><td>Interpolace normál, osvětlení po pixelech</td><td>Nejkvalitnější, shadery, náročnější</td></tr>
</tbody>
</table>""",
        [],
    ),
    (
        """<p><strong>OpenGL pipeline</strong> — transformace vrcholu z modelového prostoru do obrazovky:</p>
<ol>
<li><strong>Model-space</strong> <code>[x, y, z, 1]<sup>T</sup></code> × <strong>Model matrix</strong> (S, T, R — měřítko, posun, rotace) →</li>
<li><strong>World-space</strong> <code>[x′, y′, z′, 1]<sup>T</sup></code> × <strong>View / Eye matrix</strong> →</li>
<li><strong>View-space</strong> <code>[x″, y″, z″, 1]<sup>T</sup></code> × <strong>Projection matrix</strong> →</li>
<li><strong>Clip-space</strong> <code>[x‴, y‴, z‴, w‴]<sup>T</sup></code> — ořez: <code>−w‴ ≤ x‴,y‴,z‴ ≤ +w‴</code></li>
<li><strong>Perspective division</strong> (dělení <code>w‴</code>) → <strong>NDC</strong> <code>[x⁗, y⁗, z⁗, 1]<sup>T</sup></code>, souřadnice v <code>[−1, +1]</code></li>
<li><strong>Viewport transform</strong> → <strong>Screen-space</strong> (pixely ve framebufferu)</li>
</ol>
<p>Po transformaci vrcholů dál v pipeline:</p>
<ul>
<li>rasterizace vytvoří fragmenty</li>
<li>fragment shader určí barvu a texturu</li>
<li>z-buffer řeší viditelnost</li>
</ul>""",
        [(f"{I}opengl-pipeline.png", "Pipeline transformací: model → world → view → clip → NDC → screen")],
    ),
    (
        """<p>Viditelné plochy jsou orientované k pozorovateli — normála směřuje k pozorovateli.</p>
<p><strong>Test přivrácené strany:</strong> skalární součin vektoru <strong>pohledu</strong> <code>V</code> (od povrchu ke kameře) a <strong>normály</strong> <code>n</code> plochy:</p>
<ul>
<li><strong>Kladný výsledek</strong> <code>V · n &gt; 0</code> → plocha je <strong>přivrácená</strong> (viditelná z daného směru).</li>
<li><strong>Záporný</strong> → odvrácená (zadní strana), lze vynechat (back-face culling).</li>
</ul>
<ul>
<li>Hrana mezi dvěma viditelnými plochami je potenciálně viditelná.</li>
<li>Hrana mezi neviditelnými plochami je neviditelná.</li>
<li>Hrana mezi viditelnou a neviditelnou plochou je obrysová.</li>
</ul>""",
        [],
    ),
    (
        """<p><strong>Z-buffer</strong> — 2D pole (stejná velikost jako color buffer / framebuffer), ukládá hloubku <code>z</code> nejbližšího fragmentu, typicky float. Počítá se v GPU.</p>
<ol>
<li>O jakou datovou strukturu se jedná? → <strong>2D pole</strong></li>
<li>Jakou má velikost? → <strong>jako framebuffer</strong> (rozlišení obrazu)</li>
<li>Jaké hodnoty obsahuje? → <strong>Z souřadnice</strong> (hloubka) nejbližších bodů ploch</li>
<li>Kde se používá? → <strong>GPU</strong>, rasterizace</li>
<li>Pro jaké objekty je vhodný? → <strong>netransparentní polygony</strong> (trojúhelníky)</li>
<li>Řeší problém <strong>viditelnosti</strong> — který pixel se vykreslí, když se plochy překrývají</li>
</ol>""",
        [],
    ),
    (
        """<p><strong>Řádkové vyplňování</strong> (scan-line fill) — 4 kroky:</p>
<ol>
<li>Pro každý řádek oblasti vytvořit seznam souřadnic <code>x</code> průsečíků s hranami (vodorovné hrany vynechat).</li>
<li>Seřadit seznam podle <code>x</code>.</li>
<li>Vykreslit vodorovné úseky mezi lichým a sudým průsečníkem (1–2, 3–4, …).</li>
<li>Je-li počet průsečníků lichý, v lokálním extrému vykreslit úsek obou hran.</li>
</ol>
<p>Varianty: šrafování (přeskakování řádků), gradient (inkrement parametru po řádcích), inverzní řádkové vyplňování.</p>""",
        [(f"{P}page04-img01.png", "Řádkové vyplňování — průsečíky se scanline")],
    ),
    (
        """<p><strong>Textura</strong> — popis detailu povrchu nezávislý na geometrii, vzorek = texel.</p>
<p><strong>Typy:</strong></p>
<ul>
<li><strong>Datové</strong> — uložené v paměti, rychlé, náchylné k aliasu.</li>
<li><strong>Procedurální</strong> — dynamické, parametrické, méně aliasu, pomalejší.</li>
</ul>
<p><strong>Informace na textuře:</strong> barva, průhlednost, optické vlastnosti, normála (bump), geometrie (displacement), zrcadlení okolí, osvětlení.</p>
<p><strong>Mapování na 3D:</strong> inverzní analytické funkce (koule, válec), premietání z obalového tělesa, 3D textury (scale), UV mapování (rozvinutí „kůže“).</p>
<p><strong>Mapování povrchu:</strong></p>
<ul>
<li><strong>Bump mapping</strong> — optická změna normály</li>
<li><strong>Displacement mapping</strong> — skutečná změna geometrie</li>
<li><strong>Environment mapping</strong> — odraz okolí</li>
<li><strong>Light mapping</strong> — předpočítané světlo</li>
</ul>""",
        [],
    ),
    (
        """<p><strong>Pinedův algoritmus</strong> — vyplňování konvexní oblasti (nejčastěji trojúhelník).</p>
<ul>
<li>Oblast = seznam hran dělících rovinu na poloroviny.</li>
<li>Bod je uvnitř, leží-li na kladné straně <strong>všech</strong> polorovin (hranová funkce ≥ 0).</li>
<li><strong>Hranová funkce (edge function)</strong> <code>E<sub>i</sub></code> — vektorový součin směrového vektoru hrany a vektoru z počátku hrany do bodu <code>P</code>.</li>
<li>Je-li <code>E<sub>i</sub>(P) ≥ 0</code>, bod je uvnitř nebo na hranici.</li>
<li>Lze optimalizovat inkrementálně po řádcích/sloupcích bez přepočtu pro každý pixel.</li>
</ul>""",
        [
            (f"{I}pineda-algoritmus.png", "Pinedův algoritmus — hranové funkce E₁, E₂, E₃, pixel uvnitř jen když jsou všechny kladné"),
            (f"{P}page04-img03.png", "Průnik polorovin (edge funkce)"),
        ],
    ),
    (
        """<p><strong>Vertex shader</strong></p>
<ul>
<li>Běží na vertex procesoru, transformuje vrcholy primitiv (model, view, projekce).</li>
<li>Vstupy: built-in a user attribute/uniform proměnné.</li>
<li>Výstupy: varying proměnné pro rasterizátor (pozice, normály, UV, …).</li>
</ul>
<p><strong>Fragment shader</strong></p>
<ul>
<li>Operace nad fragmenty (kandidátní pixely), barva, textury, osvětlení ve výsledném renderu.</li>
</ul>
<p><strong>Rozdíl:</strong></p>
<ul>
<li><strong>Vertex shader</strong> — geometrická transformace do pipeline</li>
<li><strong>Fragment shader</strong> — finální vzhled každého pixelu</li>
</ul>""",
        [],
    ),
    (
        """<table>
<thead><tr><th></th><th>Ray-tracing</th><th>Radiozita</th></tr></thead>
<tbody>
<tr><td>Stíny</td><td>ostré</td><td>měkké</td></tr>
<tr><td>Odrazy okolí na povrchu</td><td>ano</td><td>ne</td></tr>
<tr><td>Sekundární osvětlení</td><td>ne</td><td>ano</td></tr>
<tr><td>Zdroje světla</td><td>bodové</td><td>plošné</td></tr>
<tr><td>Vhodná reprezentace</td><td>CSG</td><td>polygonální</td></tr>
<tr><td>Řeší viditelnost a zobrazení</td><td>ano</td><td>ne</td></tr>
</tbody>
</table>
<p>Ray-tracing je obrazová metoda. Radiozita je komplexní fyzikální metoda globálního osvětlení (měkké stíny, sekundární světlo) a neřeší přímo zobrazení.</p>""",
        [],
    ),
    (
        """<p>Aplikace matic z předchozího tématu na body:</p>
<ol>
<li>Bod v homogenních souřadnicích <code>[x, y, w]</code> nebo <code>[x, y, z, 1]</code>.</li>
<li>Násobení maticí transformace (posun, rotace, měřítko, složená matice).</li>
<li>Po perspektivní projekci: <strong>perspektivní dělení</strong> <code>x' = X/w</code>, <code>y' = Y/w</code> (příp. <code>z'</code>).</li>
</ol>
<p>Afinní transformace zachovává rovnoběžnost přímek, lineární část + translace. Složením matic lze řetězit operace v jednom kroku.</p>""",
        [
            (f"{P}page05-img02.png", "Matice posunu a měřítka ve 3D"),
            (f"{P}page05-img03.png", "Rotace, zkosení a viewport transformace"),
        ],
    ),
    (
        f"""<p><strong>RGB</strong> — aditivní míchání (světlo), základ Red, Green, Blue, max. intenzity = bílá. Monitory, projektory, kamery.</p>
<p><strong>CMYK</strong> — subtraktivní míchání (pigment), Cyan, Magenta, Yellow, Black (Key), max. = černá. Tisk.</p>
<p><strong>HSV</strong> — <strong>H</strong> odstín, <strong>S</strong> sytost, <strong>V</strong> světlost. Uživatelsky orientovaný model (barevná kolečka v editorech). Při úbytku <strong>V</strong> klesá i sytost, barva tmavne k černé.</p>
<figure>
<img src="{I}hsv-model.png" alt="HSV model — H po obvodu kruhu, S a V v trojúhelníku" loading="lazy" />
<figcaption>HSV: H po obvodu, S od bílé ke syté barvě, V od černé ke světlé</figcaption>
</figure>
<p><strong>HSL</strong> — stejné <strong>H</strong> a <strong>S</strong>, místo světlosti <strong>L</strong> jas (lightness). CSS, návrhové nástroje. Při <strong>L</strong> 0 % nebo 100 % klesá sytost na nulu (černá / bílá).</p>
<figure>
<img src="{I}hsl-model.png" alt="HSL — odstín, sytost a jas jako tři nezávislé osy" loading="lazy" />
<figcaption>HSL: H (0°–360°), S (0–100 %), L jas / světlost (0–100 %)</figcaption>
</figure>
<p>Převod do šedotónu: vážený průměr kanálů, prakticky 256 úrovní.</p>""",
        [(f"{P}page01-img01.png", "RGB a CMY — aditivní vs. subtraktivní model (krychle barev)")],
    ),
    (
        """<p><strong>DDA s fixed-point aritmetikou</strong> — rasterizace úsečky bez floatů, přírůstek <code>k</code> ve fixed-point reprezentaci.</p>
<pre><code>#define FRAC_BITS 8

LineDDAFixed(int x1, int y1, int x2, int y2) {
   int k = (y2 - y1) &lt;&lt; FRAC_BITS / (x2 - x1);
   int y = y1 &lt;&lt; FRAC_BITS;

   for (int x = x1; x &lt;= x2; x++) {
       draw_pixel(x, y &gt;&gt; FRAC_BITS);
       y += k;
   }
}</code></pre>
<p>Oproti float DDA: rychlejší na HW bez FPU, stejný princip — po <code>x</code> inkrementovat <code>y</code> o směrnici.</p>""",
        [],
    ),
    (
        """<p><strong>Aditivní model (RGB)</strong> — sčítání světelných složek, více světla = světlejší, bílá = složení max. R+G+B.</p>
<p><strong>Subtraktivní model (CMYK)</strong> — odčítání od bílého papíru pigmenty, více pigmentu = tmavší, černá = plné CMY + K.</p>
<p>RGB pro emisivní zařízení, CMYK pro tisk — fyzikálně odpovídají složení vs. filtrace světla.</p>""",
        [],
    ),
    (
        """<p>Pseudokód rasterizace úsečky (DDA) — první kvadrant, rostoucí úsečka:</p>
<pre><code>LineDDA(int x1, int y1, int x2, int y2) {
   double k = (y2 - y1) / (x2 - x1);
   double y = y1;

   for (int x = x1; x &lt;= x2; x++) {
       draw_pixel(x, round(y));
       y += k;
   }
}</code></pre>
<p>Pro křivky (De Casteljau): opakovaně dělit řídicí polygon v poměru <code>t</code> a <code>1−t</code>, spojovat body úsečkami pro různá <code>t</code>.</p>""",
        [],
    ),
    (
        """<p><strong>Aliasing</strong> — nežádoucí jev při nízkofrekvenčním vzorkování vysokofrekvenčního signálu (zubaté hrany, poruchy textur).</p>
<p><strong>Příčiny:</strong> příliš malá vzorkovací frekvence, příliš pravidelné nebo přesné vzorkování.</p>
<p><strong>Shannonův vzorkovací teorém:</strong> přesná rekonstrukce je možná, pokud je vzorkovací frekvence ≥ 2× maximální frekvence signálu.</p>
<p><strong>Řešení:</strong></p>
<ul>
<li>Zvýšení rozlišení (náročné).</li>
<li>Předfiltrování vstupu / supersampling (více vzorků na pixel, konvoluce).</li>
<li>Přefiltrování výstupu (postprocess, ztráta detailů).</li>
<li><strong>Multisampling</strong> — adaptivní supersampling hlavně u hran.</li>
</ul>""",
        [],
    ),
    (
        """<p><strong>B-rep (Boundary representation)</strong> — objekt popsaný povrchem (hranice), bez uložené vnitřní struktury.</p>
<ul>
<li>Skládá se z <strong>vrcholů</strong>, <strong>hran</strong> (úsečky, křivky) a <strong>stěn</strong> (polygony).</li>
<li><strong>Drátový model</strong> — málo informací, rychlý náhled.</li>
<li><strong>Polygonální model</strong> — jednoznačný, méně přesný, HW podpora.</li>
<li>Požadavky na model: obecnost, úplnost, jednoznačnost, přesnost, regulérnost, konzistence operací, kompaktnost.</li>
<li><strong>Manifold</strong> — každá hrana sdílena max. dvěma stěnami (vyrobitelný objekt).</li>
</ul>""",
        [],
    ),
    (
        """<p><strong>MIP mapping</strong> — řešení aliasu textur při zmenšení podle vzdálenosti od kamery.</p>
<ul>
<li>Více úrovní (mipmap) stejné textury: každá další má poloviční rozměr (32→16→8→…→1).</li>
<li>Uloženo v jedné větší 2D struktuře (např. 2× rozlišení původní textury).</li>
<li>Mohou být předgenerované na disku, při zmenšení vyhlazovací filtr.</li>
<li>Zrychlení texturování malých objektů, lepší vizuální kvalita.</li>
</ul>
<p>Perspektivní zkreslení UV: řešení dělením polygonů na menší části.</p>""",
        [],
    ),
    (
        """<p><strong>Bresenhamův (midpoint) algoritmus</strong> — celočíselná rasterizace úsečky.</p>
<pre><code>LineBres(int x1, int y1, int x2, int y2) {
   int dx = x2 - x1, dy = y2 - y1;
   int P = 2*dy - dx;
   int P1 = 2*dy, P2 = P1 - 2*dx;
   int y = y1;

   for (int x = x1; x &lt;= x2; x++) {
       draw_pixel(x, y);
       if (P &gt;= 0) { P += P2; y++; }
       else          P += P1;
   }
}</code></pre>
<p>Rozhodování o kroku v <code>y</code> pomocí prediktoru <code>P</code>, jen sčítání a porovnání — efektivnější než DDA s float.</p>""",
        [],
    ),
    (
        """<p><strong>Parametrický tvar přímky</strong> (s parametrem <code>t</code>):</p>
<p><code>P(t) = P<sub>1</sub> + t · (P<sub>2</sub> − P<sub>1</sub>)</code>, <code>t ∈ [0, 1]</code></p>
<p>Směrový vektor <code>u = (x<sub>2</sub>−x<sub>1</sub>, y<sub>2</sub>−y<sub>1</sub>)</code>.</p>
<p><strong>Směrnicový tvar</strong> (funkce <code>y = f(x)</code>):</p>
<p><code>y = q + k·x</code>, kde <code>k = dy/dx</code> je směrnice, <code>q</code> offset na ose Y.</p>
<p>Směrnicový tvar nejde pro svislé přímky, parametrický je obecnější.</p>""",
        [],
    ),
    (
        """<p><strong>Algoritmus de Casteljau</strong> — rekurentní vykreslení Bézierových křivek.</p>
<ol>
<li>Řídicí body polygonu, pro dané <code>t</code> dělit každou úsečku v poměru <code>t : (1−t)</code>.</li>
<li>Opakovat na novém polygonu, dokud nezůstane jeden bod — bod na křivce.</li>
<li>Pro různá <code>t</code> s krokem spojovat body úsečkami.</li>
</ol>
<p>U kubik: „divide and conquer“ — rekurzivní dělení na dvě podkřivky (<code>t = 0.5</code>), ukončit, když je křivka dostatečně rovná (vzdálenost &lt; úhlopříčka pixelu).</p>""",
        [],
    ),
    (
        """<p><strong>Weiler–Atherton</strong> — ořez polygonu oknem (obecné polygony, i s otvory).</p>
<p>Seznamy:</p>
<ul>
<li><code>P</code> — vrcholy a průsečíky na polygonu</li>
<li><code>W</code> — na okně</li>
<li><code>I</code> — vstupní průsečíky</li>
<li><code>O</code> — výstupní průsečíky</li>
<li><code>C</code> — ořez uvnitř okna</li>
<li><code>R</code> — odřezky venku</li>
</ul>
<ol>
<li>Průsečíky (např. Liang–Barsky).</li>
<li>Polygon celý uvnitř → do <code>C</code>.</li>
<li>Start v <code>P</code> na prvním vrcholu z <code>I</code>, střídat pohyb po <code>P</code> / <code>W</code> podle typu průsečíku.</li>
<li>Odřezky mimo okno → <code>R</code>, analogicky od prvního <code>O</code>.</li>
</ol>""",
        [],
    ),
    (
        """<p><strong>Texturování trojúhelníku</strong> — souřadnice textury v jednotlivých vrcholech, interpolace po ploše.</p>
<p>Příklad z guide (barva / textura v těžišti a na hranách):</p>
<ul>
<li><code>T(r,g,b) = ⅓(P<sub>1</sub>+P<sub>2</sub>+P<sub>3</sub>)</code> v těžišti.</li>
<li><code>C<sub>13</sub>(r,g,b) = ½(P<sub>1</sub>+P<sub>3</sub>)</code> na hraně.</li>
</ul>
<p>Obecně: <code>(u,v)</code> ve vrcholech → lineární interpolace <code>u,v</code> (a případně hloubka <code>z</code>) uvnitř polygonu, vzorkování texelu. U perspektivy je vhodné korektní perspektivní interpolace nebo dělení na menší trojúhelníky.</p>""",
        [(f"{I}image29.png", "Mapování textury na trojúhelník (UV souřadnice)")],
    ),
    (
        """<p><strong>Texturovací souřadnice (u, v)</strong></p>
<ul>
<li>Zadávají se <strong>ručně nebo automaticky</strong> u vrcholů sítě — dva floaty <code>u, v</code>.</li>
<li>Typicky <strong>0–1</strong> (normalizované) — pozice na 2D textuře.</li>
<li>Mezi vrcholy se <strong>lineárně interpolují</strong> po polygonech.</li>
<li>Definiční obor textury může být i <strong>3D prostorová textura</strong> <code>[x,y,z]</code>, normála, vektor odrazu (environment mapping), předpočítaná light mapa.</li>
</ul>""",
        [],
    ),
    (
        """<p><strong>Shannonův vzorkovací teorém:</strong> přesná rekonstrukce spojitého, frekvenčně omezeného signálu z diskrétního vzorku je možná tehdy, pokud byla vzorkovací frekvence <strong>alespoň dvojnásobkem</strong> maximální frekvence signálu (Nyquist: <code>f<sub>s</sub> ≥ 2·f<sub>max</sub></code>).</p>
<p>Porušení → aliasing. Řešení: vyšší vzorkování, předfiltrování (supersampling), vyhlazení výstupu.</p>""",
        [],
    ),
    (
        """<p><strong>Supersampling</strong> — předfiltrování, pixel rozdělen na více vzorků, výsledná barva = složení (konvoluční filtr), vyhlazí hrany i textury, vysoká cena.</p>
<p><strong>Multisampling</strong> — adaptivní supersampling, hustší vzorkování u hran a gradientů, méně u ploch, výrazné vyhlazení hran, menší pokles výkonu než plný supersampling.</p>""",
        [(f"{I}ssaa-msaa.png", "SSAA — vzorky ve všech pixelech, MSAA — více vzorků hlavně u hran trojúhelníku")],
    ),
    (
        """<p><strong>Grafický kontext</strong> — datová struktura pro kreslení na různá výstupní zařízení (display, bitmapa, PDF, soubor).</p>
<p><strong>Skládá se z:</strong></p>
<ul>
<li>Parametrů výstupního zařízení (formát obrazu).</li>
<li>Šířky a výšky kreslící plochy (včetně ořezu).</li>
<li>Transformace výstupu (device-independent kreslení).</li>
</ul>
<p>Cíl: jednotné API pro Window, Printer, Drawing, PDF atd.</p>""",
        [],
    ),
    (
        """<p><strong>Dithering</strong> — nahrazení stupňů šedi černobílými tečkami, zachová rozměr, výstup na obrazovku.</p>
<ul>
<li><strong>Prahování</strong> — podle prahu <code>T</code>, jednoduché, špatné u jemných přechodů.</li>
<li><strong>Náhodné rozptýlení</strong> — rychlé, zachová jasové poměry.</li>
<li><strong>Distribuce chyby</strong> (Floyd–Steinberg, Bayer, …) — chyba k sousedům.</li>
<li><strong>Maticové rozptýlení</strong> — porovnání s rozptylovací maticí.</li>
</ul>
<p><strong>Halftoning</strong> — každý pixel nahrazen vzorem černobílých bodů dané hodnoty, <strong>zvětšuje</strong> rozměr obrazu, výstup do tiskárny.</p>""",
        [
            (f"{P}page02-img04.png", "Dithering — rozptyl chyby"),
            (f"{I}halftoning-matice.png", "Halftoning — pixel obrázku porovnaný s maticí prahů, výstup 0 nebo 255, rozměr se zvětší"),
        ],
    ),
    (
        """<p><strong>Perspektivní projekce</strong></p>
<ul>
<li>Středová — paprsky se sbíhají v jednom bodě (kamera).</li>
<li>Nezachovává rovnoběžnost hran.</li>
<li>Vzdálenost od středu ovlivňuje velikost průmětu.</li>
</ul>
<p><strong>Paralelní (ortogonální) projekce</strong></p>
<ul>
<li>Rovnoběžné paprsky (často kolmé).</li>
<li>Zachovává rovnoběžnost.</li>
<li>Vzdálenost obvykle neovlivňuje velikost průmětu.</li>
</ul>
<p>Ortogonální: kvádr, perspektivní: jehlan.</p>""",
        [(f"{P}page07-img05.png", "Perspektivní projekční matice")],
    ),
    (
        """<p><strong>Barycentrické souřadnice</strong> — váhy <code>λ<sub>1</sub>, λ<sub>2</sub>, λ<sub>3</sub></code> vůči vrcholům trojúhelníku:</p>
<p><code>P = λ<sub>1</sub>P<sub>1</sub> + λ<sub>2</sub>P<sub>2</sub> + λ<sub>3</sub>P<sub>3</sub></code>, kde <code>λ<sub>1</sub>+λ<sub>2</sub>+λ<sub>3</sub> = 1</code>.</p>
<p>Bod je uvnitř, jsou-li všechny <code>λ<sub>i</sub> ≥ 0</code>. Výpočet z plošných nebo vektorových veličin (např. plochy dílčích trojúhelníků). Použití: interpolace barev, textur, normál uvnitř trojúhelníku.</p>""",
        [],
    ),
    (
        """<p><strong>Lambertův (difúzní) osvětlovací model</strong> — intenzita odraženého světla úměrná <code>cos θ</code>, kde <code>θ</code> je úhel mezi směrem světla <code>L</code> a normálou <code>n</code> (často <code>I ∝ max(0, L·n)</code>).</p>
<p>Na diagramu označte: zdroj světla, bod na povrchu, normálu <code>n</code>, směr k pozorovateli <code>V</code>, úhel <code>θ</code>. Difúzní odraz jde do všech směrů — pozorovatel vidí stejně (matný povrch).</p>""",
        [
            (f"{I}lambert-model.png", "Lambertův model — N, L, Dₛ = N·L·Bₛ·Bₘ, Aₛ = Bₘ·Bₐₛ"),
            (f"{P}page10-img01.png", "Difúzní odraz na kouli"),
        ],
    ),
    (
        """<p><strong>Rovnice křivky</strong> — polynomiální tvar, např. spline segmenty:</p>
<p><code>Q(t) = a t³ + b t² + c t + d</code> (kubika), koeficienty z okrajových podmínek (body, tečny).</p>
<p><strong>Typy:</strong> interpolační (prochází body), aproximační (řídicí body), racionální (váhy — invariantní k perspektivě), neracionální.</p>
<p><strong>Fergusonova kubika:</strong> 2 koncové body + 2 tečny, spojení C⁰/C¹. <strong>Bézier:</strong> Bernsteinovy polynomy, konvexní obal řídicích bodů.</p>""",
        [],
    ),
    (
        """<p><strong>Parametrický tvar křivky</strong> <code>Q(t)</code>:</p>
<p><code>Q(t) = (x(t), y(t))</code> nebo <code>Q(t) = P<sub>1</sub> + t(P<sub>2</sub> − P<sub>1</sub>)</code>, <code>t ∈ [0, 1]</code>.</p>
<p>Pro úsečku: <code>x(t) = x<sub>1</sub> + t(x<sub>2</sub>−x<sub>1</sub>)</code>, <code>y(t) = y<sub>1</sub> + t(y<sub>2</sub>−y<sub>1</sub>)</code>. U Bézierovy křivky stupně <code>n</code> je <code>n+1</code> řídicích bodů, <code>t</code> parametrizuje průběh po křivce.</p>""",
        [],
    ),
]


def figures_block(items: list[tuple[str, str]]) -> str:
    if not items:
        return ""
    body = "\n".join(
        f"""      <figure>
        <img src="{html.escape(s)}" alt="{html.escape(c)}" loading="lazy" />
        <figcaption>{html.escape(c)}</figcaption>
      </figure>"""
        for s, c in items
    )
    grid = ' class="figure-grid"' if len(items) > 1 else ""
    return f"""    <section class="figures" aria-label="Obrázky">
      <div{grid}>
{body}
      </div>
    </section>"""


def render_article(num: int, title: str, count: int, tid: str, answer: str, figs: list[tuple[str, str]]) -> str:
    t = tier(count)
    fig_html = figures_block(figs)
    return f"""  <article class="topic tier-{t}" id="{tid}">
    <header class="topic-header">
      <span class="topic-num" aria-hidden="true">{num}</span>
      <h2>{html.escape(title)}</h2>
      <span class="freq" title="Výskyt na zkouškách">{count}×</span>
    </header>

    <section class="answer" aria-label="Odpověď">
{answer}
    </section>
{fig_html}
  </article>"""


def render_toc(topics: list[tuple[str, int]]) -> str:
    lines = ['  <nav id="TOC" role="doc-toc">', "    <ul>"]
    for i, ((title, count), tid) in enumerate(zip(topics, TOPIC_IDS), start=1):
        t = tier(count)
        lines.append(
            f'      <li class="tier-{t}"><a href="#{tid}"><span class="toc-num">{i}.</span> '
            f"{html.escape(title)} <span class=\"toc-freq\">{count}×</span></a></li>"
        )
    lines.extend(["    </ul>", "  </nav>"])
    return "\n".join(lines)


def build() -> None:
    topics = parse_topics()
    if len(TOPIC_DATA) != 35:
        raise ValueError(f"TOPIC_DATA must have 35 entries, got {len(TOPIC_DATA)}")

    head = extract_head_through_style()
    articles = []
    for i, ((title, count), tid, (answer, figs)) in enumerate(
        zip(topics, TOPIC_IDS, TOPIC_DATA), start=1
    ):
        articles.append(render_article(i, title, count, tid, answer, figs))

    body = f"""{head}
</head>
<body>
  <header class="page-header">
    <h1 class="title">IZG — Příprava na zkoušku</h1>
    <p class="subtitle">35 nejčastějších témat · zdroj: IZG Ultimate Guide · seřazeno podle četnosti</p>
  </header>

  <p class="howto"><em>Zdroj:</em> IZG Ultimate Guide</p>

{render_toc(topics)}

{chr(10).join(articles)}

  <footer>
    Zdroj četnosti: <code>otazky.txt</code> · obsah: <code>IZG Ultimate Guide.txt</code>
  </footer>
</body>
</html>
"""
    OUT.write_text(body, encoding="utf-8")
    print(f"Wrote {OUT} ({len(body.splitlines())} lines)")


if __name__ == "__main__":
    build()
