#!/usr/bin/env python3
import os, math, tarfile, tempfile
from pathlib import Path
import numpy as np
import pandas as pd
import requests

SEED=42; N_RUNS=10000; H=18; CELL=5.0
KUM_LAT,KUM_LON,KUM_MAG=32.6,130.7,6.8
LAMBDA_KM=4500.0; MEMORY_TAU=8.0; MEMORY_GAIN=0.10
SEARCH_KM=1200.; SIGMA_KM=500.; DIRECTION_STRENGTH=.45
PLANE_STRENGTH=.50; ANCHOR_SIGMA_KM=900.; ANCHOR_MAX_KM=1800.; NODAL_AMBIGUITY=.75
ARCHIVE_URLS=[
 'https://www.sciencebase.gov/catalog/file/get/5aa1b00ee4b0b1c392e86467?name=Slab2Distribute_Mar2018.tar.gz',
 'https://www.sciencebase.gov/catalog/file/get/5aa1b00ee4b0b1c392e86467?f=__disk__d5%2F91%2F39%2Fd591399bf4f249ab49ffec8a366e5070fe96e0ba',
]
WSM_URL='https://datapub.gfz.de/download/10.5880.WSM.2025.001-Scbwez/WSM_Database_2025.csv'

cells=[]
for lat in np.arange(-57.5,60.0,CELL):
    for lon in np.arange(-177.5,180.0,CELL):
        if lon>=95 or lon<=-65: cells.append((float(lat),float(lon)))
n=len(cells); assert n==960
lookup={(round(a,1),round(b,1)):i for i,(a,b) in enumerate(cells)}

def hav(lat1,lon1,lat2,lon2):
    R=6371.; p1,p2=math.radians(lat1),math.radians(lat2)
    dp=math.radians(lat2-lat1); dl=math.radians(((lon2-lon1+180)%360)-180)
    a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(min(1.,math.sqrt(a)))

def hav_vec(lat,lon,lats,lons):
    p1=np.radians(lat); p2=np.radians(lats); dp=np.radians(lats-lat)
    dl=np.radians(((lons-lon+180)%360)-180)
    aa=np.sin(dp/2)**2+np.cos(p1)*np.cos(p2)*np.sin(dl/2)**2
    return 2*6371*np.arcsin(np.minimum(1,np.sqrt(aa)))

def bearing(lat1,lon1,lat2,lon2):
    p1,p2=math.radians(lat1),math.radians(lat2); dl=math.radians(((lon2-lon1+180)%360)-180)
    y=math.sin(dl)*math.cos(p2); x=math.cos(p1)*math.sin(p2)-math.sin(p1)*math.cos(p2)*math.cos(dl)
    return (math.degrees(math.atan2(y,x))+360)%360

def axial_diff(a,b):
    d=abs((a-b)%180); return min(d,180-d)

def cell_center(lat,lon):
    lon=((lon+180)%360)-180
    return (round(math.floor((lat+60)/5)*5-57.5,1),round(math.floor((lon+180)/5)*5-177.5,1))

def plane_shear(incoming,strike,dip):
    x=abs(math.sin(math.radians(dip))*math.sin(math.radians(incoming-strike)))
    x=max(0.,min(1.,x)); return 2*x*math.sqrt(max(0.,1-x*x))

def nearest(lat,lon): return int(np.argmin([hav(lat,lon,a,b) for a,b in cells]))

incoming=np.array([bearing(KUM_LAT,KUM_LON,a,b) for a,b in cells])
dist=np.array([hav(KUM_LAT,KUM_LON,a,b) for a,b in cells])
kum_idx=nearest(KUM_LAT,KUM_LON); col_idx=nearest(4.844,-76.242); flo_idx=nearest(-8.41,121.39)

