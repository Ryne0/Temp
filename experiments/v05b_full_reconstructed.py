#!/usr/bin/env python3
from __future__ import annotations
import io, math, heapq, json, tarfile, tempfile
from pathlib import Path
import requests
import numpy as np
import pandas as pd
import xarray as xr
try:
    import h5py
except Exception:
    h5py=None

SEED=42; N_RUNS=10_000; H=18
KUM_LAT,KUM_LON=32.6,130.7; KUM_MAG=6.8
LAMBDA_KM=4500.0; MEMORY_TAU=8.0; MEMORY_GAIN=0.10
WSM_RADIUS_KM=1200.0; WSM_SIGMA_KM=705.0
WSM_QMAP={'A':1.0,'B':0.8,'C':0.6,'D':0.4,'E':0.2}
WSM_STRENGTH=0.9
SLAB_MASTER_ITEM='5aa1b00ee4b0b1c392e86467'
OUT=Path('v05b_results'); OUT.mkdir(exist_ok=True)
TARGETS={'Colombia':(4.844,-76.242),'Flores':(-8.41,121.39)}
SAVED_WSM={
(-57.5,-177.5):(262,85.09130418742329,.7882591814872301,.7881709084109542),
(-57.5,-97.5):(4,110.12065764194668,.7101704846889094,.0387818888325161),
(-57.5,-92.5):(7,90.1676576510564,.7514888837425525,.0986012247446064),
(-57.5,-82.5):(35,70.99305880582439,.7897581423979111,.5270732969167363),
(32.5,-137.5):(1,26.0,1.0,.0465106909946826),
(32.5,-132.5):(942,8.883681050844334,.6219368825399855,.6219366530407853),
(32.5,97.5):(1532,44.22921741434799,.2597942118132781,.2597942118132781),
(32.5,102.5):(1543,82.49560043660331,.2152421079317725,.2152421079317725),
(-27.5,97.5):(3,125.52847500235684,.8904004853405388,.188911188447912),
}
SAVED_SLAB={
'Colombia':dict(cell=(2.5,-77.5),count=8485,depth=86.93027596753151,dip=23.994638043772984,strike=28.24158349066394,unc=13.503149659911136,Q=.1294965230754594),
'Flores':dict(cell=(-7.5,122.5),count=8301,depth=154.01556890392555,dip=28.20538303001758,strike=75.99813884077074,unc=13.30944459603893,Q=.0934430752440075),
}

def normlon(x): return ((float(x)+180.0)%360.0)-180.0
def hav(lat1,lon1,lat2,lon2):
    R=6371.0;p1=math.radians(float(lat1));p2=math.radians(float(lat2));dp=math.radians(float(lat2)-float(lat1));dl=math.radians(normlon(float(lon2)-float(lon1)))
    a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(min(1.0,math.sqrt(a)))
def bearing(lat1,lon1,lat2,lon2):
    p1=math.radians(float(lat1));p2=math.radians(float(lat2));dl=math.radians(normlon(float(lon2)-float(lon1)))
    y=math.sin(dl)*math.cos(p2);x=math.cos(p1)*math.sin(p2)-math.sin(p1)*math.cos(p2)*math.cos(dl)
    return (math.degrees(math.atan2(y,x))+360)%360
def axis_delta(a,b):
    d=abs((float(a)-float(b))%180.0); return min(d,180.0-d)
def wsm_align(direction,shmax): return abs(math.sin(math.radians(2.0*axis_delta(direction,shmax))))
def slab_align(direction,strike,dip):
    x=abs(math.sin(math.radians(float(dip)))*math.sin(math.radians(float(direction)-float(strike))))
    x=max(0.0,min(1.0,x));return 2*x*math.sqrt(max(0.0,1-x*x))
def axial(vals,weights):
    vals=np.asarray(vals,float);weights=np.asarray(weights,float);a=np.radians(2*vals);sw=weights.sum()
    if sw<=0:return np.nan,0.0
    x=np.sum(weights*np.cos(a));y=np.sum(weights*np.sin(a));return (math.degrees(math.atan2(y,x))/2)%180,math.hypot(x,y)/sw
