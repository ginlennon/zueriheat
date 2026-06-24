#!/usr/bin/env python3
"""Rebuild tree-cooling analysis from the heat raster + Baumkataster.

The heat .webp encodes RELATIVE PET (deviation from city median), rendered with
a blue->red colormap. Per-pixel nearest-colour decoding is fragile (the colormap
folds through RGB space), so we project each pixel onto the colormap's monotonic
R-B axis and map that to the legend's temperature scale, then spatially smooth
(NaN-aware, ~20 m) to match the climate model's resolution and remove render noise.
"""
import json, numpy as np
from collections import defaultdict, Counter
from PIL import Image

def winsum(a, r):
    """Sum over a (2r+1)x(2r+1) window via integral image, edge-clamped."""
    P=np.zeros((a.shape[0]+1,a.shape[1]+1)); P[1:,1:]=a.cumsum(0).cumsum(1)
    H,W=a.shape
    y0=np.clip(np.arange(H)-r,0,H); y1=np.clip(np.arange(H)+r+1,0,H)
    x0=np.clip(np.arange(W)-r,0,W); x1=np.clip(np.arange(W)+r+1,0,W)
    return (P[np.ix_(y1,x1)]-P[np.ix_(y0,x1)]-P[np.ix_(y1,x0)]+P[np.ix_(y0,x0)])

HERE = __file__.rsplit('/',1)[0]
ROOT = HERE + '/..'

# ---- 1. legend: temperature <-> R-B curve -------------------------------
leg = np.asarray(Image.open(f'{ROOT}/legend.png').convert('RGB')).astype(int)
sat = leg.max(2)-leg.min(2); x0,x1 = 41,365; grad=[]
for x in range(x0,x1+1):
    best=None;bs=-1
    for y in range(88,104):
        c=leg[y,x];s=sat[y,x]
        if s>bs and not(c[0]<60 and c[1]<60 and c[2]<60): bs=s;best=c
    if best is not None and bs>20:
        grad.append((22+(x-x0)/(x1-x0)*22.0, best[0],best[1],best[2]))
g=np.array(grad); legT=g[:,0]; legRB=g[:,1]-g[:,3]; legRGB=g[:,1:4]

# ---- 2. heat raster -> smoothed relative-PET field ----------------------
img = np.asarray(Image.open(f'{ROOT}/zurich-desktop-light-de.webp').convert('RGB')).astype(int)
H,Wpx,_ = img.shape
chroma = img.max(2)-img.min(2)
RB = (img[:,:,0]-img[:,:,2]).astype(float)
valid = chroma>22                                  # colored heat data (not grey/water/white)
lo,hi = np.percentile(RB[valid],1), np.percentile(RB[valid],99)
def rb_to_T(rb):
    s=(rb-lo)/(hi-lo)
    return np.interp(legRB.min()+s*(legRB.max()-legRB.min()), legRB, legT)
Traw = rb_to_T(RB)
R=2                                                # ~45 m window, matches model res
num = winsum(np.where(valid,Traw,0.0), R)
den = winsum(valid.astype(float), R)
frac = den/((2*R+1)**2)                            # local fraction of valid pixels
Tsm = np.where(den>0, num/np.maximum(den,1e-6), np.nan)
support = frac>0.15
print(f"valid heat pixels {100*valid.mean():.1f}%  ;  city PET range "
      f"{np.nanpercentile(Tsm,2):.1f}..{np.nanpercentile(Tsm,98):.1f} °C")

S,Wl,N,El = 47.31333,8.38564,47.45056,8.67139
def to_px(la,ln):
    x=np.clip(((ln-Wl)/(El-Wl)*Wpx).astype(int),0,Wpx-1)
    y=np.clip(((N-la)/(N-S)*H ).astype(int),0,H-1); return x,y
def field(la,ln):
    x,y=to_px(np.asarray(la),np.asarray(ln)); return Tsm[y,x], support[y,x]

# ---- 3. trees -----------------------------------------------------------
feats=json.load(open(f'{HERE}/baumkataster.geojson'))['features']
lat=np.array([f['geometry']['coordinates'][1] for f in feats])
lng=np.array([f['geometry']['coordinates'][0] for f in feats])
genus=np.array([f['properties'].get('baumgattunglat') or '?' for f in feats])
crown=np.array([f['properties'].get('kronendurchmesser') or 0 for f in feats],float)
kat=np.array([f['properties'].get('kategorie') or '?' for f in feats])
namede=[f['properties'].get('baumnamedeu') or '' for f in feats]
def germ(gen):
    full=[namede[i].split(',')[0].strip() for i in np.where(genus==gen)[0] if namede[i]]
    if not full: return str(gen)
    for nm,_ in Counter(full).most_common():
        if 1<=len(nm.split())<=2: return nm
    return Counter(full).most_common(1)[0][0]