def build_wsm():
    print('Downloading WSM 2025...')
    w=pd.read_csv(WSM_URL,low_memory=False)[['LAT','LON','AZI','QUALITY','REGIME']].copy()
    for c in ['LAT','LON','AZI']: w[c]=pd.to_numeric(w[c],errors='coerce')
    w=w.dropna(subset=['LAT','LON','AZI']); w=w[(w.AZI>=0)&(w.AZI<180)]
    qwmap={'A':1.,'B':.8,'C':.6,'D':.35,'E':.15}; w['qw']=w.QUALITY.map(qwmap).fillna(.2)
    wlats=w.LAT.to_numpy(float); wlons=w.LON.to_numpy(float); waz=w.AZI.to_numpy(float); wq=w.qw.to_numpy(float)
    sa=np.full(n,np.nan); sq=np.zeros(n); sr=np.zeros(n); sn=np.zeros(n,int)
    for i,(lat,lon) in enumerate(cells):
        latpad=SEARCH_KM/111.; lonpad=SEARCH_KM/max(20.,111.*math.cos(math.radians(lat)))
        dlon=np.abs(((wlons-lon+180)%360)-180)
        ids=np.where((np.abs(wlats-lat)<=latpad)&(dlon<=lonpad))[0]
        if not len(ids): continue
        dd=hav_vec(lat,lon,wlats[ids],wlons[ids]); keep=dd<=SEARCH_KM; ids=ids[keep]; dd=dd[keep]
        if not len(ids): continue
        ww=wq[ids]*np.exp(-.5*(dd/SIGMA_KM)**2); th=np.radians(2*waz[ids])
        X=np.sum(ww*np.cos(th)); Y=np.sum(ww*np.sin(th)); sw=np.sum(ww)
        if sw<=0: continue
        sa[i]=(.5*math.degrees(math.atan2(Y,X)))%180; R=math.hypot(X,Y)/sw
        sq[i]=np.clip(R*(1-math.exp(-sw/3.)),0,1); sr[i]=R; sn[i]=len(ids)
    align=np.full(n,.5); G=np.ones(n)
    for i in range(n):
        if np.isfinite(sa[i]) and sq[i]>0:
            d=axial_diff(incoming[i]%180,sa[i]); A=abs(math.sin(math.radians(2*d)))
            align[i]=A; G[i]=1+DIRECTION_STRENGTH*sq[i]*(2*A-1)
    return G,sa,sq,sr,sn

anchors=[
 ('Bali 1976',-8.14,114.89,6.5,(96,29),(280,61)),('Ryukyu 2017',26.47,126.84,5.2,(69,30),(214,65)),
 ('Kamchatka 1976',51.45,159.50,6.1,(206,18),(39,73)),('Costa Rica 2017',9.43,-86.15,4.9,(320,44),(125,47)),
 ('N Colombia 2017',6.54,-72.18,4.8,(211,60),(105,65)),('Solomon 1987',-11.09,161.58,5.8,(343,12),(156,79)),
 ('Tonga 2022',-20.63,-175.25,4.9,(281,39),(107,51)),('Philippines 2023',8.90,127.42,4.7,(347,41),(171,49)),
 ('S Alaska 2016',59.75,-153.27,7.1,(313,59),(59,66))]
def build_cmt():
    num=np.zeros(n); den=np.zeros(n); support=np.zeros(n); counts=np.zeros(n,int)
    for name,la,lo,mw,p1,p2 in anchors:
        for i,(lat,lon) in enumerate(cells):
            dk=hav(la,lo,lat,lon)
            if dk>ANCHOR_MAX_KM: continue
            A=.5*(plane_shear(incoming[i],*p1)+plane_shear(incoming[i],*p2))
            spatial=math.exp(-.5*(dk/ANCHOR_SIGMA_KM)**2); magw=min(1.,max(.55,(mw-4.5)/2.5)); ww=spatial*magw*NODAL_AMBIGUITY
            num[i]+=ww*A; den[i]+=ww; support[i]+=spatial; counts[i]+=1
    A=np.full(n,.5); m=den>0; A[m]=num[m]/den[m]; Q=np.clip(1-np.exp(-support),0,1)
    G=np.clip(1+PLANE_STRENGTH*Q*(2*A-1),.5,1.5)
    qcap=float(Q[counts==1].max()) if np.any(counts==1) else .65
    return G,A,Q,counts,qcap

def download_archive(path):
    for u in ARCHIVE_URLS:
        try:
            print('Trying Slab2:',u)
            with requests.get(u,stream=True,timeout=90) as r:
                r.raise_for_status()
                with open(path,'wb') as f:
                    for ch in r.iter_content(1024*1024):
                        if ch: f.write(ch)
            mb=os.path.getsize(path)/1024/1024; print('Downloaded',round(mb,2),'MB')
            if mb>50 and tarfile.is_tarfile(path): return
        except Exception as e: print('download candidate failed:',repr(e))
    raise RuntimeError('Unable to download/validate official Slab2 archive')

