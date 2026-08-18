import requests, json
ids=['5aa1b00ee4b0b1c392e86467','5aa312cde4b0b1c392ea3ef5','5aa41473e4b0b1c392eaaf2d']
for item in ids:
 url=f'https://www.sciencebase.gov/catalog/item/{item}?format=json'
 r=requests.get(url,timeout=120); print('\nITEM',item,'status',r.status_code,'bytes',len(r.content)); r.raise_for_status(); j=r.json()
 print('title',j.get('title'))
 for f in j.get('files',[]):
  print('FILE',f.get('name'),'size',f.get('size'),'url',f.get('url'))
 print('children?',j.get('hasChildren'),j.get('childIds'))
