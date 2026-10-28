"""Repair only the Akor P2 test-copy manifest. Offline, SHA-pinned, reversible.

P2.1 will NOT write to services, application sources, Orgo, databases or child data.
"""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
PKG=Path(__file__).resolve().parent
ROOT=PKG.parents[1]
MANIFEST=json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
COPY=['README.md','src','tests','run_akor.py','run_akor_tandem.py',
      'run_akor_tandem_intent.py','docs/TANDEM_AKOR_INTEROP_SECURITY_P1.md',
      'examples/sample_review','examples/tandem/fete-sorciere.11-tasks.intent.synthetic.json',
      'docs/TANDEM_EDUCATION_P2_REVIEW_ONLY.md','tools/tandem_education_p2']

def sha(path):
    if not path.is_file():return None
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def fail(msg):raise RuntimeError(msg)

def rel(raw):
    if not isinstance(raw,str) or not raw or raw.startswith('/') or '\\' in raw or ':' in raw or any(x in ('','.','..') for x in raw.split('/')):fail('Unsafe path: '+repr(raw))
    return Path(*raw.split('/'))

def safe(root,raw):
    root=root.resolve(strict=True)
    target=root/rel(raw)
    p=target
    while p!=root:
        if p.is_symlink():fail('Symlink forbidden: '+raw)
        if p==p.parent:fail('Path escapes repository: '+raw)
        p=p.parent
    return target

def integrity():
    if not safe(ROOT,MANIFEST['sentinel']).is_file():fail('Not an Akor repository root')
    for raw,wanted in MANIFEST['anchors'].items():
        if sha(safe(ROOT,raw))!=wanted:fail('Pinned P2 source changed: '+raw)
    for e in MANIFEST['files']:
        if sha(safe(PKG,'payload/'+e['path']))!=e['new']:fail('Payload hash mismatch: '+e['path'])

def scan():
    output=[]
    for e in MANIFEST['files']:
        raw=e['path']; target=safe(ROOT,raw)
        if target.exists() and not target.is_file():status='CONFLICT'
        else:
            found=sha(target)
            status='ALREADY_UPDATED' if found==e['new'] else 'READY' if found==e['old'] else 'CONFLICT'
        print(f'[{status}] {raw}',flush=True)
        output.append((e,status))
    if any(s=='CONFLICT' for _,s in output):fail('Source SHA-256 diverged; no change made')
    return output

def atomic(target,contents):
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='wb',delete=False,dir=target.parent,prefix='.tandem-p21-') as f:
        tmp=Path(f.name);f.write(contents)
    try:os.replace(tmp,target)
    finally:tmp.unlink(missing_ok=True)

def no_symlinks(src):
    if src.is_symlink():fail('Symlink in isolated test sources: '+str(src))
    if src.is_dir():
        for top,dirs,files in os.walk(src,followlinks=False):
            for name in dirs+files:
                if (Path(top)/name).is_symlink():fail('Symlink in isolated test sources: '+name)

