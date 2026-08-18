import io,math,requests,pandas as pd,numpy as np
URL='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'
df=pd.read_csv(io.BytesIO(requests.get(URL,timeout=120).content),low_memory=False)
lat=np.radians(pd.to_numeric(df.LAT,errors='coerce').to_numpy(float));lon=np.radians(pd.to_numeric(df.LON,errors='coerce').to_numpy(float));azi=pd.to_numeric(df.AZI,errors='coerce').to_numpy(float);qual=df.QUALITY.astype(str).str.strip().str.upper().to_numpy()
ok=np.isfinite(lat)&np.isfinite(lon)&np.isfinite(azi);lat=lat[ok];lon=lon[ok];azi=azi[ok];qual=qual[ok]
R0=6371.;SR=1200.;SIG=705.;QMAP={'A':1.0,'B':.8,'C':.6,'D':.4,'E':.2}
def dist(la,lo):
 p=math.radians(la);q=math.radians(lo);dp=lat-p;dl=(lon-q+math.pi)%(2*math.pi)-math.pi;a=np.sin(dp/2)**2+math.cos(p)*np.cos(lat)*np.sin(dl/2)**2;return 2*R0*np.arcsin(np.minimum(1,np.sqrt(a)))
def ax(v,w):
 a=np.radians(2*v);sw=w.sum();x=(w*np.cos(a)).sum();y=(w*np.sin(a)).sum();return (math.degrees(math.atan2(y,x))/2)%180,math.hypot(x,y)/sw
def ad(a,b):return abs(((a-b+90)%180)-90)
expct={(-57.5,-177.5):(85.09130418742329,.7882591814872301,.7881709084109542),(-57.5,-97.5):(110.12065764194668,.7101704846889094,.0387818888325161),(-57.5,-92.5):(90.1676576510564,.7514888837425525,.0986012247446064),(-57.5,-82.5):(70.99305880582439,.7897581423979111,.5270732969167363),(32.5,-137.5):(26.,1.,.0465106909946826),(32.5,-132.5):(8.883681050844334,.6219368825399855,.6219366530407853),(32.5,97.5):(44.22921741434799,.2597942118132781,.2597942118132781),(32.5,102.5):(82.49560043660331,.2152421079317725,.2152421079317725),(-27.5,97.5):(125.52847500235684,.8904004853405388,.188911188447912)}
for k,e in expct.items():
 d=dist(*k);m=(d<=SR)&(azi>=0)&(azi<180);v=azi[m];dd=d[m];qq=qual[m];qw=np.array([QMAP.get(q,0.0) for q in qq]);w=np.exp(-(dd/SIG)**2)*qw
 if w.sum()<=0:w=np.exp(-(dd/SIG)**2)
 a,r=ax(v,w);ratio=e[2]/e[1] if e[1] else np.nan
 print('\n',k,'N',len(v),'SH/R got',a,r,'saved',e[:2]);print('sumw',w.sum(),'saved Q/R',ratio,'Qpred R*min(1,sumw)',r*min(1,w.sum()),'savedQ',e[2]);print('scaled sum needed',ratio/w.sum() if w.sum()>0 else np.nan)