def adiff(a,b): return abs(((float(a)-float(b)+90)%180)-90)

def make_grid():
    lats=np.arange(-57.5,58.0,5.0)
    lons=np.r_[np.arange(-177.5,-62.5,5.0),np.arange(97.5,178.0,5.0)]
    cells=[(float(la),float(lo)) for la in lats for lo in lons]
    assert len(cells)==960
    return cells

def nearest(cells,lat,lon): return int(np.argmin([hav(lat,lon,a,b) for a,b in cells]))

def wsm_reconstruct(cells):
    url='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'
    r=requests.get(url,timeout=180);r.raise_for_status();df=pd.read_csv(io.BytesIO(r.content),low_memory=False)
    lat=np.radians(pd.to_numeric(df['LAT'],errors='coerce').to_numpy(float));lon=np.radians(pd.to_numeric(df['LON'],errors='coerce').to_numpy(float));azi=pd.to_numeric(df['AZI'],errors='coerce').to_numpy(float);qual=df['QUALITY'].astype(str).str.strip().str.upper().to_numpy()
    ok=np.isfinite(lat)&np.isfinite(lon)&np.isfinite(azi);lat=lat[ok];lon=lon[ok];azi=azi[ok];qual=qual[ok]
    out=[];R0=6371.0
    for z,(la,lo) in enumerate(cells):
        p=math.radians(la);q=math.radians(lo);dp=lat-p;dl=(lon-q+math.pi)%(2*math.pi)-math.pi
        aa=np.sin(dp/2)**2+math.cos(p)*np.cos(lat)*np.sin(dl/2)**2;d=2*R0*np.arcsin(np.minimum(1,np.sqrt(aa)))
        m=(d<=WSM_RADIUS_KM)&(azi>=0)&(azi<180);n=int(m.sum())
        if n==0: out.append((0,np.nan,0.,0.,0.));continue
        vv=azi[m];dd=d[m];qq=qual[m]
        qw=np.array([WSM_QMAP.get(x,0.0) for x in qq],float);w=np.exp(-(dd/WSM_SIGMA_KM)**2)*qw
        if w.sum()<=0: w=np.exp(-(dd/WSM_SIGMA_KM)**2)
        sh,R=axial(vv,w);evidence=float(w.sum());Q=float(R*(1-math.exp(-evidence/3.0)))
        out.append((n,sh,R,Q,evidence))
        if z%120==0: print('WSM grid',z,'/',len(cells))
    arr=pd.DataFrame(out,columns=['WSM_record_count','WSM_SHmax_deg','WSM_coherence_R','WSM_confidence_Q','WSM_evidence'])
    ae=[];re=[];qe=[];count_ok=0
    lookup={c:i for i,c in enumerate(cells)}
    for c,e in SAVED_WSM.items():
        row=arr.iloc[lookup[c]];count_ok+=int(int(row.WSM_record_count)==e[0]);ae.append(adiff(row.WSM_SHmax_deg,e[1]));re.append(abs(row.WSM_coherence_R-e[2]));qe.append(abs(row.WSM_confidence_Q-e[3]))
    print('WSM VALIDATION count',count_ok,'/9 angle_MAE',np.mean(ae),'R_MAE',np.mean(re),'Q_MAE',np.mean(qe),'angle_MAX',np.max(ae),'R_MAX',np.max(re),'Q_MAX',np.max(qe))
    return arr

def cell_center(lat,lon):
    lon=normlon(lon);latc=math.floor((float(lat)+60)/5)*5-57.5;lonc=math.floor((lon+180)/5)*5-177.5
    return round(latc,1),round(lonc,1)
def _select_h5(f):
    for name in ('z','Z','depth','DEPTH','dip','DIP','strike','STRIKE','unc','UNCERTAINTY'):
        if name in f and hasattr(f[name],'shape'):return f[name]
    cand=[]
    def visit(name,obj):
        if isinstance(obj,h5py.Dataset) and np.issubdtype(obj.dtype,np.number):cand.append((obj.size,name))
    f.visititems(visit)
    if not cand:raise ValueError('No HDF5 numeric data')
    return f[max(cand)[1]]
