# Hitzekarte Zürich – zoombare Überlagerung

Eine selbstständige Webseite, die die Zürcher Hitzekarte ("Gefühlte Temperatur")
zoombar über eine offene Strassenkarte legt.

## Benutzung
- Öffne `index.html` (Doppelklick, oder über einen lokalen Server). Internet wird
  nur für die Kartenkacheln und die Leaflet-Bibliothek (CDN) benötigt.
- **Deckkraft**: Schieberegler regelt die Transparenz der Hitzekarte.
- **Nur Hitze / Mit Relief**: schaltet zwischen der freigestellten Hitze-Ebene
  (Strassen scheinen durch) und dem Originalbild inkl. Reliefschattierung um.
- **Grundkarte** (oben rechts): CARTO hell, OpenStreetMap, swisstopo Farbe/Grau,
  Esri-Satellit.
- **Ausrichten**: zeigt Ziehgriffe, um die Hitzekarte pixelgenau auf die Strassen
  zu schieben/skalieren. Eck-Griffe = Grösse, gestrichelter Griff = verschieben.
  Die Ausrichtung wird im Browser (localStorage) gespeichert; **Zurücksetzen**
  stellt die Standard-Georeferenzierung wieder her.

## Baum-Analyse: «Welche Bäume kühlen?»
Aufklappbares Panel unten links (Klick auf den Titel). Datengrundlage:
**Baumkataster der Stadt Zürich** (Open Data, 81 068 Bäume; 78 337 davon liegen
im Hitze-Raster und erhalten einen verlässlichen Wert).

### Wie die Temperatur aus dem Bild gelesen wird
Laut Quelle (`vorgehen_article.txt`) zeigt die Karte **relative PET** (Abweichung
vom Stadt-Median), als deckende Farbe gerendert. Naïves «nächste-Farbe»-Matching
im RGB-Raum ist instabil (die Farbskala faltet sich durch den Raum → ein leicht
verfälschtes Orange «springt» zu Blau; das erzeugte die unsinnigen Ausreisser).
Stattdessen wird jeder Pixel auf die **monotone R−B-Achse** der Skala projiziert
(Rot-minus-Blau steigt durchgehend von kühl→heiss) und über die Legende auf
°C abgebildet. Anschliessend **räumliche Glättung** (~45 m, Auflösung des
Klimamodells), die Render-/Kompressionsrauschen entfernt. Grau/Wasser/Weiss
(keine Hitzedaten) werden maskiert.

> Validierung: dieselben 20 Bäume im Siriuspark streuten vorher **13 °C**,
> jetzt **0.9 °C**; Langstrasse liest sich heiss (36°), Irchelpark kühler (32°).

### Tab «Standort» (deskriptiv)
- **Punktfarbe = gefühlte Temperatur am Baumstandort** – dieselbe blau→rot-Skala
  wie die Hitzekarte (blau = kühler Standort, rot = heisser). Gradient-Legende im Panel.
- **Lokale Kühlung** = mittlere PET im 200‑m‑Umkreis minus PET am Baum.
  Im Schnitt stehen Bäume **0.34 °C kühler** als ihr Umkreis.
- **Kronengrösse entscheidet:** > 14 m Krone → ~1.1–1.8 °C kühlerer Standort,
  kleine Bäume kaum (~0.2 °C).
- Klick auf eine Gattung filtert die Karte; Klick auf einen Baum zeigt Details.

> ⚠︎ Korrelation: Weide, Fichte, Eibe stehen oft an ohnehin kühlen Lagen.

### Tab «Art-Effekt» (standortbereinigt)
Damit nicht Art und Lage verwechselt werden: jeder Baum wird *nur* mit Bäumen im
selben 150‑m‑Quartier **und** derselben Lagekategorie verglichen
(`Strassenbaum` ↔ `Strassenbaum`, `Parkbaum` ↔ `Parkbaum`). Kennzahl = PET am Baum
minus Mittel der gleichartigen Nachbarn (Leave-one-out). Knopf «alle Gattungen»
öffnet die vollständige, sortierte Liste.

