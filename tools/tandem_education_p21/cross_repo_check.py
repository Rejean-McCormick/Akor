"""Read-only Akor/Orgo_Worlds/Orgo P2 synthetic contract chain.

This checks pinned local scripts/fixtures only, never invokes a service or database.
"""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,tempfile
DENIES=('runtime_admitted','teacher_authorized','permissions_verified',
        'world_release_verified','dispatch_allowed','may_publish_to_child')

def fail(s):raise RuntimeError(s)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load_obj(p):
    def no_dupes(pairs):
        result={}
        for k,v in pairs:
            if k in result:fail('Duplicate JSON key '+k)
            result[k]=v
        return result
    if not p.is_file() or p.is_symlink() or not 0<p.stat().st_size<=262144:fail('Unsafe JSON input '+str(p))
    return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=no_dupes)

def pinned(root,relative):
    manifest=root/'tools/tandem_education_p2/manifest.json'
    content=load_obj(manifest)
    pinned={spec['path']:spec['new'] for spec in content['files']}
    if relative not in pinned:fail('P2 manifest missing file '+relative)
    p=root/relative
    if not p.is_file() or p.is_symlink() or sha(p)!=pinned[relative]:fail('P2 file divergent: '+relative)
    return p

def node(path,*args):
    cmd=['node',str(path),*map(str,args)]
    cp=subprocess.run(cmd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                      encoding='utf-8',errors='replace',timeout=20,check=False)
    if cp.returncode:fail('P2 offline gate refused: '+cp.stderr.strip()[:350])
    try:return json.loads(cp.stdout)
    except ValueError:fail('Invalid gate output')

def main():
    parser=argparse.ArgumentParser(description='Offline P2 multi-repo synthetic contract qualification')
    parser.add_argument('--akor',type=Path,required=True)
    parser.add_argument('--worlds',type=Path,required=True)
    parser.add_argument('--orgo',type=Path,required=True)
    a=parser.parse_args()
    akor=a.akor.resolve(strict=True)
    worlds=a.worlds.resolve(strict=True)
    orgo=a.orgo.resolve(strict=True)
    intent_file=pinned(akor,'examples/tandem/fete-sorciere.11-tasks.intent.synthetic.json')
    script_worlds=pinned(worlds,'scripts/tandem-education/scope-review.mjs')
    world_fixture=pinned(worlds,'scripts/tandem-education/fixtures/fete-sorciere.world.synthetic.json')
    script_orgo=pinned(orgo,'tools/tandem-education/review-plan.mjs')
    orgo_fixture=pinned(orgo,'tools/tandem-education/fixtures/fete-sorciere.intent.synthetic.json')
    intent=load_obj(intent_file);compare=load_obj(orgo_fixture)
    if intent!=compare:fail('Akor and Orgo P2 intents differ (stale fixture)')
    if len(intent.get('tasks',[]))!=11:fail('Expected 11 P2 tasks')
    scope=node(script_worlds,intent_file,world_fixture)
    for k in DENIES:
        if scope.get(k) is not False:fail('Authority falsely granted in Worlds output: '+k)
    if scope.get('scope_consistent') is not True:fail('Synthetic scope mismatch')
    with tempfile.TemporaryDirectory(prefix='tandem-p2-crossrepo-') as work:
        report=Path(work)/'scope.json'
        report.write_text(json.dumps(scope,ensure_ascii=False)+'\n',encoding='utf-8')
        plan=node(script_orgo,intent_file,report)
    if plan.get('status')!='REVIEW_ONLY' or plan.get('task_count')!=11 or plan.get('planned_case_count')!=1 or plan.get('planned_task_count')!=11:
        fail('Orgo synthetic plan not aligned with 11 tasks/1 Case')
    if [t['task_ref'] for t in intent['tasks']]!=plan.get('task_refs'):fail('Task refs altered')
    if plan.get('db_writes')!=0 or plan.get('network_calls')!=0 or plan.get('workflow_published') is not False:
        fail('Review plan cannot claim effects')
    for k in DENIES:
        if intent.get(k) is not False or plan.get(k) is not False:fail('Authority cannot be claimed: '+k)
    print(json.dumps({'format':'tandem-education.cross-repo-offline-qualification/1.0',
        'status':'PASS_REVIEW_ONLY','repositories':['Akor','Orgo_Worlds','Orgo'],
        'scenario_ref':intent['scenario_ref'],'task_count':11,'planned_case_count':1,
        'scope_consistent':True,'runtime_admitted':False,'teacher_authorized':False,
        'permissions_verified':False,'world_release_verified':False,'dispatch_allowed':False,
        'may_publish_to_child':False,'workflow_published':False,'db_writes':0,'network_calls':0},
        indent=2))
    return 0
if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as e:
        print('[FAIL]',e,file=sys.stderr);sys.exit(1)