def grid_xyz(path):
    for engine in ('scipy',None):
        try:
            ds=xr.open_dataset(path,engine=engine,decode_cf=False) if engine else xr.open_dataset(path,decode_cf=False)
            try:
                vars_num=[(da.size,n) for n,da in ds.data_vars.items() if np.issubdtype(da.dtype,np.number)]
                if not vars_num:raise ValueError()
                name=next((n for n in ('z','Z','depth','DEPTH','dip','DIP','strike','STRIKE') if n in ds.data_vars),None);da=ds[name] if name else ds[max(vars_num)[1]]
                xn=next((x for x in ('x','lon','longitude') if x in ds.variables),None);yn=next((y for y in ('y','lat','latitude') if y in ds.variables),None)
                if xn and yn and da.ndim>=2:
                    xs=np.asarray(ds[xn].values,float);ys=np.asarray(ds[yn].values,float);z=np.asarray(da.values,float).squeeze()
                    if z.shape==(len(xs),len(ys)):z=z.T
                    if z.shape==(len(ys),len(xs)):
                        xx,yy=np.meshgrid(xs,ys);return xx.ravel(),yy.ravel(),z.ravel()
                if all(k in ds.variables for k in ('x_range','y_range','spacing','dimension')):
                    xrng=np.asarray(ds['x_range'].values,float);yrng=np.asarray(ds['y_range'].values,float);sp=np.asarray(ds['spacing'].values,float);dim=np.asarray(ds['dimension'].values,int);nx,ny=int(dim[0]),int(dim[1]);xs=xrng[0]+np.arange(nx)*sp[0];ys=yrng[0]+np.arange(ny)*sp[1];z=np.asarray(da.values,float).reshape(ny,nx);xx,yy=np.meshgrid(xs,ys);return xx.ravel(),yy.ravel(),z.ravel()
            finally: ds.close()
        except Exception: pass
    if h5py is not None:
        try:
            with h5py.File(path,'r') as f:
                da=_select_h5(f);xn=next((x for x in ('x','lon','longitude') if x in f),None);yn=next((y for y in ('y','lat','latitude') if y in f),None)
                if xn and yn:
                    xs=np.asarray(f[xn][...],float).squeeze();ys=np.asarray(f[yn][...],float).squeeze();z=np.asarray(da[...],float).squeeze()
                    if z.shape==(len(xs),len(ys)):z=z.T
                    if z.shape==(len(ys),len(xs)):
                        xx,yy=np.meshgrid(xs,ys);return xx.ravel(),yy.ravel(),z.ravel()
        except Exception:pass
    raise ValueError('Unsupported grd '+str(path))
def text_xyz(path):
    a=np.loadtxt(path,dtype=float);return a[:,0],a[:,1],a[:,2]
def read_grid(path):return text_xyz(path) if path.suffix.lower()=='.xyz' else grid_xyz(path)
def discover(root):
    sets={};files=list(root.rglob('*.xyz'))+list(root.rglob('*.grd'));files.sort(key=lambda p:0 if p.suffix.lower()=='.xyz' else 1)
    for p in files:
        n=p.name.lower()
        if '_slab2_' not in n:continue
        reg=n.split('_slab2_',1)[0];typ='dep' if '_dep_' in n else 'dip' if '_dip_' in n else 'str' if '_str_' in n else 'unc' if '_unc_' in n else None
        if typ and typ not in sets.setdefault(reg,{}):sets[reg][typ]=p
    return {r:s for r,s in sets.items() if all(k in s for k in ('dep','dip','str','unc'))}
