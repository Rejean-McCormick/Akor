"""P3: untrusted, synthetic request for server-side authority checks; NEVER an approval.

This creates no actors, teacher permissions, student identities, Orgo tasks or tokens.
The eventual Orgo admission adapter must authenticate and authorize independently.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from uuid import UUID

MAX_BYTES = 262_144
FLAGS = ('runtime_admitted','teacher_authorized','permissions_verified','world_release_verified',
         'dispatch_allowed','may_publish_to_child')
KEYS = frozenset(('format','mode','authority','scenario_ref','workflow_ref','tenant_id',
 'world_id','world_release_id','source_sha256','preview_sha256','tasks',*FLAGS))

class AdmissionRequestDenied(ValueError):
    pass

def _deny(message):
    raise AdmissionRequestDenied(message)

def _pairs(pairs):
    found = {}
    for k, v in pairs:
        if k in found: _deny('duplicate JSON key')
        found[k] = v
    return found

def _ref(s):
    return isinstance(s, str) and 1 <= len(s) <= 80 and s[0].isalnum() and s[0].islower() and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in s)

def _uuid(s):
    if not isinstance(s, str): return False
    try: u=UUID(s)
    except (ValueError, AttributeError): return False
    return u.int != 0 and str(u) == s and u.version in range(1, 9)

def from_intent_bytes(raw: bytes) -> dict:
    """Parse untrusted P2 intent into a non-authoritative request; no permissions input."""
    if not isinstance(raw, bytes) or not (1 <= len(raw) <= MAX_BYTES): _deny('intent size')
    try:
        value = json.loads(raw.decode('utf-8', errors='strict'), object_pairs_hook=_pairs,
                           parse_constant=lambda _: _deny('non-finite JSON'))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as e: raise AdmissionRequestDenied('invalid JSON') from e
    if type(value) is not dict or set(value) != KEYS: _deny('P2 intent field allowlist')
    if value['format'] != 'akor.tandem-execution-intent/1.0' or value['mode'] != 'synthetic' or value['authority'] != 'orgo': _deny('wrong P2 intent')
    for k in FLAGS:
        if value[k] is not False: _deny('untrusted authority claim: '+k)
    for k in ('tenant_id','world_id','world_release_id'):
        if not _uuid(value[k]): _deny('invalid UUID '+k)
    for k in ('source_sha256','preview_sha256'):
        v = value[k]
        if not isinstance(v, str) or len(v) != 64 or any(c not in '0123456789abcdef' for c in v): _deny('invalid hash')
    for k in ('scenario_ref','workflow_ref'):
        if not _ref(value[k]): _deny('invalid reference')
    tasks = value['tasks']
    if type(tasks) is not list or not (1 <= len(tasks) <= 50): _deny('task bound')
    seen=set()
    for t in tasks:
        if type(t) is not dict or set(t) != {'task_ref','role_code'} or not all(_ref(t[k]) for k in ('task_ref','role_code')): _deny('untrusted task shape')
        if t['task_ref'] in seen: _deny('duplicate task')
        seen.add(t['task_ref'])
    return {
      'format':'akor.tandem-authority-request/1.0', 'mode':'synthetic',
      'status':'AWAITING_SERVER_VERIFICATION', 'authority':'orgo',
      'scenario_ref':value['scenario_ref'], 'workflow_ref':value['workflow_ref'],
      'tenant_id':value['tenant_id'], 'world_id':value['world_id'],
      'world_release_id':value['world_release_id'],
      'intent_sha256':hashlib.sha256(raw).hexdigest(),
      'task_count':len(tasks), 'runtime_admitted':False,
      'teacher_authorized':False, 'permissions_verified':False,
      'world_release_verified':False, 'dispatch_allowed':False,
      'may_publish_to_child':False,
    }

def from_intent_path(path: Path) -> dict:
    if path.is_symlink() or not path.is_file() or not (1 <= path.stat().st_size <= MAX_BYTES): _deny('invalid intent file')
    return from_intent_bytes(path.read_bytes())