t_tree,ok = field(lat,lng)

# local cooling: mean PET on a 200 m ring minus PET at the tree
mlat,mlng = 111000.0, 111320*np.cos(np.radians(47.38))
ang=np.linspace(0,2*np.pi,16,endpoint=False)
ring=np.full((len(feats),16),np.nan)
for i,a in enumerate(ang):
    tt,oo=field(lat+200*np.sin(a)/mlat, lng+200*np.cos(a)/mlng)
    ring[oo,i]=tt[oo]
ring_mean=np.nanmean(ring,1); ring_n=np.sum(~np.isnan(ring),1)
cooling=ring_mean-t_tree
good = ok & (ring_n>=6) & np.isfinite(cooling) & np.isfinite(t_tree)
print(f"trees with reliable PET: {int(good.sum())} of {len(feats)} "
      f"({100*good.mean():.0f}%)  mean cooling {np.nanmean(cooling[good]):+.2f} °C")

# ---- 4. raw ranking by genus + crown bins ------------------------------
rows=[]
for gen in np.unique(genus[good]):
    m=(genus==gen)&good; n=int(m.sum())
    if n<200: continue
    cm=crown[m]
    rows.append(dict(genus=str(gen),de=germ(gen),n=n,
        cooling=round(float(cooling[m].mean()),3),
        temp=round(float(t_tree[m].mean()),2),
        crown=round(float(cm[cm>0].mean()) if (cm>0).any() else 0,1)))
rows.sort(key=lambda r:-r['cooling'])
cw=crown[good]; co=cooling[good]; okc=cw>0; cb=[]
for a,b in zip([0,4,7,10,14,20],[4,7,10,14,20,40]):
    s=okc&(cw>=a)&(cw<b)
    if s.sum()>50: cb.append(dict(lo=a,hi=b,n=int(s.sum()),cooling=round(float(co[s].mean()),3)))
analysis=dict(meta=dict(nTrees=int(good.sum()),
    meanCooling=round(float(cooling[good].mean()),3),
    petLo=round(float(np.nanpercentile(t_tree[good],5)),1),
    petHi=round(float(np.nanpercentile(t_tree[good],95)),1)),
    genera=rows, crownBins=cb)

# ---- 5. environment-controlled effect (cell x kategorie) ----------------
dlat,dlng = 150/111000.0, 150/(111320*np.cos(np.radians(47.4)))
ci=np.floor(lat/dlat).astype(int); cj=np.floor(lng/dlng).astype(int)
byst=defaultdict(list)
for i in range(len(feats)):
    if good[i]: byst[(int(ci[i]),int(cj[i]),kat[i])].append(i)
dev=np.full(len(feats),np.nan); MIN=6; nst=0; used=0
for s,idx in byst.items():
    if len(idx)<MIN: continue
    nst+=1; t=t_tree[idx]; tot=t.sum(); k=len(idx)
    for j,i in enumerate(idx): dev[i]=t[j]-(tot-t[j])/(k-1); used+=1
# street vs park within the same neighbourhood
cellb=defaultdict(list)
for i in range(len(feats)):
    if good[i]: cellb[(int(ci[i]),int(cj[i]))].append(i)
diffs=[]
for c,idx in cellb.items():
    st=[t_tree[i] for i in idx if kat[i]=='Strassenbaum']; pk=[t_tree[i] for i in idx if kat[i]=='Parkbaum']
    if len(st)>=2 and len(pk)>=2: diffs.append(np.mean(st)-np.mean(pk))
wrows=[]
for gen in np.unique(genus):
    m=(genus==gen)&np.isfinite(dev); n=int(m.sum())
    if n<150: continue
    x=dev[m]; mean=x.mean(); se=x.std(ddof=1)/np.sqrt(n); cm=crown[m]
    wrows.append(dict(genus=str(gen),de=germ(gen),n=n,dev=round(float(mean),3),
        se=round(float(se),3),t=round(float(mean/se),1),
        crown=round(float(cm[cm>0].mean()),1) if (cm>0).any() else 0))
wrows.sort(key=lambda r:r['dev'])
within=dict(streetVsPark=round(float(np.mean(diffs)),2),nStrata=nst,nTrees=used,genera=wrows)
print(f"controlled: {nst} strata, street vs park +{within['streetVsPark']} °C")