def aligned(fs):
    data={k:read_grid(p) for k,p in fs.items()};lon,lat,dep=data['dep'];vals={'dep':np.asarray(dep,float)}
    good=True
    for t in ('dip','str','unc'):
        lo,la,v=data[t]
        if len(lo)!=len(lon) or not np.allclose(lo,lon,atol=1e-6,equal_nan=True) or not np.allclose(la,lat,atol=1e-6,equal_nan=True):good=False;break
        vals[t]=np.asarray(v,float)
    if good:return np.asarray(lon,float),np.asarray(lat,float),vals['dep'],vals['dip'],vals['str'],vals['unc']
    left=pd.DataFrame({'lon':lon,'lat':lat,'dep':dep})
    for t in ('dip','str','unc'):
        lo,la,v=data[t];left=left.merge(pd.DataFrame({'lon':lo,'lat':la,t:v}),on=['lon','lat'],how='inner',validate='one_to_one')
    return tuple(left[c].to_numpy(float) for c in ('lon','lat','dep','dip','str','unc'))
def download_slab(root):
    meta=requests.get(f'https://www.sciencebase.gov/catalog/item/{SLAB_MASTER_ITEM}?format=json',timeout=120).json();f=next(x for x in meta['files'] if x.get('name')=='Slab2Distribute_Mar2018.tar.gz');arc=root/'slab.tar.gz'
    print('Downloading Slab2',f['url'],'size',f.get('size'))
    with requests.get(f['url'],stream=True,timeout=300) as r:
        r.raise_for_status()
        with open(arc,'wb') as o:
            for ch in r.iter_content(1024*1024):
                if ch:o.write(ch)
    ext=root/'slab';ext.mkdir();
    with tarfile.open(arc,'r:*') as tf:tf.extractall(ext)
    return ext

def slab_reconstruct(cells,root):
    lookup={(round(a,1),round(b,1)):i for i,(a,b) in enumerate(cells)};n=len(cells)
    count=np.zeros(n,np.int64);sw=np.zeros(n);sdep=np.zeros(n);sdip=np.zeros(n);sunc=np.zeros(n);sc=np.zeros(n);ss=np.zeros(n);sinv=np.zeros(n);regions=[set() for _ in cells]
    sets=discover(root);print('Slab regional sets',len(sets),sorted(sets))
    for ri,(reg,fs) in enumerate(sorted(sets.items())):
        print('Slab region',ri+1,'/',len(sets),reg);lon,lat,dep,dip,strike,unc=aligned(fs);valid=np.isfinite(lon)&np.isfinite(lat)&np.isfinite(dep)&np.isfinite(dip)&np.isfinite(strike)&np.isfinite(unc);lon,lat,dep,dip,strike,unc=[x[valid] for x in (lon,lat,dep,dip,strike,unc)];pu=unc[unc>0];floor=float(np.percentile(pu,5)) if len(pu) else 1.;floor=floor if np.isfinite(floor) and floor>0 else 1.
        for lo,la,de,di,st,un in zip(lon,lat,dep,dip,strike,unc):
            idx=lookup.get(cell_center(la,lo))
            if idx is None:continue
            ue=max(abs(float(un)),floor);w=1/(ue*ue);th=math.radians(2*(float(st)%180));count[idx]+=1;sw[idx]+=w;sinv[idx]+=w;sdep[idx]+=w*abs(float(de));sdip[idx]+=w*float(di);sunc[idx]+=w*abs(float(un));sc[idx]+=w*math.cos(th);ss[idx]+=w*math.sin(th);regions[idx].add(reg)
    cov=count>0;depth=np.full(n,np.nan);dipm=np.full(n,np.nan);strm=np.full(n,np.nan);uncm=np.full(n,np.nan);coh=np.zeros(n)
    for i in np.where(cov)[0]:
        depth[i]=sdep[i]/sw[i];dipm[i]=sdip[i]/sw[i];uncm[i]=sunc[i]/sw[i];strm[i]=(0.5*math.degrees(math.atan2(ss[i],sc[i])))%180;coh[i]=math.hypot(sc[i],ss[i])/sw[i]
    evidence=np.zeros(n);evidence[cov]=sinv[cov]/np.maximum(count[cov],1);ev=evidence[cov&(evidence>0)&np.isfinite(evidence)];ev95=float(np.percentile(ev,95)) if len(ev) else 1.;qu=np.zeros(n);qu[cov]=np.clip(evidence[cov]/ev95,0,1)
    # recover frozen old q_cap from saved output diagnostics, not from earthquake outcomes
    caps=[]
    for name,s in SAVED_SLAB.items():
        idx=lookup[s['cell']]
        if coh[idx]*qu[idx]>0:caps.append(s['Q']/(coh[idx]*qu[idx]))
    qcap=float(np.median(caps)) if caps else .65
    Q=np.zeros(n);Q[cov]=qcap*np.clip(coh[cov],0,1)*qu[cov]
    print('Slab qcap recovered',qcap,'target estimates',caps,'coverage',int(cov.sum()),'/960')
    for name,s in SAVED_SLAB.items():
        i=lookup[s['cell']];print('SLAB VALID',name,'count',count[i],s['count'],'depth',depth[i],s['depth'],'dip',dipm[i],s['dip'],'strike',strm[i],s['strike'],'unc',uncm[i],s['unc'],'Q',Q[i],s['Q'])
    return pd.DataFrame({'slab2_covered':cov,'slab2_node_count':count,'slab2_regions':[','.join(sorted(x)) for x in regions],'slab2_depth_km':depth,'slab2_dip_deg':dipm,'slab2_strike_deg':strm,'slab2_uncertainty_km':uncm,'slab2_strike_coherence':coh,'slab2_q_unc':qu,'Q_slab':Q}),qcap

