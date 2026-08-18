import io,math,requests,pandas as pd,numpy as np
URL='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'
df=pd.read_csv(io.BytesIO(requests.get(URL,timeout=120).content),low_memory=False)
lat=np.radians(pd.to_numeric(df.LAT,errors='coerce').to_numpy(float));lon=np.radians(pd.to_numeric(df.LON,errors='coerce').to_numpy(float));azi=pd.to_numeric(df.AZI,errors='coerce').to_numpy(float)
ok=np.isfinite(lat)&np.isfinite(lon)&np.isfinite(azi);lat=lat[ok];lon=lon[ok];azi=azi[ok]
R0=6371.;SR=1200.
def dist(la,lo):
 p=math.radians(la);q=math.radians(lo);dp=lat-p;dl=(lon-q+math.pi)%(2*math.pi)-math.pi;a=np.sin(dp/2)**2+math.cos(p)*np.cos(lat)*np.sin(dl/2)**2;return 2*R0*np.arcsin(np.minimum(1,np.sqrt(a)))
def ax(v,w):
 a=np.radians(2*v);sw=w.sum();x=(w*np.cos(a)).sum();y=(w*np.sin(a)).sum();return (math.degrees(math.atan2(y,x))/2)%180,math.hypot(x,y)/sw
def ad(a,b):return abs(((a-b+90)%180)-90)
expct={(-57.5,-177.5):(85.09130418742329,.7882591814872301),(-57.5,-97.5):(110.12065764194668,.7101704846889094),(-57.5,-92.5):(90.1676576510564,.7514888837425525),(-57.5,-82.5):(70.99305880582439,.7897581423979111),(32.5,-137.5):(26.,1.),(32.5,-132.5):(8.883681050844334,.6219368825399855),(32.5,97.5):(44.22921741434799,.2597942118132781),(32.5,102.5):(82.49560043660331,.2152421079317725),(-27.5,97.5):(125.52847500235684,.8904004853405388)}
data=[]
for k,e in expct.items():
 d=dist(*k);m=(d<=SR)&(azi>=0)&(azi<180);data.append((k,azi[m],d[m],e))
def score(kind,param):
 ae=[];re=[]
 for k,v,d,e in data:
  if kind=='exp':w=np.exp(-d/param)
  elif kind=='gauss':w=np.exp(-(d/param)**2)
  elif kind=='rat':w=1/(d+param)
  elif kind=='powlin':w=np.maximum(1e-9,1-d/SR)**param
  elif kind=='cliplin':w=SR+1-np.maximum(SR*param,d)
  a,r=ax(v,w);ae.append(ad(a,e[0]));re.append(abs(r-e[1]))
 return np.mean(ae)+30*np.mean(re),np.mean(ae),np.mean(re)
for kind,params in [('exp',np.linspace(100,5000,99)),('gauss',np.linspace(100,5000,99)),('rat',np.linspace(1,3000,100)),('powlin',np.linspace(.05,3,120)),('cliplin',np.linspace(0,.95,96))]:
 vals=[(score(kind,float(p)),float(p)) for p in params];vals.sort(key=lambda x:x[0]);print('\nBEST',kind,vals[:8])
 p=vals[0][1]
 for k,v,d,e in data:
  if kind=='exp':w=np.exp(-d/p)
  elif kind=='gauss':w=np.exp(-(d/p)**2)
  elif kind=='rat':w=1/(d+p)
  elif kind=='powlin':w=np.maximum(1e-9,1-d/SR)**p
  else:w=SR+1-np.maximum(SR*p,d)
  a,r=ax(v,w);print(k,'got',a,r,'expected',e,'ea',ad(a,e[0]),'er',r-e[1])