# ---- 5b. LITERATURE-based cooling potential per genus (v2 shade guide) ---
# Heuristic 1-5 score (canopy density/LAI + transpiration), see
# treedata/genus_cooling_literature.md. Independent of the heat image.
GENUS_SCORE={
 'Tilia':5.0,'Platanus':5.0,'Acer':4.5,'Aesculus':4.0,'Fagus':4.0,'Populus':4.0,
 'Carpinus':4.0,'Paulownia':3.5,'Salix':3.5,'Quercus':3.5,'Ulmus':3.5,'Castanea':3.5,
 'Fraxinus':3.0,'Juglans':3.0,'Liquidambar':3.0,'Liriodendron':3.0,'Celtis':3.0,
 'Sophora':2.5,'Styphnolobium':2.5,'Robinia':2.5,'Koelreuteria':2.5,'Ostrya':2.5,
 'Gleditsia':2.0,'Betula':2.0,'Ginkgo':2.0,'Pinus':2.0,'Picea':2.0,'Abies':2.0,
 'Larix':2.0,'Sorbus':2.0,'Parrotia':2.0,'Tetradium':2.0,
 'Taxus':1.5,'Thuja':1.5,'Chamaecyparis':1.5,'Prunus':1.5,'Malus':1.5,'Pyrus':1.5,
 'Magnolia':1.5,'Cornus':1.5,'Crataegus':1.5,'Corylus':1.5,'Ilex':1.0}
DEFAULT_SCORE=2.5
medcrown={}
for gen in np.unique(genus):
    cm=crown[genus==gen]; cm=cm[cm>0]
    medcrown[str(gen)]=float(np.median(cm)) if len(cm) else 7.0
def shade_score(gen,cr):
    gq=(GENUS_SCORE.get(str(gen),DEFAULT_SCORE)-1)/4.0          # 0..1 intrinsic
    c=cr if cr>0 else medcrown.get(str(gen),7.0)
    cf=min(max(c/16.0,0.2),1.15)                                 # delivered-shade factor
    return gq*cf                                                 # 0..~1.15
sh=np.array([shade_score(genus[i],crown[i]) for i in range(len(feats))])
sh_p95=float(np.percentile(sh[good],95)) or 1.0

# genus guide ranking (intrinsic literature score), for genera present in the city
guide=[]
for gen in np.unique(genus[good]):
    m=(genus==gen)&good; n=int(m.sum())
    if n<150: continue
    cm=crown[m]
    guide.append(dict(genus=str(gen),de=germ(gen),n=n,
        score=GENUS_SCORE.get(str(gen),DEFAULT_SCORE),
        crown=round(float(cm[cm>0].mean()),1) if (cm>0).any() else 0))
guide.sort(key=lambda r:(-r['score'],-r['n']))
analysis['guide']=guide
analysis['guideNote']="Literatur-Score 1-5 (Kronendichte/LAI + Transpiration), unabh. vom Hitzebild."
print("GUIDE top:", [(r['de'],r['score']) for r in guide[:6]])

# ---- 6. write outputs (json + js global) --------------------------------
idx=np.where(good)[0]
genlist=[r['genus'] for r in rows]; gmap={gx:i for i,gx in enumerate(genlist)}
pts=dict(lat=[round(float(lat[i]),5) for i in idx], lng=[round(float(lng[i]),5) for i in idx],
    t=[int(round(t_tree[i]*10)) for i in idx], c=[int(round(cooling[i]*100)) for i in idx],
    cr=[int(crown[i]) for i in idx], g=[gmap.get(str(genus[i]),-1) for i in idx],
    s=[int(round(min(sh[i]/sh_p95,1.0)*100)) for i in idx],     # 0..100 delivered shade
    genera=genlist, generaDe=[r['de'] for r in rows])
# colormap stops for the page (T -> hex), sampled from the legend
def hexat(T):
    r=int(np.interp(T,legT,legRGB[:,0])); gg=int(np.interp(T,legT,legRGB[:,1])); b=int(np.interp(T,legT,legRGB[:,2]))
    return f'#{r:02x}{gg:02x}{b:02x}'
analysis['colormap']=[[round(float(T),1),hexat(T)] for T in np.linspace(legT.min(),legT.max(),12)]

def dump(name,obj,var):
    json.dump(obj, open(f'{HERE}/{name}.json','w'), ensure_ascii=False)
    open(f'{HERE}/{name}.js','w').write(f'window.{var}='+json.dumps(obj,ensure_ascii=False)+';')
dump('tree_analysis',analysis,'__ANALYSIS__')
dump('tree_within',within,'__WITHIN__')
dump('trees_points',pts,'__TREES__')
print("wrote tree_analysis / tree_within / trees_points (.json + .js) to treedata/")
print("\nRAW top:   ", [(r['de'],r['cooling']) for r in rows[:5]])
print("CONTROLLED cool:", [(r['de'],r['dev'],r['t']) for r in wrows[:5]])
print("CONTROLLED warm:", [(r['de'],r['dev'],r['t']) for r in wrows[-4:]])