def build_neighbors(cells):
    lookup={(round(a,1),round(b,1)):i for i,(a,b) in enumerate(cells)};adj=[[] for _ in cells]
    for i,(la,lo) in enumerate(cells):
        for da in (-5.,0.,5.):
            for do in (-5.,0.,5.):
                if da==0 and do==0:continue
                key=(round(la+da,1),round(normlon(lo+do),1));j=lookup.get(key)
                if j is not None:adj[i].append((j,hav(la,lo,*cells[j]),bearing(la,lo,*cells[j])))
    return adj

def dijkstra(cells,adj,src,wsm,slab,use_wsm=True,use_slab=True,fallback=1.0):
    n=len(cells);dist=np.full(n,np.inf);prev=np.full(n,-1,np.int32);dist[src]=0;heap=[(0.,src)]
    def gain(i,b):
        g=1.
        if use_wsm and np.isfinite(wsm.WSM_SHmax_deg.iloc[i]):g*=1+WSM_STRENGTH*float(wsm.WSM_confidence_Q.iloc[i])*(wsm_align(b,float(wsm.WSM_SHmax_deg.iloc[i]))-.5)
        if use_slab:
            if bool(slab.slab2_covered.iloc[i]):g*=1+float(slab.Q_slab.iloc[i])*(slab_align(b,float(slab.slab2_strike_deg.iloc[i]),float(slab.slab2_dip_deg.iloc[i]))-.5)
            else:g*=fallback
        return max(0.05,g)
    while heap:
        du,i=heapq.heappop(heap)
        if du!=dist[i]:continue
        for j,dkm,b in adj[i]:
            gj=gain(j,bearing(*cells[j],*cells[i]));gi=gain(i,b);K=math.sqrt(gi*gj);nd=du+dkm/(LAMBDA_KM*K)
            if nd<dist[j]:dist[j]=nd;prev[j]=i;heapq.heappush(heap,(nd,j))
    return dist,prev

def neutral_dijkstra(adj,src,n):
    dist=np.full(n,np.inf);dist[src]=0;heap=[(0.,src)]
    while heap:
        du,i=heapq.heappop(heap)
        if du!=dist[i]:continue
        for j,dkm,b in adj[i]:
            nd=du+dkm/LAMBDA_KM
            if nd<dist[j]:dist[j]=nd;heapq.heappush(heap,(nd,j))
    return dist

