import io, math, requests, pandas as pd, numpy as np
URL='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'
r=requests.get(URL,timeout=120); r.raise_for_status()
print('download bytes',len(r.content))
df=pd.read_csv(io.BytesIO(r.content),low_memory=False)
print('shape',df.shape)
print('columns',list(df.columns))
print(df.head(3).to_string())

def colpick(keys):
    for c in df.columns:
        s=c.lower().replace(' ','').replace('_','')
        if any(k in s for k in keys): return c
    return None
latc=colpick(['latitude','lat']); lonc=colpick(['longitude','lon']); shc=colpick(['shmax']); qc=colpick(['quality'])
print('picked',latc,lonc,shc,qc)

def axmean(vals,weights=None):
    a=np.radians(np.asarray(vals,float)*2)
    if weights is None: weights=np.ones(len(a))
    x=np.sum(weights*np.cos(a)); y=np.sum(weights*np.sin(a))
    ang=(math.degrees(math.atan2(y,x))/2)%180
    R=math.hypot(x,y)/np.sum(weights)
    return ang,R

targets=[(-57.5,-177.5),(-57.5,-97.5),(-57.5,-92.5),(-57.5,-82.5),(32.5,-137.5),(32.5,-132.5),(32.5,97.5),(32.5,102.5),(-27.5,97.5),(2.5,162.5)]
lat=pd.to_numeric(df[latc],errors='coerce'); lon=pd.to_numeric(df[lonc],errors='coerce'); sh=pd.to_numeric(df[shc],errors='coerce')
for la,lo in targets:
    dlon=((lon-lo+180)%360)-180
    m=(abs(lat-la)<=2.5)&(abs(dlon)<=2.5)&sh.notna()
    sub=df.loc[m].copy()
    vals=pd.to_numeric(sub[shc],errors='coerce').dropna().to_numpy()
    print('\nTARGET',la,lo,'N',len(vals),'AX',axmean(vals) if len(vals) else None)
    if qc and len(sub): print('quality',sub[qc].astype(str).value_counts(dropna=False).to_dict())
