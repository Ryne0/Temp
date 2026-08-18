import io, math, requests, pandas as pd, numpy as np
URL='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'
df=pd.read_csv(io.BytesIO(requests.get(URL,timeout=120).content),low_memory=False)
lat=np.radians(pd.to_numeric(df['LAT'],errors='coerce').to_numpy(float));lon=np.radians(pd.to_numeric(df['LON'],errors='coerce').to_numpy(float));azi=pd.to_numeric(df['AZI'],errors='coerce').to_numpy(float);qual=df['QUALITY'].astype(str).str.strip().str.upper().to_numpy();typ=df['TYPE'].astype(str).str.strip().str.upper().to_numpy()
base=np.isfinite(lat)&np.isfinite(lon)&np.isfinite(azi);lat=lat[base];lon=lon[base];azi=azi[base];qual=qual[base];typ=typ[base]
R0=6371.; SR=1200.
def distkm(la,lo):
 p=math.radians(la);q=math.radians(lo);dp=lat-p;dl=(lon-q+math.pi)%(2*math.pi)-math.pi;a=np.sin(dp/2)**2+math.cos(p)*np.cos(lat)*np.sin(dl/2)**2;return 2*R0*np.arcsin(np.minimum(1,np.sqrt(a)))
def ax(v,w):
 a=np.radians(2*np.asarray(v,float));w=np.asarray(w,float);sw=w.sum();x=(w*np.cos(a)).sum();y=(w*np.sin(a)).sum();return ((math.degrees(math.atan2(y,x))/2)%180, math.hypot(x,y)/sw)
def qweight(q): return {'A':1/15,'B':1/20,'C':1/25,'D':1/40}.get(q,0.)
def mweight(t):
 s=t[:2]
 return {'OC':2,'HF':4,'BO':5,'DI':5,'GF':5,'GV':4}.get(s,1)/5
expected={(-57.5,-177.5):(262,85.09130418742329,.7882591814872301),(-57.5,-97.5):(4,110.12065764194668,.7101704846889094),(-57.5,-92.5):(7,90.1676576510564,.7514888837425525),(-57.5,-82.5):(35,70.99305880582439,.7897581423979111),(32.5,-137.5):(1,26.,1.),(32.5,-132.5):(942,8.883681050844334,.6219368825399855),(32.5,97.5):(1532,44.22921741434799,.2597942118132781),(32.5,102.5):(1543,82.49560043660331,.2152421079317725),(-27.5,97.5):(3,125.52847500235684,.8904004853405388)}
for key,exp in expected.items():
 d=distkm(*key);m=(d<=SR)&(azi>=0)&(azi<180);v=azi[m];dd=d[m];qq=qual[m];tt=typ[m]
 wd_lin=SR+1-np.maximum(SR*.1,dd);wd_inv=1/np.maximum(SR*.1,dd);ones=np.ones(len(v));qw=np.array([qweight(x) for x in qq]);mw=np.array([mweight(x) for x in tt]);
 cands={'none':ones,'linear':wd_lin,'inverse':wd_inv,'lin_q':wd_lin*qw,'lin_m':wd_lin*mw,'lin_qm':wd_lin*qw*mw,'inv_qm':wd_inv*qw*mw}
 print('\nTARGET',key,'N',len(v),'EXPECTED',exp,'types',pd.Series(tt).value_counts().head(8).to_dict(),'qualities',pd.Series(qq).value_counts().to_dict())
 for n,w in cands.items():
  if w.sum()>0: print(n,ax(v,w),'errAngle',((ax(v,w)[0]-exp[1]+90)%180)-90,'errR',ax(v,w)[1]-exp[2])
