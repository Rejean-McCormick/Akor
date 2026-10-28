"""Akor Tandem P2.2: offline-only Windows chain launcher repair.

Replaces exactly one .cmd after SHA verification. Never writes other repositories.
"""
from __future__ import annotations
import hashlib,json,os,shutil,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path
PKG=Path(__file__).resolve().parent
ROOT=PKG.parents[1]
SPEC=json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))

def digest(path):
    if not path.is_file():return None
    h=hashlib.sha256()
    with path.open('rb') as src:
        for block in iter(lambda:src.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def fail(reason):raise RuntimeError(reason)

def safe(root,raw):
    if not raw or raw.startswith('/') or '\\' in raw or ':' in raw or any(c in ('','.','..') for c in raw.split('/')):
        fail('Unsafe path '+repr(raw))
    root=root.resolve(strict=True)
    path=root.joinpath(*raw.split('/'))
    q=path
    while q!=root:
        if q.is_symlink():fail('Symbolic link refused: '+str(q))
        q=q.parent
    return path

def verify_anchors():
    if not safe(ROOT,SPEC['sentinel']).is_file():fail('Invalid Akor repository root')
    for r,want in SPEC['anchors'].items():
        if digest(safe(ROOT,r))!=want:fail('P2/P2.1 source drift: '+r)
    for e in SPEC['files']:
        if digest(safe(PKG,'payload/'+e['path']))!=e['new']:fail('Corrupt P2.2 payload')

def status():
    result=[]
    for e in SPEC['files']:
        actual=digest(safe(ROOT,e['path']))
        s='ALREADY_UPDATED' if actual==e['new'] else 'READY' if actual==e['old'] else 'CONFLICT'
        print('['+s+']',e['path'],flush=True)
        result.append((e,s))
    if any(s=='CONFLICT' for _,s in result):fail('SHA-256 conflict; no write performed')
    return result

def selftest():
    # Syntax of the Windows batch invocation is part of the security contract.
    raw=safe(PKG,'payload/CHECK_TANDEM_EDU_P2_CHAIN.cmd').read_text(encoding='utf-8')
    for token in ('set "AKOR_ROOT=%~dp0."','set "WORLDS_ROOT=%~dp0..\\..\\..\\Orgo\\Orgo_Worlds"',
                  'set "ORGO_ROOT=%~dp0..\\..\\..\\Orgo\\Orgo"','--akor "%AKOR_ROOT%" --worlds "%WORLDS_ROOT%" --orgo "%ORGO_ROOT%"',
                  'if errorlevel 1 ('):
        if token not in raw:fail('Launcher check missing: '+token)
    if '--akor "%~dp0"' in raw:fail('Unsafe trailing slash quoted argument')
    print('[PASS] Quoted Windows argv and all required --akor/--worlds/--orgo flags')
    # We also validate the real cross-repo Python CLI independently (no execution effects).
    from subprocess import run,DEVNULL,PIPE
    p=safe(ROOT,'tools/tandem_education_p21/cross_repo_check.py')
    with tempfile.TemporaryDirectory(prefix='akor-tandem-p22-test-') as directory:
        check=Path(directory)/'cross_repo_check.py'
        shutil.copy2(p,check)
        cp=run([sys.executable,str(check),'--help'],stdin=DEVNULL,stdout=PIPE,stderr=PIPE,text=True,timeout=10)
        if cp.returncode or not all(x in cp.stdout for x in ('--akor','--worlds','--orgo')):fail('Cross-repo CLI regression')
    print('[PASS] Isolated checker CLI args validated; no services, DB or network')

def atomic(target,data):
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent,prefix='.p22-',delete=False) as f:
        tmp=Path(f.name);f.write(data)
    try:os.replace(tmp,target)
    finally:tmp.unlink(missing_ok=True)

def local():return ROOT.parent/'Tandem_Local'/SPEC['id']

def install(scanned):
    selftest()
    changed=[e for e,s in scanned if s=='READY']
    if not changed:
        print('[OK] Already updated, no write');return
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup=local()/'backups'/stamp
    backup.mkdir(parents=True,exist_ok=False)
    written=[]
    try:
        for e in changed:
            old=safe(ROOT,e['path']);dest=backup/e['path'];dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(old,dest)
            if digest(dest)!=e['old']:fail('Backup SHA-256 changed')
        for e in changed:
            dst=safe(ROOT,e['path'])
            if digest(dst)!=e['old']:fail('Source changed during install')
            atomic(dst,safe(PKG,'payload/'+e['path']).read_bytes());written.append(e)
        for e in written:
            if digest(safe(ROOT,e['path']))!=e['new']:fail('Written file SHA-256 differs')
    except BaseException:
        for e in reversed(written):
            dst=safe(ROOT,e['path']);saved=backup/e['path']
            if digest(dst)==e['new'] and digest(saved)==e['old']:atomic(dst,saved.read_bytes())
        raise
    atomic(local()/'current.json',(json.dumps({'stamp':stamp,'files':changed},indent=2)+'\n').encode())
    print('[OK] Launcher P2.2 updated. Backup:',backup)

def rollback():
    cur=local()/'current.json'
    if not cur.is_file():fail('No P2.2 install state')
    state=json.loads(cur.read_text(encoding='utf-8'))
    backup=local()/'backups'/state['stamp']
    for e in state['files']:
        if digest(safe(ROOT,e['path']))!=e['new'] or digest(safe(backup,e['path']))!=e['old']:
            fail('Rollback SHA-256 refusal: '+e['path'])
    for e in state['files']:
        atomic(safe(ROOT,e['path']),safe(backup,e['path']).read_bytes())
        print('[RESTORED]',e['path'])
    cur.unlink();print('[OK] P2.2 rollback')

def main():
    mode=sys.argv[1].upper() if len(sys.argv)>1 else 'PREVIEW'
    if mode not in ('PREVIEW','INSTALL','VERIFY','ROLLBACK'):fail('Unknown mode')
    print('=== '+SPEC['title']+' / '+mode+' ===')
    print('[REPO]',ROOT)
    print('[SCOPE] Repairs only local .cmd; no services, databases, network, Docker or VPS')
    verify_anchors()
    if mode=='ROLLBACK':rollback();return
    checked=status()
    if mode=='PREVIEW':print('[OK] Read-only SHA-256 PREVIEW');return
    if mode=='INSTALL':install(checked);return
    if any(s!='ALREADY_UPDATED' for e,s in checked):fail('P2.2 missing, run INSTALL')
    selftest()
    print('[OK] P2.2 launcher verified; execute CHECK_TANDEM_EDU_P2_CHAIN.cmd separately')

if __name__=='__main__':
    try:main()
    except Exception as ex:
        print('[ECHEC]',ex,file=sys.stderr);sys.exit(1)