def stage(path,patched):
    repo=path/'repo';repo.mkdir()
    for raw in COPY:
        src=safe(ROOT,raw);dst=repo/rel(raw)
        if not src.exists():fail('Required test source missing: '+raw)
        no_symlinks(src)
        if src.is_dir():
            dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(src,dst,symlinks=False,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache','*.pyc','.git','node_modules'))
        else:
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
    # This file must exist in both pre-install and post-install checks.
    if not (repo/'run_akor_tandem_intent.py').is_file():fail('Missing launch file in isolated copy')
    if patched:
        for e in MANIFEST['files']:
            dst=repo/rel(e['path']);shutil.copy2(safe(PKG,'payload/'+e['path']),dst)
    return repo

def tests(patched):
    with tempfile.TemporaryDirectory(prefix='akor-tandem-p21-') as tmp:
        repo=stage(Path(tmp),patched)
        m=json.loads((repo/rel('tools/tandem_education_p2/manifest.json')).read_text(encoding='utf-8'))
        if 'run_akor_tandem_intent.py' not in m['test_copy']:fail('P2 manifest still omits explicit launcher test copy')
        if ['{PYTHON}','-m','py_compile','run_akor_tandem_intent.py'] not in m['tests']:fail('P2 manifest lacks a fail-hard launcher compile')
        env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONPATH=str(repo/'src'),NO_COLOR='1')
        cmd=[sys.executable,'tools/tandem_education_p2/manager.py','VERIFY']
        print('[TEST] P2 VERIFY on independent staging copy (compile + 32 tests)',flush=True)
        run=subprocess.run(cmd,cwd=repo,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace',timeout=120,check=False)
        print(run.stdout[-6500:],flush=True)
        if run.returncode or "Can't list" in run.stdout:fail('P2 staged VERIFY incomplete (exit %s)'%run.returncode)
        print('[PASS] Explicit launcher py_compile, complete unittest suite and P2 manager VERIFICATION',flush=True)

def local():return ROOT.parent/'Tandem_Local'/MANIFEST['id']

def rollback():
    p=local()/'current.json'
    if not p.is_file():fail('No P2.1 backup to restore')
    state=json.loads(p.read_text(encoding='utf-8'))
    backup=local()/'backups'/state['stamp']
    for e in state['files']:
        dst=safe(ROOT,e['path']);old=safe(backup,e['path'])
        if sha(dst)!=e['new']:fail('Rollback refused: installed source diverged')
        if sha(old)!=e['old']:fail('Rollback backup hash mismatch')
    for e in state['files']:
        atomic(safe(ROOT,e['path']),safe(backup,e['path']).read_bytes())
        print('[RESTORED]',e['path'])
    p.unlink();print('[OK] P2.1 rollback; P2 application files unchanged')

def install(checked):
    changed=[e for e,status in checked if status=='READY']
    if not changed:
        tests(False);print('[OK] Already installed; no sources modified');return
    tests(True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup=local()/'backups'/stamp;backup.mkdir(parents=True,exist_ok=False)
    for e in changed:
        src=safe(ROOT,e['path']);dst=safe(backup,e['path'])
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
        if sha(dst)!=e['old']:fail('Backup SHA-256 mismatch')
    written=[]
    try:
        for e in changed:
            dst=safe(ROOT,e['path'])
            if sha(dst)!=e['old']:fail('Concurrent source edit')
            atomic(dst,safe(PKG,'payload/'+e['path']).read_bytes());written.append(e)
        scan();tests(False)
    except BaseException:
        for e in reversed(written):
            dst=safe(ROOT,e['path'])
            if sha(dst)==e['new']:atomic(dst,safe(backup,e['path']).read_bytes())
        print('[AUTO-ROLLBACK] Restored P2 manifest after failed install')
        raise
    atomic(local()/'current.json',(json.dumps({'stamp':stamp,'files':changed},indent=2)+'\n').encode('utf-8'))
    print('[OK] Akor P2.1 installed. Backup:',backup)

def main():
    mode=sys.argv[1].upper() if len(sys.argv)>1 else 'PREVIEW'
    if mode not in ('PREVIEW','INSTALL','VERIFY','ROLLBACK'):fail('Bad mode')
    print('=== '+MANIFEST['title']+' / '+mode+' ===')
    print('[REPO]',ROOT)
    print('[SCOPE] Installer verification only; no app, service, DB, network, or VPS changes')
    integrity()
    if mode=='ROLLBACK':rollback();return
    checked=scan()
    if mode=='PREVIEW':print('[OK] Read-only SHA-256 check');return
    if mode=='INSTALL':install(checked);return
    if any(s!='ALREADY_UPDATED' for _,s in checked):fail('P2.1 manifest not installed')
    tests(False)
    print('[OK] P2.1 launcher compilation and offline tests verified; Orgo runtime not qualified')

if __name__=='__main__':
    try:main()
    except Exception as e:
        print('[FAIL]',e,file=sys.stderr,flush=True);sys.exit(1)