def discover(root):
    sets={}
    for p in list(Path(root).rglob('*.xyz')):
        s=p.name.lower()
        if '_slab2_' not in s: continue
        reg=s.split('_slab2_',1)[0]; typ=None
        if '_dep_' in s: typ='dep'
        elif '_dip_' in s: typ='dip'
        elif '_str_' in s: typ='str'
        elif '_unc_' in s: typ='unc'
        if typ: sets.setdefault(reg,{})[typ]=p
    return {r:d for r,d in sets.items() if all(k in d for k in ('dep','dip','str','unc'))}

def readxyz(p):
    a=np.loadtxt(p,dtype=float); return a[:,0],a[:,1],a[:,2]

def build_slab(qcap):
    with tempfile.TemporaryDirectory() as td:
        arc=Path(td)/'slab2.tar.gz'; download_archive(arc)
        ext=Path(td)/'x'; ext.mkdir()
        with tarfile.open(arc,'r:*') as tf: tf.extractall(ext)
        sets=discover(ext); print('Complete Slab2 XYZ regional sets:',len(sets),sorted(sets))
        if not sets: raise RuntimeError('No complete Slab2 XYZ sets discovered')
        count=np.zeros(n,np.int64); sw=np.zeros(n); sdep=np.zeros(n); sdip=np.zeros(n); sunc=np.zeros(n)
        sc=np.zeros(n); ss=np.zeros(n); sA=np.zeros(n); evidence=np.zeros(n); regions=[set() for _ in range(n)]
        for reg,fs in sorted(sets.items()):
            dat={k:readxyz(p) for k,p in fs.items()}; lo,la,de=dat['dep']
            aligned=True
            for typ in ('dip','str','unc'):
                l2,a2,v2=dat[typ]
                if len(l2)!=len(lo) or not np.allclose(l2,lo,atol=1e-6,equal_nan=True) or not np.allclose(a2,la,atol=1e-6,equal_nan=True): aligned=False
            if aligned:
                frame=pd.DataFrame({'lon':lo,'lat':la,'dep':de,'dip':dat['dip'][2],'str':dat['str'][2],'unc':dat['unc'][2]})
            else:
                frame=pd.DataFrame({'lon':lo,'lat':la,'dep':de})
                for typ in ('dip','str','unc'):
                    l2,a2,v2=dat[typ]; frame=frame.merge(pd.DataFrame({'lon':l2,'lat':a2,typ:v2}),on=['lon','lat'],how='inner')
            frame=frame.replace([np.inf,-np.inf],np.nan).dropna()
            pos=frame.loc[frame.unc>0,'unc'].to_numpy(float); floor=float(np.percentile(pos,5)) if len(pos) else 1.; floor=max(floor,1e-6)
            for row in frame.itertuples(index=False):
                idx=lookup.get(cell_center(float(row.lat),float(row.lon)))
                if idx is None: continue
                ue=max(abs(float(row.unc)),floor); ww=1/(ue*ue); sr=float(row.str); dp=float(row.dip)
                A=plane_shear(incoming[idx],sr,dp); th=math.radians(2*(sr%180))
                count[idx]+=1; sw[idx]+=ww; evidence[idx]+=ww; sdep[idx]+=ww*abs(float(row.dep)); sdip[idx]+=ww*dp; sunc[idx]+=ww*abs(float(row.unc)); sc[idx]+=ww*math.cos(th); ss[idx]+=ww*math.sin(th); sA[idx]+=ww*A; regions[idx].add(reg)
        cov=count>0; depth=np.full(n,np.nan); dip=np.full(n,np.nan); strike=np.full(n,np.nan); unc=np.full(n,np.nan); coh=np.zeros(n); A=np.full(n,.5)
        for i in np.where(cov)[0]:
            w=sw[i]; depth[i]=sdep[i]/w; dip[i]=sdip[i]/w; unc[i]=sunc[i]/w; strike[i]=(.5*math.degrees(math.atan2(ss[i],sc[i])))%180; coh[i]=math.hypot(sc[i],ss[i])/w; A[i]=sA[i]/w
        ev=np.zeros(n); ev[cov]=evidence[cov]/np.maximum(count[cov],1); good=ev[cov & (ev>0) & np.isfinite(ev)]; ev95=float(np.percentile(good,95)) if len(good) else 1.; ev95=max(ev95,1e-12)
        qu=np.zeros(n); qu[cov]=np.clip(ev[cov]/ev95,0,1); Q=np.zeros(n); Q[cov]=qcap*np.clip(coh[cov],0,1)*qu[cov]
        G=np.ones(n); G[cov]=1+Q[cov]*(A[cov]-.5)
        return dict(cov=cov,count=count,regions=[','.join(sorted(x)) for x in regions],depth=depth,dip=dip,strike=strike,unc=unc,coh=coh,qu=qu,Q=Q,A=A,G=G,setcount=len(sets))

