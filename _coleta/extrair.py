import json, re, subprocess, time, urllib.parse
d=json.load(open('nuxt.json',encoding='utf-8'))
m=d['data']['menu-x-calota-taubate']
cfg=m['store']['config']
order=[p.split('/')[-1] for p in cfg['menu']['orderedCategories']]
catname={c['id']:c['name'] for c in m['categories']}
customs={c['id']:c for c in m['customs']}
for p in m['missingProducts']:
    for c in (p.get('customs') or []): customs.setdefault(c['id'],c)
prods=[]
for cid,lst in m['productsByCategory'].items():
    for p in lst: prods.append((cid,p,False))
for p in m['missingProducts']:
    prods.append((p['categoryPath'].split('/')[-1],p,True))
out=[]
for cid,p,missing in prods:
    slug=p['slug']
    url='https://menu.brendi.com.br/x-calota-taubate/produto/'+urllib.parse.quote(slug)
    html=subprocess.run(['curl','-sL','-A','Mozilla/5.0',url],capture_output=True).stdout.decode('utf-8','ignore')
    codes=re.findall(r'images\.brendi\.com\.br/optimized/([a-f0-9]{32})',html)
    time.sleep(0.2)
    gs=[]
    for path in p.get('customsPaths') or []:
        c=customs.get(path.split('/')[-1])
        if not c: continue
        gs.append({'titulo':c['title'],'min':c.get('minChoices',0),'max':c.get('maxChoices'),'obrig':c.get('required'),'tipo':c.get('type'),'ativo':c.get('active'),
                   'opcoes':[{'nome':ch['title'],'preco':ch.get('extraPrice',0)/100,'max':ch.get('maxChoices'),'desc':ch.get('description',''),'ativo':ch.get('active',True),'falta':ch.get('missing',False)} for ch in c['choices']]})
    out.append({'cat':cid,'catNome':catname.get(cid,''),'nome':p['name'],'desc':p.get('description',''),'preco':p['price']/100,'slug':slug,'falta':missing or p.get('missing',False),
                'img':codes[0] if codes else '','grupos':gs})
    print(len(out), cid[:6], p['name'][:40], p['price']/100, 'img' if codes else 'SEM', len(gs))
json.dump({'ordem':order,'produtos':out},open('produtos.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
