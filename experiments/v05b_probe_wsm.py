import io, math, requests, pandas as pd, numpy as np
URL='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'
r=requests.get(URL,timeout=120); r.raise_for_status()
print('download bytes',len(r.content))
df=pd.read_csv(io.BytesIO(r.content),low_memory=False)
print('shape',df.shape)
print('columns',list(df.columns))
lat=pd.to_numeric(df['LAT'],errors='coerce'); lon=pd.to_numeric(df['LON'],errors='coerce'); sh=pd.to_numeric(df['AZI'],errors='coerce')
qtxt=df['QUALITY'].astype(str).str.strip().str.upper()

def axmean(vals,weights=None):
    vals=np.asarray(vals,float); ok=np.isfinite(vals); vals=vals[ok]
    if weights is None: weights=np.ones(len(vals))
    else: weights=np.asarray(weights,float)[ok]
    a=np.radians(vals*2); sw=np.sum(weights)
    if sw<=0:return (np.nan,np.nan)
    x=np.sum(weights*np.cos(a)); y=np.sum(weights*np.sin(a))
    return (math.degrees(math.atan2(y,x))/2)%180, math.hypot(x,y)/sw

# saved v0.4a values for validation
expected={
(-57.5,-177.5):(262,85.09130418742329,.7882591814872301,.7881709084109542),
(-57.5,-97.5):(4,110.12065764194668,.7101704846889094,.0387818888325161),
(-57.5,-92.5):(7,90.1676576510564,.7514888837425525,.0986012247446064),
(-57.5,-82.5):(35,70.99305880582439,.7897581423979111,.5270732969167363),
(32.5,-137.5):(1,26.0,1.0,.0465106909946826),
(32.5,-132.5):(942,8.883681050844334,.6219368825399855,.6219366530407853),
(32.5,97.5):(1532,44.22921741434799,.2597942118132781,.2597942118132781),
(32.5,102.5):(1543,82.49560043660331,.2152421079317725,.2152421079317725),
(-27.5,97.5):(3,125.52847500235684,.8904004853405388,.188911188447912),
(2.5,162.5):(20, None, None,None),
}
weight_maps={
 'all1':{'A':1,'B':1,'C':1,'D':1,'E':1},
 'dropE':{'A':1,'B':1,'C':1,'D':1,'E':0},
 'linear':{'A':1,'B':.8,'C':.6,'D':.3,'E':0},
 'angle':{'A':1,'B':.75,'C':.5,'D':.125,'E':0},
 'sq':{'A':1,'B':.64,'C':.36,'D':.09,'E':0},
}
for (la,lo),exp in expected.items():
    dlon=((lon-lo+180)%360)-180
    m=(abs(lat-la)<=2.5)&(abs(dlon)<=2.5)&sh.notna()
    sub=df.loc[m].copy(); vals=pd.to_numeric(sub['AZI'],errors='coerce').to_numpy(); quals=sub['QUALITY'].astype(str).str.strip().str.upper().to_numpy()
    print('\nTARGET',la,lo,'rawN',len(vals),'expected',exp)
    print('quality',pd.Series(quals).value_counts(dropna=False).to_dict())
    for name,mp in weight_maps.items():
        w=np.array([mp.get(q,0) for q in quals],float); keep=w>0
        print(name,'N+',int(keep.sum()),'sumw',float(w.sum()),'ax',axmean(vals,w))
