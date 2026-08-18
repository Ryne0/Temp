import io, math, requests, pandas as pd, numpy as np
URL='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'
df=pd.read_csv(io.BytesIO(requests.get(URL,timeout=120).content),low_memory=False)
lat=np.radians(pd.to_numeric(df['LAT'],errors='coerce').to_numpy(float)); lon=np.radians(pd.to_numeric(df['LON'],errors='coerce').to_numpy(float)); azi=pd.to_numeric(df['AZI'],errors='coerce').to_numpy(float); qual=df['QUALITY'].astype(str).str.strip().str.upper().to_numpy()
base=np.isfinite(lat)&np.isfinite(lon)&np.isfinite(azi); lat=lat[base];lon=lon[base];azi=azi[base];qual=qual[base]
R0=6371.0

def distkm(la,lo):
 p=math.radians(la);q=math.radians(lo);dp=lat-p;dl=(lon-q+math.pi)%(2*math.pi)-math.pi
 a=np.sin(dp/2)**2+math.cos(p)*np.cos(lat)*np.sin(dl/2)**2
 return 2*R0*np.arcsin(np.minimum(1,np.sqrt(a)))
def ax(vals,w=None):
 vals=np.asarray(vals,float);w=np.ones(len(vals)) if w is None else np.asarray(w,float);a=np.radians(2*vals);sw=w.sum();x=(w*np.cos(a)).sum();y=(w*np.sin(a)).sum();return ((math.degrees(math.atan2(y,x))/2)%180,math.hypot(x,y)/sw)
expected={(-57.5,-177.5):(262,85.09130418742329,.7882591814872301),(-57.5,-97.5):(4,110.12065764194668,.7101704846889094),(-57.5,-92.5):(7,90.1676576510564,.7514888837425525),(-57.5,-82.5):(35,70.99305880582439,.7897581423979111),(32.5,-137.5):(1,26.,1.),(32.5,-132.5):(942,8.883681050844334,.6219368825399855),(32.5,97.5):(1532,44.22921741434799,.2597942118132781),(32.5,102.5):(1543,82.49560043660331,.2152421079317725),(-27.5,97.5):(3,125.52847500235684,.8904004853405388)}
qmaps={'unweighted':{'A':1,'B':1,'C':1,'D':1},'ABCD_1_.75_.5_.25':{'A':1,'B':.75,'C':.5,'D':.25},'ABCD_1_.8_.6_.4':{'A':1,'B':.8,'C':.6,'D':.4},'ABCD_1_.75_.5_.125':{'A':1,'B':.75,'C':.5,'D':.125}}
for key,exp in expected.items():
 la,lo=key;d=distkm(la,lo); spatial=d<=1200; aziok=(azi>=0)&(azi<180); qok=np.isin(qual,['A','B','C','D']);
 print('\nTARGET',key,'EXPECTED',exp)
 for label,m in [('rad1200_allazi',spatial),('rad1200_aziok',spatial&aziok),('rad1200_ABCD',spatial&aziok&qok)]:
  print(label,'N',int(m.sum()),'AX',ax(azi[m]) if m.sum() else None,'Q',pd.Series(qual[m]).value_counts().to_dict())
 m=spatial&aziok&qok
 for name,mp in qmaps.items():
  w=np.array([mp.get(q,0) for q in qual[m]],float); print(name,'AXW',ax(azi[m],w),'sumw',float(w.sum()))