- **Kontrolle:** Strassen-Standorte sind im selben Quartier **+0.46 °C** heisser
  als Park-Standorte – die Trennung ist nötig.
- **Lage war ein grosser Teil:** Fichte roh −1.04 °C → bereinigt ~0; Eibe ähnlich.
- **Robuster Art-Kühler:** **Weide** −0.34 °C (t ≈ −6.8, hoch signifikant).
- **Warm:** kleine Zier-/Heckengehölze – Thuja +0.44 °C, Weissdorn +0.34 °C (✱✱✱).
- ✱ = signifikant (✱ |t|>2, ✱✱ >2.6, ✱✱✱ >3.3).

### Tab «Schatten» (v2 – Kühl-/Schatten-Guide, literaturbasiert)
Unabhängig vom Hitzebild. Zeigt, welche Bäume **von Natur aus** am meisten kühlen
(Schatten + Verdunstung), nach Fachliteratur – ein Wegweiser «wo finde ich guten
Schatten?».

- Jede Gattung erhält einen **Literatur-Score 1–5** (Kronendichte/LAI + Transpiration),
  siehe `treedata/genus_cooling_literature.md`. Top: Linde, Platane, Ahorn,
  Rosskastanie, Hainbuche; Nadel- und kleine Zierbäume tief.
- **Karte:** Punktfarbe (grün-Skala) = *geliefertes* Potenzial = Gattungs-Score ×
  **heutige Kronengrösse** – ein grosser Baum spendet jetzt mehr Schatten als ein
  frisch gepflanzter. Beim Wechsel auf diesen Tab färbt sich die Baum-Ebene um.
- Auf eine Art klicken filtert die Karte; Baum-Popup zeigt das Kühlpotenzial.
- Heuristik (kein Vor-Ort-Messwert) – ergänzt die gemessenen Tabs, ohne deren
  Standort-Confounding.

### Daten neu erzeugen
`python3 treedata/build.py` (braucht `numpy` + `Pillow`) liest
`treedata/baumkataster.geojson` + das Hitzebild und schreibt
`tree_analysis`, `tree_within`, `trees_points` (je `.json` + `.js`).

## Dateien
| Datei | Zweck |
|-------|-------|
| `index.html` | komplette App (HTML + CSS + JS) |
| `zurich-desktop-light-de.webp` | Original-Hitzekarte (Quelle: Tages-Anzeiger) |
| `zurich-heat-masked.png` | freigestellte Hitze-Ebene (grauer Hintergrund transparent) |
| `legend.png` | Farb-Legende der gefühlten Temperatur |
| `vorgehen_article.txt` | Methodenbeschreibung der Originalkarte (PET, relativ) |
| `treedata/baumkataster.geojson` | Roh-Quelle: Baumkataster Stadt Zürich (OGD) |
| `treedata/build.py` | erzeugt die Analyse-Dateien neu |
| `treedata/genus_cooling_literature.md` | Literatur-Recherche + Score je Gattung (Basis Tab «Schatten») |
| `treedata/tree_analysis.*` | Gattungs-Rangliste (roh) + Kronen + Farbskala + `guide` (Literatur-Score) |
| `treedata/tree_within.*` | standortbereinigter Art-Effekt (Tab 2) |
| `treedata/trees_points.*` | 78 337 Bäume (Position, PET, Kühlung, Krone, Gattung) |
| `*.js` neben `*.json` | dieselben Daten als JS-Globals, damit die Seite auch per Doppelklick (`file://`) lädt – `fetch` ist dort blockiert |

## Georeferenzierung
Die Standard-Bounds wurden geometrisch an die Stadtgrenze angepasst
(Seitenverhältnis Bild ↔ Geografie stimmt auf 3 Nachkommastellen überein):
`S 47.31333 · W 8.38564 · N 47.45056 · E 8.67139`.
Da es sich um ein 2D-Reliefbild handelt, kann eine minimale Verschiebung bleiben –
dafür ist der **Ausrichten**-Modus gedacht.