def reconstruct(prev,t,cells):
    p=[];x=int(t);seen=set()
    while x>=0 and x not in seen:p.append(x);seen.add(x);x=int(prev[x])
    p=p[::-1];return ' > '.join(f'{cells[i][0]:.1f},{cells[i][1]:.1f}' for i in p),p

def memory_from_path(cells,neutral,structured):
    direct=np.array([hav(KUM_LAT,KUM_LON,a,b)/LAMBDA_KM for a,b in cells]);corr=np.maximum(0,direct+structured-neutral);amp=MEMORY_GAIN*(KUM_MAG/7.7)**2;return amp*np.exp(-corr),corr,direct

def simulate(memories,cells):
    n=len(cells);power=n/16;rng=np.random.default_rng(SEED);names=list(memories);first={s:np.full(N_RUNS,-1,np.int32) for s in names};fday={s:np.full(N_RUNS,999,np.int16) for s in names};a13={s:np.zeros(n,np.int32) for s in names};a18={s:np.zeros(n,np.int32) for s in names};kum=nearest(cells,KUM_LAT,KUM_LON)
    for r in range(N_RUNS):
        C=rng.uniform(.95,1.05,n);u=rng.random(n);S0=(.50+(.94-.50)*(u**power))*C;u=rng.random(n);L=(.004+(.014-.004)*(u**power))*C;sens=rng.uniform(.75,1.25,n);states={}
        for s,W in memories.items():
            S=S0.copy();M=W*sens*C
            if s!='none':S[kum]=min(S[kum],.30*C[kum]);M[kum]=0
            else:M[:]=0
            states[s]=[S,M,False]
        for day in range(1,H+1):
            for s in names:
                S,M,done=states[s];S+=L;M*=math.exp(-1/MEMORY_TAU);E=S+M;cand=np.where(E>=C)[0]
                if day==13 and cand.size:a13[s][cand]+=1
                if day==18 and cand.size:a18[s][cand]+=1
                if (not done) and cand.size:
                    j=int(cand[np.argmax(E[cand]/C[cand])]);first[s][r]=j;fday[s][r]=day;done=True;S[j]=.30*S[j];M[j]=0
                states[s]=[S,M,done]
        if (r+1)%1000==0:print('MC',r+1,'/',N_RUNS)
    rows=[];per={}
    for s in names:
        mask13=fday[s]<=13;mask18=fday[s]<=18;cnt=np.bincount(first[s][mask18 & (first[s]>=0)],minlength=n);fp=100*cnt/N_RUNS;per[s]=dict(first=fp,t13=100*a13[s]/N_RUNS,t18=100*a18[s]/N_RUNS)
        rows.append((s,100*mask13.mean(),100*mask18.mean()))
    return pd.DataFrame(rows,columns=['Scenario','Any_first_T13_%','Any_first_T18_%']),per