def simulate(Gw,Gcmt,G04b,G04c):
    rng=np.random.default_rng(SEED); power=n/16; W0=MEMORY_GAIN*(KUM_MAG/7.7)**2*np.exp(-dist/LAMBDA_KM)
    scens=('none','v03','v04a','v04b','v04c'); fac={'none':np.zeros(n),'v03':np.ones(n),'v04a':Gw,'v04b':G04b,'v04c':G04c}
    firstcell={s:np.full(N_RUNS,-1,np.int32) for s in scens}; firstday={s:np.full(N_RUNS,999,np.int16) for s in scens}
    exact13={s:np.zeros(n,np.int32) for s in scens}; exact18={s:np.zeros(n,np.int32) for s in scens}; ever13={s:np.zeros(n,np.int32) for s in scens}; ever18={s:np.zeros(n,np.int32) for s in scens}
    for r in range(N_RUNS):
        C=rng.uniform(.95,1.05,n); S0=(.50+(.94-.50)*(rng.random(n)**power))*C; L=(.004+(.014-.004)*(rng.random(n)**power))*C; rs=rng.uniform(.75,1.25,n)
        states={}; seen={s:np.zeros(n,bool) for s in scens}
        for s in scens:
            S=S0.copy(); M=W0*rs*fac[s]*C
            if s!='none': S[kum_idx]=min(S[kum_idx],.30*C[kum_idx]); M[kum_idx]=0
            else: M[:]=0
            states[s]=[S,M,False]
        for day in range(1,H+1):
            for s in scens:
                S,M,done=states[s]; S+=L; M*=math.exp(-1/MEMORY_TAU); E=S+M; hit=E>=C; cand=np.where(hit)[0]
                seen[s]|=hit
                if day==13: exact13[s][cand]+=1; ever13[s]+=seen[s]
                if day==18: exact18[s][cand]+=1; ever18[s]+=seen[s]
                if (not done) and len(cand):
                    j=int(cand[np.argmax(E[cand]/C[cand])]); firstcell[s][r]=j; firstday[s][r]=day; done=True; S[j]=.30*S[j]; M[j]=0
                states[s]=[S,M,done]
    def fp(s,w):
        mask=firstday[s]<=w; vals=firstcell[s][mask]; vals=vals[vals>=0]; return 100*np.bincount(vals,minlength=n)/N_RUNS,mask
    fp13={};fp18={};m13={};m18={}
    for s in scens: fp13[s],m13[s]=fp(s,13); fp18[s],m18[s]=fp(s,18)
    return scens,fp13,fp18,m13,m18,exact13,exact18,ever13,ever18

