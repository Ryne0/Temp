import requests, json
BASE='https://earthquake.usgs.gov/arcgis/rest/services/eq/slab2_grid/MapServer/0/query'
for params in [
 {'where':'1=1','returnCountOnly':'true','f':'json'},
 {'where':'1=1','outFields':'OBJECTID,lon,lat,DEPTH,DIP,STRIKE,UNCERTAINTY','returnGeometry':'false','resultRecordCount':5,'f':'json'}
]:
 r=requests.get(BASE,params=params,timeout=120); print('URL',r.url,'status',r.status_code,'bytes',len(r.content)); r.raise_for_status(); print(json.dumps(r.json(),indent=2)[:20000])
