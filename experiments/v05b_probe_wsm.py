import io, math, requests, pandas as pd, numpy as np
URL='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'
r=requests.get(URL,timeout=120); r.raise_for_status(); df=pd.read_csv(io.BytesIO(r.content),low_memory=False)
lat=np.radians(pd.to_numeric(df['LAT'],errors='coerce').to_numpy(float)); lon=np.radians(pd.to_numeric(df['LON'],errors='coerce').to_numpy(float)); sh=pd.to_numeric(df['AZI'],errors='coerce').to_numpy(float)
qual=df['QUALITY'].astype(str).str.strip().str.upper().to_numpy()
valid=np.isfinite(lat)&np.isfinite(lon)&np.isfinite(sh)
lat=lat[valid];lon=lon[valid];sh=sh[valid];qual=qual[valid]
R=6371.0

def distkm(la,lo):
 p=math.radians(la); q=math.radians(lo); dp=lat-p; dl=(lon-q+math.pi)%(2*math.pi)-math.pi
 a=np.sin(dp/2)**2+math.cos(p)*np.cos(lat)*np.sin(dl/2)**2
 return 2*R*np.arcsin(np.minimum(1,np.sqrt(a)))
def axmean(vals,weights=None):
 vals=np.asarray(vals,float); w=np.ones(len(vals)) if weights is None else np.asarray(weights,float); a=np.radians(vals*2); sw=w.sum(); x=np.sum(w*np.cos(a));y=np.sum(w*np.sin(a));return (math.degrees(math.atan2(y,x))/2)%180, math.hypot(x,y)/sw
expected={(-57.5,-177.5):(262,85.09130418742329,.7882591814872301),(-57.5,-97.5):(4,110.12065764194668,.7101704846889094),(-57.5,-92.5):(7,90.1676576510564,.7514888837425525),(-57.5,-82.5):(35,70.99305880582439,.7897581423979111),(32.5,-137.5):(1,26.0,1.0),(32.5,-132.5):(942,8.883681050844334,.6219368825399855),(32.5,97.5):(1532,44.22921741434799,.2597942118132781),(32.5,102.5):(1543,82.49560043660331,.2152421079317725),(-27.5,97.5):(3,125.52847500235684,.8904004853405388)}
radii=[500,750,1000,1250,1500,1750,2000,2250,2500,3000]
for (la,lo),exp in expected.items():
 d=distkm(la,lo); order=np.argsort(d); print('\nTARGET',la,lo,'expected',exp,'nearest',[(round(float(d[k]),1),float(sh[k]),qual[k]) for k in order[:5]])
 for rad in radii:
  m=d<=rad; vals=sh[m]; print('R',rad,'N',len(vals),'ax',axmean(vals) if len(vals) else None)
 # distance to Nth expected record, and exact unweighted stat using closest N
 n=exp[0]; ids=order[:n]; print('CLOSEST_N radius',float(d[ids[-1]]) if n else None,'ax',axmean(sh[ids]) if n else None,'quality',pd.Series(qual[ids]).value_counts().to_dict())
