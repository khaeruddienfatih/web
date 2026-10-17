import json,sys,subprocess,os,datetime as d
mon=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
lab=lambda x:f"{x.day:02d} {mon[x.month-1]} {x.year}"
PW=subprocess.check_output(['npm','root','-g']).decode().strip()+'/playwright'
env=dict(os.environ,PWPATH=PW)
def run(js,cfg=None,extra=None):
    e=dict(env); 
    if cfg is not None: e['CFG']=json.dumps(cfg)
    if extra: e.update(extra)
    r=subprocess.run(['node',js],env=e,capture_output=True,text=True,timeout=1500)
    return r.stdout+r.stderr
def build(spec):
    out=run('dupgen.js',extra={'SRC':str(spec['src'])}); print(out.strip())
    nid=[l.split()[1] for l in out.splitlines() if l.startswith('NEWID')][0].strip()
    o=run('fill.js',dict(id=int(nid),name=spec['name'],description=spec['desc'],quad=spec['q'],triple=spec['t'],double=spec['dd'],dates=spec['dates'],quotas=spec['quotas']),{'SAVE':'1'})
    print('fill:', [l for l in o.splitlines() if l.startswith('SAVED') or 'rror' in l])
    ents=[]
    for dep in spec['dates']:
        if dep in spec.get('nohotel',[]): continue
        t=d.date.fromisoformat(dep); mad,mak=spec['nights']
        ents.append(dict(date=lab(t),hotel=spec['h1'],**{'in':t.isoformat(),'out':(t+d.timedelta(mad)).isoformat()}))
        ents.append(dict(date=lab(t),hotel=spec['h2'],**{'in':(t+d.timedelta(mad)).isoformat(),'out':(t+d.timedelta(mak)).isoformat()}))
    o=run('hotel1.js',dict(id=int(nid),entries=ents),{'SAVE':'1'})
    print('hotels created:', o.count('notif Created'),'of',len(ents)); 
    return nid
if __name__=='__main__':
    spec=json.load(open(sys.argv[1])); print('RESULT',build(spec))
