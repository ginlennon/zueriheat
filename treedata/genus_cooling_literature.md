# Cooling potential per tree genus — literature reference (for v2)

This file collects **published** knowledge on how much different tree genera cool
their surroundings. It is the intended basis for a future map layer ("where are the
trees that *should* cool most → shade-hunting guide"), **independent** of the
heat-image-derived analysis in the app (that one, *version 1*, is confounded by
location because the heat raster is too coarse to isolate a single tree).

## How trees cool (and which traits matter)
Two mechanisms: **shade** (blocking shortwave radiation) and **transpiration**
(latent-heat / evaporative cooling). Meta-analyses agree the single most
influential trait is **canopy density / Leaf Area Index (LAI)**, together with
**crown size/height** and **transpiration rate**.

- **Broadleaf deciduous ≫ conifer/evergreen** for *summer* cooling: higher LAI,
  higher transpiration, lighter canopy albedo. Conifers can even retain heat.
- **Diffuse-porous ≫ ring-porous** xylem for transpiration (when water is available).
  - Diffuse-porous (high transpiration): *Tilia, Acer, Fagus, Carpinus, Betula,
    Populus, Salix, Liriodendron, Liquidambar.*
  - Ring-porous (lower transpiration, often more drought-tolerant): *Robinia,
    Quercus, Fraxinus, Gleditsia, Ulmus, Celtis, Castanea, Sophora.*
- **Trade-off:** the strongest coolers (dense, high-transpiration, e.g. *Tilia*)
  often need water; the most **drought-resilient** "future trees" (e.g. *Gleditsia,
  Celtis, Sophora, Robinia*) tend to have lighter canopies → **less** cooling.

## Quantitative anchors
- *Tilia cordata* (small-leaved lime): up to **3.5 °C** daytime air-temperature
  reduction under canopy; ~30 % higher LAI and ~**3× the transpiration** of
  *Robinia pseudoacacia* (Munich, Rahman et al.).
- Cooling order in one comparison (by negative sensible-heat flux / LAI):
  **Tilia cordata > Acer platanoides > Platanus × acerifolia**.
- Mixed deciduous + some evergreen in open morphology ≈ +0.5 °C more cooling than
  a single-species planting.

## Heuristic cooling-potential score per genus
Score 1–5 (5 = strongest summer cooling). Combines typical **canopy density/LAI**,
**mature crown size**, and **transpiration (porosity)**. This is a literature-based
*heuristic*, not a measurement — meant to rank genera for a "best coolers" overlay.
Genera taken from the Zürich Baumkataster.

| Genus (lat) | Deutsch | Score | Why |
|---|---|---|---|
| Tilia | Linde | 5 | diffuse-porous, dense crown, very high transpiration — classic top cooler |
| Platanus | Platane | 5 | very large dense canopy, strong shade, good transpiration |
| Acer (platanoides/pseudoplatanus) | Ahorn | 4–5 | diffuse-porous, dense, large |
| Aesculus | Rosskastanie | 4 | large dense crown, strong shade |
| Fagus | Buche | 4 | very dense canopy / high LAI (but drought-sensitive) |
| Populus | Pappel | 4 | fast, high transpiration, large (but short-lived/messy) |
| Carpinus | Hainbuche | 4 | dense canopy, good shade, medium size |
| Salix | Weide | 3–4 | very high transpiration **near water**, open canopy otherwise |
| Quercus | Eiche | 3–4 | ring-porous (less transpiration) but large dense crown |
| Ulmus | Ulme | 3–4 | historically dense; modern hybrids vary |
| Fraxinus | Esche | 3 | moderate canopy & transpiration |
| Juglans | Walnuss | 3 | large crown, medium density |
| Liquidambar / Liriodendron | Amberbaum / Tulpenbaum | 3 | medium-large, decent LAI |
| Celtis | Zürgelbaum | 3 | drought-tolerant, medium canopy |
| Sophora (Styphnolobium) | Schnurbaum | 2–3 | drought-tolerant, lighter canopy |
| Gleditsia | Gleditschie | 2 | deliberately **light/open** canopy → low shade (but resilient) |
| Betula | Birke | 2 | light, airy canopy → modest shade |
| Ginkgo | Ginkgo | 2 | open-ish medium crown |
| Pinus/Picea/Abies/Larix | Kiefer/Fichte/Tanne/Lärche | 2 | conifers: low summer cooling, heat retention |
| Taxus/Thuja/Chamaecyparis | Eibe/Lebensbaum/Scheinzypresse | 1–2 | dense but small/hedge, low transpiration |
| Prunus/Malus/Pyrus | Zier-Kirsche/Apfel/Birne | 1–2 | small ornamental crowns, low LAI |
| Magnolia/Cornus/Crataegus/Corylus/Sorbus/Parrotia/Ostrya/Koelreuteria | Magnolie/Hartriegel/Weissdorn/Hasel/Eberesche/Parrotie/Hopfenbuche/Blasenbaum | 1–2 | small understory/ornamental → weak cooling |
| Ilex | Stechpalme | 1 | small evergreen shrub-tree |

> Note: v1's *measured* "warm" end (Crataegus, Malus, Magnolia, Thuja) matches the
> low scores here — i.e. small low-LAI trees genuinely cool little. v1's "cool" end
> (Picea/Taxus) was a **location** artifact: literature says conifers are weak
> summer coolers. So the heuristic above is the more trustworthy guide to a tree's
> *own* cooling.

## v2 idea
Colour/score each Baumkataster tree by this genus potential **× mature crown size**
(both in the cadastre) → a "supposed-to-cool-most" map. Lets a user find the best
shade nearby and lets planners see where strong vs weak coolers stand. Keep v1 as a
separate, clearly-labelled descriptive tab.

## Sources
- Comparing the relative abilities of tree species to cool the urban environment —
  Urban Ecosystems 21:851 (2018). https://link.springer.com/article/10.1007/s11252-018-0761-y
- Rahman et al., Comparing transpirational & shading effects of two contrasting urban
  tree species (Tilia cordata vs Robinia pseudoacacia) — Urban Ecosystems (2020).
  https://link.springer.com/article/10.1007/s11252-019-00853-x
- Traits of trees for cooling urban heat islands: a meta-analysis — Building &
  Environment (2019). https://www.sciencedirect.com/science/article/abs/pii/S0360132319308182
- Cooling efficacy of trees across cities… — Comms Earth & Environment (2024).
  https://www.nature.com/articles/s43247-024-01908-4
- The influence of tree traits on urban ground surface shade cooling — Landscape &
  Urban Planning (2020). https://www.sciencedirect.com/science/article/abs/pii/S0169204619309338
- GALK "Zukunftsbäume für die Stadt" / Straßenbaumliste.
  https://galk.de/arbeitskreise/stadtbaeume/themenuebersicht/zukunftsbaeume-fuer-die-stadt/
- CityTreeSuit (FVA Baden-Württemberg) — climate-suitability tool. https://www.citytreesuit.de
