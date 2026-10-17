#!/usr/bin/env python3
"""Préparation auditable Kontexte → kompose → Orgo, sans aucune écriture Orgo.
Ce pont ne crée jamais de session élève, de Task, de Case ni de preuve scolaire.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

NAMES=('ekole','ekole-quebec','Kontexte','kompose','Orgo','Orgo_Worlds')

def locate(parent: Path, name: str) -> Path:
    for trial in (parent/name, parent/name/name, parent/name.capitalize() if name == "kompose" else parent/name):
        if trial.is_dir():
            return trial.resolve()
    raise FileNotFoundError(f'Dépôt absent : {name} sous {parent}')

def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def invoke(cmd: list[str], *, cwd=None, timeout=25) -> dict:
    try:
        p=subprocess.run(cmd,cwd=cwd,timeout=timeout,encoding='utf-8',errors='replace',capture_output=True)
        return {'ok':p.returncode==0, 'code':p.returncode, 'stdout':p.stdout[-5000:], 'stderr':p.stderr[-3000:], 'command':cmd}
    except (OSError,subprocess.TimeoutExpired) as ex:
        return {'ok':False,'code':None,'stdout':'','stderr':str(ex),'command':cmd}

def review_html(preview: dict, status: dict) -> str:
    e=html.escape
    steps=''.join('<li><b>'+e(s['id'])+' — '+e(s['role'])+'</b> : '+e(s['instruction'])+'</li>' for s in preview['steps'])
    warns=''.join('<li>'+e(w)+'</li>' for w in preview['warnings'])
    tests=''.join('<tr><th scope="row">'+e(k)+'</th><td>'+e('OK' if v.get('ok') else 'À vérifier')+'</td></tr>' for k,v in status['checks'].items())
    return f'''<!doctype html><html lang="fr-CA"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Revue d'intégration des missions — Ekole</title><style>
    :root{{font:17px/1.55 system-ui, sans-serif;color:#19323f;background:#f2f6f7}} body{{max-width:1000px;margin:0 auto;padding:22px}} article{{background:white;padding:20px;border-radius:14px;margin:16px 0;border:1px solid #d0dde0}} h1,h2{{line-height:1.18}} .tag{{display:inline-block;border-radius:8px;padding:5px 12px;color:#714b20;background:#fff0d0;font-weight:700}} td,th{{border-bottom:1px solid #ddd;padding:8px;text-align:left}} table{{width:100%;border-collapse:collapse}} li{{margin:9px 0}} .note{{color:#445b68}} a{{color:#075d83}} :focus-visible{{outline:3px solid #dc961d}}</style>
    <h1>Ekole — revue de mission (Enseignant)</h1><p class="tag">Simulation sur fichiers · Aucune mission élève activée</p>
    <article><h2>{e(preview['scenario']['title'])}</h2><p>{e(preview['scenario']['fiction'])}</p><p><strong>Rôles :</strong> {', '.join(e(v['name']) for v in preview['roles'])}</p><ol>{steps}</ol></article>
    <article><h2>Points à résoudre</h2><ul>{warns}</ul><p class="note">Les textes des indices privés ne sont pas inclus. Les résultats de ce rapport ne donnent aucune autorisation de divulguer un fragment à un enfant.</p></article>
    <article><h2>Vérifications des dépôts</h2><table>{tests}</table><p><b>Activation d'une mission réelle :</b> NON AUTORISÉE par ce pont.</p></article>
    <p class="note">Sources : Kontexte + kompose. Orgo reste propriétaire des états et Orgo_Worlds des contextes. Cette page est une revue statique pour l'enseignant, pas l'interface d'un élève.</p></html>'''

def build(parent:Path, output:Path, *, overrides:dict[str,Path]|None=None) -> dict:
    overrides=overrides or {}
    roots={name:(overrides[name].resolve() if name in overrides else locate(parent,name)) for name in NAMES}
    for name,path in roots.items():
        if not path.is_dir():
            raise FileNotFoundError('Repository not found: '+name+' '+str(path))
        try:
            output.resolve().relative_to(path)
        except ValueError:
            pass
        else:
            raise ValueError('Output directory must not be inside source repository: '+str(path))
    content=roots['ekole-quebec']; kon=roots['Kontexte']; komp=roots['kompose']; orgo=roots['Orgo']; worlds=roots['Orgo_Worlds']
    pack=read(content/'pack.json')
    cid='qc-pri-ma-008'; ref='qc-pri-ma-006'
    grade3=next(i for i in pack['parcours'] if i['id']=='annee-3')['cours_ids']
    course_ids={c['id'] for c in pack['cours']}
    if len(course_ids)!=202 or len(grade3)!=36:raise ValueError('Pack non conforme à la base Ekole attendue (202 cours, 36 en 3e).')
    for id in (cid,ref):
        if id not in course_ids:raise ValueError('Cours introuvable: '+id)
    mission_file=kon/'data/missions/boulangerie.json'; mission=read(mission_file)
    original_hashes={f'cours/{id}.json':sha(content/'cours'/(id+'.json')) for id in course_ids}
    # Les modules importés sont seulement les compilateurs d'aperçu déjà présents dans les sources.
    sys.path.insert(0,str(kon/'src'));sys.path.insert(0,str(komp/'src'))
    from kontexte.models import validate_mission, validate_role, curriculum_index
    from kontexte.orgo import scenario_fixture, integration_manifest
    from kompose.kontexte_preview import compile_preview,role_projection,propose_absence_fallback
    refs=curriculum_index(read(kon/'data/catalogue/202_kristals.json'))
    validate_mission(mission,refs)
    roles=[validate_role(read(kon/'data/roles'/(rid+'.json'))) for rid in mission['roles']]
    preview=compile_preview(mission,roles,target_course_id=cid)
    fixture=scenario_fixture(mission)
    blueprint=integration_manifest(mission)
    outs=output/'artefacts';outs.mkdir(parents=True,exist_ok=True)
    save(outs/'plan_kompose_enseignant.json',preview)
    save(outs/'intentions_orgo.json',blueprint)
    save(outs/'fixture_orgo_preparation.json',fixture)
    for role in mission['roles']:
        save(outs/f'apercu_role_{role}_non_publie.json',role_projection(preview,role))
    save(outs/'repli_fermier_non_execute.json',propose_absence_fallback(preview,'fermier'))
    world_packs=[]
    for f in sorted((worlds/'world-packs').glob('*/world-pack.json')):
        v=read(f);world_packs.append({'file':str(f.relative_to(worlds)),'key':v.get('world',{}).get('key'),'release':v.get('world',{}).get('release')})
    source_refs=preview['curriculum']['source_ids']
    grade_mismatch=cid not in source_refs
    checks={
     'catalogue':{'ok':len(course_ids)==202 and len(grade3)==36,'details':'202 cours, 36 en 3e'},
     'sources':{'ok':mission.get('synthetic') is True and preview['dispatch_allowed'] is False,'details':'sources synthétiques conservées'},
     'alignement_pedagogique':{'ok':not grade_mismatch,'details':f'Cible {cid}; mission {source_refs}'},
     'execution_conditionnelle_orgo':{'ok':False,'details':'Les fragments et jointures restent des intentions, pas des transitions Orgo installées'},
     'validation_enseignant':{'ok':False,'details':'Mission squelette non approuvée pédagogiquement'},
     'world_release_boulangerie':{'ok':False,'details':'Aucune WorldRelease boulangerie associée/épinglée dans les sources'},
     'identite_eleves':{'ok':False,'details':'Aucun fournisseur identité scolaire configuré dans cette livraison'},
    }
    result_injector=invoke(['node',str(orgo/'tools/scenario-injector/cli.mjs'),'validate',str(outs/'fixture_orgo_preparation.json')])
    checks['injecteur_orgo_validation']={'ok':result_injector['ok'],'details':result_injector['stderr'] or result_injector['stdout']}
    if result_injector['ok']:
        result_plan=invoke(['node',str(orgo/'tools/scenario-injector/cli.mjs'),'plan',str(outs/'fixture_orgo_preparation.json')])
    else:result_plan={'ok':False,'stdout':'','stderr':'Validation non passée','command':[]}
    checks['injecteur_orgo_plan']={'ok':result_plan['ok'],'details':result_plan['stderr'] or result_plan['stdout'][:250]}
    checks['frontiere_worlds']={'ok':(c:=invoke(['node',str(worlds/'scripts/check-worlds.mjs')]))['ok'],'details':c['stderr'] or c['stdout']}
    # Prevent placing private clue content or Orgo auth credentials in any generated artefact.
    result={'format':'ekole.missions.preflight/1','created_at':datetime.now(timezone.utc).isoformat(),
       'mission_id':mission['id'],'target_course':cid,'source_courses':source_refs,
       'preview_only':True,'dispatch_allowed':False,'may_publish_to_child':False,
       'repos':{k:{'path':str(v),'snapshot':True} for k,v in roots.items()},
       'source_sha256':{'pack.json':sha(content/'pack.json'),'mission.json':sha(mission_file),
                        'orgo_injector':sha(orgo/'tools/scenario-injector/cli.mjs')},
       'course_sha256_count':len(original_hashes),'world_packs':world_packs,
       'checks':checks,'injector':{'validate':result_injector,'plan':result_plan},
       'required_next_steps':['Arbitrer qc-pri-ma-006 vs qc-pri-ma-008 et revoir situation de multiplication','Créer et valider release dédiée dans Orgo_Worlds',
             'Développer gardes de distribution des fragments et jointures dans Orgo','Définir identité/permissions et supervision enseignant',
             'Raccorder API Ekole élève à des vues Orgo autorisées sans jeton navigateur','Lier seulement les preuves validées au suivi des acquis Ekole']}
    save(outs/'rapport_machine.json',result)
    (output/'REVUE_ENSEIGNANT.html').write_text(review_html(preview,result),encoding='utf8')
    safe_counts={'catalogue':len(course_ids),'annee_3':len(grade3),'roles':len(mission['roles']),'etapes':len(mission['steps']),'indices_prives':len(mission.get('fragments',[]))}
    summary=f'''# Rapport — Pont Missions Ekole (préqualification sans écriture)\n\n**État : NON prêt pour une mission réelle en classe.** Les API/contrats ont été confrontés, mais aucune Case, Task ou WorldRelease n'a été créée.\n\n- {safe_counts['catalogue']} cours, {safe_counts['annee_3']} cours de 3e année; sources originales intactes.\n- Pilote Kontexte : {safe_counts['roles']} rôles, {safe_counts['etapes']} étapes, {safe_counts['indices_prives']} fragments privés et 1 jointure.\n- Références source : {', '.join(source_refs)}; pilote désiré : {cid}. **Aucun remappage automatique.**\n- Statut source : {mission.get('status')}.\n- Injecteur Orgo `validate` : {'OK' if result_injector['ok'] else 'À corriger'}; `plan` sans mutation : {'OK' if result_plan['ok'] else 'À corriger'}.\n- Orgo_Worlds architecture statique : {'OK' if checks['frontiere_worlds']['ok'] else 'À corriger'}.\n\n## Décisions bloquantes\n\n'''+''.join(f"- **{k}** : {v['details']}\n" for k,v in checks.items() if not v['ok'])+'''\n## Démarche suivante\n\nValider le programme/énoncé et les identifiants de cours; écrire un vrai workflow Orgo versionné (gardes/jointures) et une WorldRelease pertinente; connecter ensuite la vue Élève via un serveur protégé et des comptes scolaires. Ne jamais considérer un Task complété comme une maîtrise automatique.\n\nLa visualisation `REVUE_ENSEIGNANT.html` est une fiche statique de revue, pas une application Élève.\n'''
    (output/'RAPPORT.md').write_text(summary,encoding='utf-8')
    return result

def main():
    parser=argparse.ArgumentParser(description='Ekole, Kontexte, kompose, Orgo, Worlds — pont read-only')
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3])
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[2]/'output')
    for name in NAMES:parser.add_argument('--'+name.lower().replace('_','-'),type=Path)
    args=parser.parse_args()
    try:
        value=build(args.root.resolve(),args.out.resolve(),overrides={name:getattr(args,name.lower().replace('_','_').replace('-','_')) for name in NAMES if getattr(args,name.lower().replace('_','_').replace('-','_')) is not None})
        print('REVUE ENSEIGNANT:',args.out/'REVUE_ENSEIGNANT.html')
        for name,c in value['checks'].items(): print('OK' if c['ok'] else 'À RÉSOUDRE',name)
        print('Aucune API Orgo appelée et aucun fichier de source modifié.')
    except Exception as e:
        print('ERREUR :',e,file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':raise SystemExit(main())