def main():
    cells=make_grid();grid=pd.DataFrame({'cell_id':np.arange(960),'lat':[x[0] for x in cells],'lon':[x[1] for x in cells]});src=nearest(cells,KUM_LAT,KUM_LON);print('Source cell',src,cells[src])
    wsm=wsm_reconstruct(cells)
    with tempfile.TemporaryDirectory() as td:
        slabroot=download_slab(Path(td));slab,qcap=slab_reconstruct(cells,slabroot)
    adj=build_neighbors(cells);neutral=neutral_dijkstra(adj,src,len(cells));struct_wsm,prev_wsm=dijkstra(cells,adj,src,wsm,slab,True,False);struct_full,prev_full=dijkstra(cells,adj,src,wsm,slab,True,True,1.0);struct_lo,_=dijkstra(cells,adj,src,wsm,slab,True,True,.9);struct_hi,_=dijkstra(cells,adj,src,wsm,slab,True,True,1.1)
    W_wsm,C_wsm,direct=memory_from_path(cells,neutral,struct_wsm);W_full,C_full,_=memory_from_path(cells,neutral,struct_full);W_lo,_,_=memory_from_path(cells,neutral,struct_lo);W_hi,_,_=memory_from_path(cells,neutral,struct_hi);amp=MEMORY_GAIN*(KUM_MAG/7.7)**2;W_rad=amp*np.exp(-direct)
    # exact neutral invariant
    W_neutral,_c,_=memory_from_path(cells,neutral,neutral);print('Neutral invariant max abs',float(np.max(np.abs(W_neutral-W_rad))))
    summary,per=simulate({'none':np.zeros(960),'v03_radial':W_rad,'v05bR_WSM_path':W_wsm,'v05bR_WSM_Slab2_path':W_full},cells)
    out=pd.concat([grid,wsm,slab],axis=1);out['radial_cost']=direct;out['neutral_grid_cost']=neutral;out['structured_WSM_cost']=struct_wsm;out['structured_full_cost']=struct_full;out['corrected_WSM_cost']=C_wsm;out['corrected_full_cost']=C_full;out['W_radial']=W_rad;out['W_path_WSM']=W_wsm;out['W_path_full']=W_full;out['PathRatio_WSM_vs_radial']=W_wsm/W_rad;out['PathRatio_full_vs_radial']=W_full/W_rad;out['PathRatio_CMTsens_low']=W_lo/W_rad;out['PathRatio_CMTsens_high']=W_hi/W_rad
    for s,d in per.items():out[f'T18_first_{s}_%']=d['first'];out[f'T13_threshold_{s}_%']=d['t13'];out[f'T18_threshold_{s}_%']=d['t18']
    out['Delta_first_full_vs_v03_T18_pp']=out['T18_first_v05bR_WSM_Slab2_path_%']-out['T18_first_v03_radial_%'];out['Delta_threshold_full_vs_v03_T18_pp']=out['T18_threshold_v05bR_WSM_Slab2_path_%']-out['T18_threshold_v03_radial_%']
    targets=[];paths=[]
    for name,(la,lo) in TARGETS.items():
        i=nearest(cells,la,lo);r=out.iloc[i];path,ids=reconstruct(prev_full,i,cells);targets.append({'Target':name,'cell_id':i,'lat':r.lat,'lon':r.lon,'W_radial':r.W_radial,'W_path_full':r.W_path_full,'PathRatio':r.PathRatio_full_vs_radial,'T18_first_v03_%':r['T18_first_v03_radial_%'],'T18_first_v05bR_%':r['T18_first_v05bR_WSM_Slab2_path_%'],'T18_threshold_v03_%':r['T18_threshold_v03_radial_%'],'T18_threshold_v05bR_%':r['T18_threshold_v05bR_WSM_Slab2_path_%'],'CMTsens_low_ratio':r.PathRatio_CMTsens_low,'CMTsens_high_ratio':r.PathRatio_CMTsens_high,'path_hops':len(ids)-1});paths.append({'Target':name,'cell_id':i,'path':path})
    targets=pd.DataFrame(targets);paths=pd.DataFrame(paths)
    top=out.assign(abs_log_ratio=np.abs(np.log(out.PathRatio_full_vs_radial))).sort_values('abs_log_ratio',ascending=False).head(50)
    out.to_csv(OUT/'v05bR_cells_10000runs.csv',index=False);summary.to_csv(OUT/'v05bR_summary_10000runs.csv',index=False);targets.to_csv(OUT/'v05bR_targets.csv',index=False);paths.to_csv(OUT/'v05bR_paths.csv',index=False);top.to_csv(OUT/'v05bR_top_path_changes.csv',index=False)
    print('\nSUMMARY\n',summary.to_string(index=False));print('\nTARGETS\n',targets.to_string(index=False));print('\nTOP PATH RATIOS\n',top[['cell_id','lat','lon','PathRatio_full_vs_radial','T18_first_v03_radial_%','T18_first_v05bR_WSM_Slab2_path_%','Delta_first_full_vs_v03_T18_pp']].head(20).to_string(index=False));print('\nPATHS\n',paths.to_string(index=False));print('Saved',list(OUT.iterdir()))
if __name__=='__main__':main()
