"""Prepare an *untrusted* synthetic classroom review intent from validated P1 owners.

No approval, pupil identity, Orgo write, or admission is ever produced here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from .tandem_gate import GateError, _module, verify_handoff


def prepare_intent(*, kontexte: Path, kompose: Path, ekole: Path, preview: Path,
                   tenant_id: str, world_id: str, world_release_id: str) -> dict:
    proof = verify_handoff(kontexte=kontexte, kompose=kompose, ekole=ekole,
        preview=preview, tenant_id=tenant_id, world_id=world_id,
        world_release_id=world_release_id)
    if any(proof.get(flag) is not False for flag in (
            'runtime_admitted', 'teacher_authorized', 'permissions_verified',
            'world_release_verified', 'dispatch_allowed', 'may_publish_to_child')):
        raise GateError('Akor P1 may not grant authority')
    owner = _module(Path(kompose), 'src/kompose/tandem_handoff.py',
                    'akor_intent_owner_kompose')
    document = owner.load_teacher_preview(preview)
    # Re-check exact source to stop a different or stale preview from being exported.
    if hashlib.sha256(Path(preview).read_bytes()).hexdigest() != proof['preview_sha256']:
        raise GateError('Preview changed during review')
    tasks = [{'task_ref': t['task_ref'], 'role_code': t['role_code']} for t in document['tasks']]
    if len(tasks) != proof['task_count'] or len({t['task_ref'] for t in tasks}) != len(tasks):
        raise GateError('Task identity/count divergence')
    return {
        'format': 'akor.tandem-execution-intent/1.0',
        'mode': 'synthetic', 'authority': 'orgo',
        'scenario_ref': proof['scenario_ref'],
        'workflow_ref': document['workflow_ref'],
        'tenant_id': tenant_id.lower(), 'world_id': world_id.lower(),
        'world_release_id': world_release_id.lower(),
        'source_sha256': proof['source_sha256'],
        'preview_sha256': proof['preview_sha256'],
        'tasks': tasks, 'runtime_admitted': False,
        'teacher_authorized': False, 'permissions_verified': False,
        'world_release_verified': False, 'dispatch_allowed': False,
        'may_publish_to_child': False,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description='Akor P2 SYNTHETIC REVIEW ONLY (no Orgo call)')
    for name in ('kontexte','kompose','ekole','preview'):
        p.add_argument('--'+name,required=True,type=Path)
    for name in ('tenant-id','world-id','world-release-id'):
        p.add_argument('--'+name,required=True)
    args=p.parse_args(argv)
    try:
        result=prepare_intent(kontexte=args.kontexte,kompose=args.kompose,
           ekole=args.ekole,preview=args.preview,tenant_id=args.tenant_id,
           world_id=args.world_id,world_release_id=args.world_release_id)
    except (GateError, OSError, ValueError, KeyError, TypeError) as exc:
        print('[REFUS] '+str(exc),file=__import__('sys').stderr)
        return 1
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
