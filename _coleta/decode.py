import re, json, sys
sys.setrecursionlimit(100000)
h=open('brendi.html',encoding='utf-8',errors='ignore').read()
raw=json.loads(re.search(r'id="__NUXT_DATA__"[^>]*>(.*?)</script>',h,re.S).group(1))
memo={}
WRAP={'Reactive','ShallowReactive','Ref','ShallowRef','EmptyRef','EmptyShallowRef','NuxtError','Island'}
def dv(i):
    if isinstance(i,int):
        if i in memo: return memo[i]
        if i<0: return None
        v=raw[i]
        if isinstance(v,list):
            if v and isinstance(v[0],str) and v[0] in WRAP:
                r=dv(v[1]) if len(v)>1 else None; memo[i]=r; return r
            if v and v[0] in ('Set',): r=[dv(x) for x in v[1:]]; memo[i]=r; return r
            if v and v[0] in ('Map',): r={str(dv(v[k])):dv(v[k+1]) for k in range(1,len(v),2)}; memo[i]=r; return r
            if v and v[0]=='Date': return v[1]
            out=[]; memo[i]=out
            out.extend(dv(x) for x in v); return out
        if isinstance(v,dict):
            out={}; memo[i]=out
            for k,x in v.items(): out[k]=dv(x)
            return out
        return v
    return i
data=dv(0)
json.dump(data,open('nuxt.json','w',encoding='utf-8'),ensure_ascii=False,default=str)
def walk(o,path='',depth=0,out=None):
    if out is None: out=[]
    if depth>7: return out
    if isinstance(o,dict):
        for k,v in o.items():
            p=f'{path}.{k}'
            if isinstance(v,(list,dict)): out.append((p,type(v).__name__,len(v)))
            walk(v,p,depth+1,out)
    elif isinstance(o,list) and o:
        walk(o[0],path+'[0]',depth+1,out)
    return out
for p,t,n in walk(data)[:80]: print(p,t,n)
