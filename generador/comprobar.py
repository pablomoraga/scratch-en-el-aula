import zipfile, json, sys, glob, os
bad=0
for f in sorted(glob.glob(sys.argv[1]+'/*.sb3')):
    z=zipfile.ZipFile(f); names=set(z.namelist()); p=json.loads(z.read('project.json'))
    errs=[]
    stage=p['targets'][0]; varids=set(stage['variables']); listids=set(stage['lists']); bids=set(stage['broadcasts'])
    sprites={t['name'] for t in p['targets'][1:]}
    backdrops={c['name'] for c in stage['costumes']}
    for t in p['targets']:
        for c in t['costumes']+t['sounds']:
            if c['md5ext'] not in names: errs.append('asset missing '+c['md5ext'])
        cos={c['name'] for c in t['costumes']}; snd={s['name'] for s in t['sounds']}
        B=t['blocks']
        tapados={v[2] for b in B.values() for v in b['inputs'].values() if v[0]==3 and len(v)>2 and isinstance(v[2],str)}  # menús tapados por un reportero
        for bid,b in B.items():
            if b['parent'] and b['parent'] not in B: errs.append('parent '+bid)
            if b['next'] and (b['next'] not in B or B[b['next']]['parent']!=bid): errs.append('next '+bid)
            if b['parent'] is None and not b['topLevel']: errs.append('orphan '+bid)
            for k,v in b['inputs'].items():
                for x in v[1:]:
                    if isinstance(x,str):
                        if x not in B: errs.append('input ref '+bid+k)
                        elif B[x]['parent']!=bid: errs.append('input parent '+bid+k)
                    elif isinstance(x,list) and x[0]==12 and x[2] not in varids: errs.append('var '+x[1])
                    elif isinstance(x,list) and x[0]==11 and x[2] not in bids: errs.append('bc '+x[1])
            for k,v in b['fields'].items():
                if k=='VARIABLE' and v[1] not in varids: errs.append('varfield')
                if k=='LIST' and v[1] not in listids: errs.append('listfield')
                if k=='BROADCAST_OPTION' and v[1] not in bids: errs.append('bcfield')
            op=b['opcode']; fv=list(b['fields'].values())[0][0] if b['fields'] else None
            if op=='looks_costume' and bid not in tapados and fv not in cos: errs.append('costume '+fv)
            if op in('looks_backdrops',) and fv not in backdrops: errs.append('backdrop '+fv)
            if op=='event_whenbackdropswitchesto' and fv not in backdrops: errs.append('bd hat '+fv)
            if op=='sound_sounds_menu' and fv not in snd: errs.append('sound %s in %s'%(fv,t['name']))
            if op in('sensing_touchingobjectmenu','motion_goto_menu','motion_pointtowards_menu','sensing_distancetomenu','control_create_clone_of_menu','motion_glideto_menu') and not fv.startswith('_') and fv not in sprites: errs.append('sprite '+fv)
    if errs: bad+=1; print(os.path.basename(f), sorted(set(errs))[:6])
print('checked', len(glob.glob(sys.argv[1]+'/*.sb3')), 'bad', bad)

import sys as _sys
_sys.exit(1 if bad else 0)
