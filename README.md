# 🌡️🌳 Züriheat — Zürichs Hitze & die kühlenden Bäume

**🚀 Live-Demo: https://ginlennon.github.io/zueriheat/**

> Eine kleine, eigenständige Webseite, die Zürichs **Hitzekarte** («Gefühlte
> Temperatur») zoombar über eine offene Strassenkarte legt — und mit dem
> **Baumkataster** der Stadt verbindet, um zu fragen: 🌳 *Wo ist es heiss, wo kühl,
> und welche Bäume spenden den besten Schatten?*

---

## 🔥 Worum geht's?

In der Stadt ist Hitze **nicht gleich verteilt**: versiegelte Strassen und Plätze
glühen, Parks und Gewässer kühlen. Diese Karte macht das sichtbar 👀 — und lädt dazu
ein, die Rolle der **Stadtbäume** zu erkunden. Praktischer Nebeneffekt im Sommer:
ein kleiner **Schatten-Wegweiser** 🕶️.

## 🗺️ Was kann ich tun?

- 🔍 **Zoomen & schwenken** über die ganze Stadt, mit Strassennamen aus offenen Karten.
- 🎚️ **Deckkraft** der Hitze-Ebene regeln; zwischen **Nur Hitze** (Strassen scheinen
  durch) und **Mit Relief** umschalten.
- 🧭 **Grundkarte wählen** (oben rechts): CARTO hell, OpenStreetMap, swisstopo
  Farbe/Grau, Esri-Satellit.
- 🎯 **Ausrichten**: die Hitzekarte mit Ziehgriffen pixelgenau auf die Strassen
  schieben/skalieren (wird im Browser gespeichert).
- 🌳 **Bäume einblenden** (Panel unten links) und nach Gattung filtern; auf einen
  Baum klicken zeigt Details (Temperatur, Kühlung, Krone, Kühlpotenzial).

## 🌳 Die Baum-Analyse — drei Sichten

Aufklappbares Panel unten links (Klick auf den Titel 🔽). Datengrundlage:
**Baumkataster der Stadt Zürich** (81 068 Bäume; 78 337 davon liegen im Hitze-Raster).

### 📍 Tab «Standort» (deskriptiv)
- 🎨 **Punktfarbe = gefühlte Temperatur am Baumstandort** — dieselbe blau→rot-Skala
  wie die Hitzekarte (🔵 kühl, 🔴 heiss).
- ❄️ **Lokale Kühlung** = mittlere Temperatur im 200‑m‑Umkreis minus am Baum.
  Im Schnitt stehen Bäume **0.34 °C kühler** als ihr Umfeld.
- 👑 **Kronengrösse entscheidet:** > 14 m Krone → ~1.1–1.8 °C kühlerer Standort.
- ⚠️ *Korrelation, nicht Kausalität* — Weide/Fichte/Eibe stehen oft an ohnehin kühlen Lagen.

### 🧪 Tab «Art-Effekt» (standortbereinigt)
Jeder Baum wird **nur mit Bäumen im selben 150‑m‑Quartier und derselben Lage**
verglichen (Strassenbaum ↔ Strassenbaum, Parkbaum ↔ Parkbaum) — so fällt heraus,
*wo* eine Art wächst, übrig bleibt der Art-Effekt.
- 🚦 Strassen-Standorte sind im selben Quartier **+0.46 °C** heisser als Park-Standorte.
- 🍃 Robuster Kühler: **Weide** −0.34 °C (hoch signifikant). Kleine Zier-/Heckengehölze
  (Thuja, Weissdorn) markieren eher **wärmere** Punkte.

### 🌿 Tab «Schatten» (Kühl-Guide, literaturbasiert)
Unabhängig vom Hitzebild: welche Bäume **von Natur aus** am meisten kühlen
(Schatten + Verdunstung), nach Fachliteratur 📚.
- 🏆 Top: **Linde, Platane, Ahorn, Rosskastanie, Hainbuche**; Nadel- & kleine
  Zierbäume tief.
- 🟢 Karten-Farbe (grün) = Gattungs-Score × **heutige Kronengrösse** → wo steht jetzt
  guter Schatten.

## 🧠 Wie ist das entstanden?

1. 🧩 **Georeferenzierung** der Hitzekarte: geometrisch an die Stadtgrenze angepasst
   (Bild- ↔ Geo-Seitenverhältnis stimmen auf 3 Nachkommastellen).