def main():
    Gw,sha,wsq,wsr,wsn=build_wsm(); Gcmt,Acmt,Qcmt,cnt,qcap=build_cmt(); G04b=np.clip(Gw*Gcmt,.45,1.80)
    print('CMT qcap',qcap); slab=build_slab(qcap); Gweak=np.where(slab['cov'],slab['G'],Gcmt); G04c=Gw*Gweak
    scens,fp13,fp18,m13,m18,e13,e18,ev13,ev18=simulate(Gw,Gcmt,G04b,G04c)
    summary=pd.DataFrame({'Scenario':['No Kumamoto','v0.3 distance+memory','v0.4a + WSM','v0.4b + WSM + CMT weak planes','v0.4c + WSM + continuous Slab2 / CMT fallback'],'Any first rupture by T+13 %':[100*m13[s].mean() for s in scens],'Any first rupture by T+18 %':[100*m18[s].mean() for s in scens]})
    out=pd.DataFrame({'cell_id':np.arange(n),'lat':[x[0] for x in cells],'lon':[x[1] for x in cells],'distance_km':dist,'G_WSM':Gw,'G_CMT':Gcmt,'G_v04b_total':G04b,'slab2_covered':slab['cov'],'slab2_node_count':slab['count'],'slab2_regions':slab['regions'],'slab2_depth_km':slab['depth'],'slab2_dip_deg':slab['dip'],'slab2_strike_deg':slab['strike'],'slab2_uncertainty_km':slab['unc'],'slab2_strike_coherence':slab['coh'],'Q_slab':slab['Q'],'A_slab':slab['A'],'G_slab':slab['G'],'G_v04c_total':G04c})
    for s in scens:
        out[f'T13_exact_{s}_%']=100*e13[s]/N_RUNS; out[f'T18_exact_{s}_%']=100*e18[s]/N_RUNS; out[f'T13_ever_{s}_%']=100*ev13[s]/N_RUNS; out[f'T18_ever_{s}_%']=100*ev18[s]/N_RUNS; out[f'T13_first_{s}_%']=fp13[s]; out[f'T18_first_{s}_%']=fp18[s]
    out['DeltaEver_v04c_vs_v04b_T18_pp']=out['T18_ever_v04c_%']-out['T18_ever_v04b_%']; out['DeltaExact_v04c_vs_v04b_T18_pp']=out['T18_exact_v04c_%']-out['T18_exact_v04b_%']
    out['Rank_first_v04c_T18']=out['T18_first_v04c_%'].rank(ascending=False,method='min').astype(int); out['Rank_ever_v04c_T18']=out['T18_ever_v04c_%'].rank(ascending=False,method='min').astype(int)
    rows=[]
    for name,idx in [('Colombia',col_idx),('Flores',flo_idx)]:
        r=out.iloc[idx]; rows.append({'Target':name,'cell_id':idx,'lat':r.lat,'lon':r.lon,'slab2_covered':bool(r.slab2_covered),'slab2_regions':r.slab2_regions,'slab2_node_count':int(r.slab2_node_count),'depth_km':r.slab2_depth_km,'dip_deg':r.slab2_dip_deg,'strike_deg':r.slab2_strike_deg,'uncertainty_km':r.slab2_uncertainty_km,'Q_slab':r.Q_slab,'A_slab':r.A_slab,'G_slab':r.G_slab,'G_v04b_total':r.G_v04b_total,'G_v04c_total':r.G_v04c_total,'T13_ever_v04b_%':r['T13_ever_v04b_%'],'T13_ever_v04c_%':r['T13_ever_v04c_%'],'T18_ever_v04b_%':r['T18_ever_v04b_%'],'T18_ever_v04c_%':r['T18_ever_v04c_%'],'T18_exact_v04b_%':r['T18_exact_v04b_%'],'T18_exact_v04c_%':r['T18_exact_v04c_%'],'T18_first_v04b_%':r['T18_first_v04b_%'],'T18_first_v04c_%':r['T18_first_v04c_%'],'Rank_first_v04c_T18':int(r.Rank_first_v04c_T18),'Rank_ever_v04c_T18':int(r.Rank_ever_v04c_T18)})
    targets=pd.DataFrame(rows)
    out.to_csv('v04c_real_slab2_continuous_10000runs.csv',index=False); summary.to_csv('v04c_summary.csv',index=False); targets.to_csv('v04c_targets.csv',index=False)
    out[['cell_id','lat','lon','slab2_covered','slab2_node_count','slab2_regions','slab2_depth_km','slab2_dip_deg','slab2_strike_deg','slab2_uncertainty_km','slab2_strike_coherence','Q_slab','A_slab','G_slab']].to_csv('v04c_slab2_5deg_structure.csv',index=False)
    print('Slab sets',slab['setcount'],'coverage',int(slab['cov'].sum()),'/960'); print(summary.to_string(index=False)); print('\nTARGETS\n',targets.to_string(index=False))

if __name__=='__main__': main()