2. 🎨 **Farbe → Temperatur:** Die Karte zeigt *relative* PET als deckende Farbe.
   Naïves «nächste-Farbe»-Matching ist instabil — deshalb wird jeder Pixel auf die
   **monotone R−B-Achse** der Farbskala projiziert und über die Legende auf °C
   abgebildet, dann **räumlich geglättet** (~45 m). 
   - ✅ *Validierung:* dieselben 20 Bäume im Siriuspark streuten vorher **13 °C**,
     jetzt **0.9 °C**.
3. 🌳 **Verschneidung** mit dem Baumkataster und drei Analysen (siehe oben).
4. ⚙️ Alles wird von [`treedata/build.py`](treedata/build.py) erzeugt; die Seite ist
   ein einziges `index.html` + ein paar Daten-Dateien (kein Build-Tool nötig).

## 🙏 Danke! — Inspiration, Daten & Werkzeuge

Dieses Hobby-Projekt steht komplett auf den Schultern offener Daten und Arbeit anderer 💚:

- 💡 **Inspiration & Hitzekarte:** der Tages-Anzeiger-Artikel
  [«Hitzewelle Schweiz — wo es in den Städten am heissesten ist»](https://www.tagesanzeiger.ch/hitzewelle-schweiz-wo-es-in-den-staedten-am-heissesten-ist-877255459625).
  Die Hitzedaten beruhen auf kantonalen **Klimamodellen** (PET, gefühlte Temperatur).
- 🌳 **Baumdaten:** [Baumkataster der Stadt Zürich](https://data.stadt-zuerich.ch/dataset/geo_baumkataster)
  (Open Government Data) — danke an **Grün Stadt Zürich** & das OGD-Team.
- 🗺️ **Grundkarten:** [OpenStreetMap](https://www.openstreetmap.org/copyright) (© Mitwirkende),
  [swisstopo](https://www.swisstopo.admin.ch/) (OGD), [CARTO](https://carto.com/) &
  [Esri World Imagery](https://www.esri.com/).
- 🧰 **Bibliothek:** [Leaflet](https://leafletjs.com/) — die freundlichste Karten-Lib. 🍃
- 📚 **Wissenschaft:** u. a. Rahman et al. (München: Linde kühlt bis **3.5 °C**) und
  weitere Studien — vollständige Liste & Scores in
  [`treedata/genus_cooling_literature.md`](treedata/genus_cooling_literature.md).

## 🛠️ Selbst ausführen / Daten neu erzeugen

```bash
# einfach öffnen (Doppelklick) oder lokal servieren:
python3 -m http.server 8000   # → http://localhost:8000
# Analyse-Daten neu bauen (braucht numpy + Pillow):
python3 treedata/build.py
```

Internet wird nur für **Kartenkacheln** und **Leaflet** (CDN) benötigt; die
Baum-Daten liegen als `*.js`-Globals daneben, damit es auch per Doppelklick
(`file://`) lädt.

## 📁 Dateien

| Datei | Zweck |
|-------|-------|
| `index.html` | 🌐 komplette App (HTML + CSS + JS) |
| `zurich-desktop-light-de.webp` | 🔥 Original-Hitzekarte (© Tages-Anzeiger) |
| `zurich-heat-masked.png` | ✂️ freigestellte Hitze-Ebene (Hintergrund transparent) |
| `legend.png` | 🌈 Farb-Legende der gefühlten Temperatur |
| `vorgehen_article.txt` | 📝 Methoden-Notiz der Originalkarte (PET, relativ) |
| `treedata/baumkataster.geojson` | 🌳 Roh-Quelle: Baumkataster Zürich (OGD) |
| `treedata/build.py` | ⚙️ erzeugt alle Analyse-Dateien |
| `treedata/genus_cooling_literature.md` | 📚 Literatur + Kühl-Score je Gattung |
| `treedata/tree_analysis.*` | 📊 Gattungs-Rangliste + Kronen + Farbskala + Literatur-Score |
| `treedata/tree_within.*` | 🧪 standortbereinigter Art-Effekt |
| `treedata/trees_points.*` | 📍 78 337 Bäume (Position, PET, Kühlung, Krone, Gattung) |

## ⚠️ Kleingedrucktes

- Die Hitzewerte sind aus einem **gerenderten Bild** geschätzt (±1–2 °C, *relativ*) —
  gut fürs Erkunden & Vergleichen, kein amtlicher Messwert.
- Das Hitzebild ist © **Tages-Anzeiger** und hier nur zu nicht-kommerziellen
  Analyse-/Demo-Zwecken eingebunden; die **MIT-Lizenz** dieses Repos gilt für den
  Code, nicht für dieses Bild.
- Gebaut mit viel ☕ und [Claude Code](https://claude.com/claude-code) 🤖.
