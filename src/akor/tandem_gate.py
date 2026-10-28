"""Read-only Akor P1 integration gate.

Consumes established Kontexte design and delegates preview validation to the
installed Kompose V3 and Ekole P1 owners. Never authorizes an Orgo operation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from uuid import UUID

MAX_SOURCE_BYTES = 262_144


class GateError(ValueError):
    """Interopability or safe-scope prerequisite missing."""


def _file(root: Path, rel: str) -> Path:
    root = root.resolve(strict=True)
    candidate = root.joinpath(*rel.split('/'))
    if not root.is_dir() or not candidate.is_file() or candidate.is_symlink():
        raise GateError('Source requise absente ou non reguliere: ' + rel)
    if not candidate.resolve().is_relative_to(root):
        raise GateError('Source en dehors du depot: ' + rel)
    return candidate


def _module(root: Path, rel: str, name: str):
    source = _file(root, rel)
    spec = importlib.util.spec_from_file_location(name, source)
    if spec is None or spec.loader is None:
        raise GateError('Validateur indisponible: ' + rel)
    module = importlib.util.module_from_spec(spec)
    # Trusted checked-out owner module. We do not copy or fork its rules.
    spec.loader.exec_module(module)
    return module


def _json(path: Path) -> dict:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_SOURCE_BYTES:
        raise GateError('Mission Kontexte non reguliere ou trop volumineuse')
    def unique(pairs):
        result = {}
        for key, val in pairs:
            if key in result:
                raise GateError('Cle dupliquee dans la mission Kontexte')
            result[key] = val
        return result
    try:
        value = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)
    except (OSError, UnicodeError, json.JSONDecodeError) as e:
        raise GateError('Mission Kontexte JSON invalide') from e
    if not isinstance(value,dict):
        raise GateError('Mission Kontexte non conforme')
    return value


def _uuid(text: str) -> str:
    if not isinstance(text,str):
        raise GateError('UUID attendu obligatoire')
    try:
        parsed = UUID(text)
    except (ValueError, AttributeError) as e:
        raise GateError('UUID attendu invalide') from e
    if not parsed.int or str(parsed) != text.lower():
        raise GateError('UUID attendu non canonique')
    return text.lower()


def verify_handoff(*, kontexte: Path, kompose: Path, ekole: Path,
                   preview: Path, tenant_id: str, world_id: str,
                   world_release_id: str) -> dict:
    """Fail closed on syntactic/scope drift; no teacher, WorldRelease or actor auth.

    Expected UUIDs are operator-declared synthetic fixtures, not trusted grants.
    The whole preview is never returned: that prevents accidental disclosure.
    """
    expected = {k:_uuid(v) for k,v in {
        'tenant_id':tenant_id, 'world_id':world_id,
        'world_release_id':world_release_id}.items()}
    try:
        # Invoke the two existing owner validators, not another Akor validator.
        km = _module(Path(kompose), 'src/kompose/tandem_handoff.py', 'akor_owner_kompose_tandem')
        ek = _module(Path(ekole), 'tandem/projection.py', 'akor_owner_ekole_tandem')
        document = km.load_teacher_preview(preview)
        ek.validate_synthetic_preview(document)
    except GateError:
        raise
    except Exception as exc:
        raise GateError('Handoff refuse par Kompose V3 ou Ekole P1: ' + type(exc).__name__) from exc
    for key, value in expected.items():
        if document[key].lower() != value:
            raise GateError('Contexte different de la cible explicite: ' + key)
    # Source-provenance check: Akor never exports narrative private fragments.
    scenario_ref = document['scenario_ref']
    source = _file(Path(kontexte), 'data/missions/' + scenario_ref + '.json')
    mission = _json(source)
    if mission.get('id') != scenario_ref or mission.get('format') != 'kontexte.mission/1' or mission.get('synthetic') is not True:
        raise GateError('Scenario source absent, non synthetique ou divergent')
    steps = mission.get('steps')
    if not isinstance(steps,list) or len(steps) != len(document['tasks']):
        raise GateError('Liste de missions incompatible avec le scenario Kontexte')
    source_roles = {}
    for step in steps:
        if not isinstance(step,dict) or not isinstance(step.get('id'),str) or not isinstance(step.get('role'),str) or step['id'] in source_roles:
            raise GateError('Etapes de conception invalides')
        source_roles[step['id']] = step['role']
    task_roles = {row['task_ref']:row['role_code'] for row in document['tasks']}
    if task_roles != source_roles:
        raise GateError('Divergence des etapes ou roles Kontexte / Ekole')
    return {
        'format':'akor.tandem-handoff-check/1.0',
        'status':'synthetic_preview_checked',
        'scenario_ref':scenario_ref,
        'task_count':len(steps),
        'authority':'orgo',
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'preview_sha256':hashlib.sha256(Path(preview).read_bytes()).hexdigest(),
        'declared_scope_matches':True,
        'runtime_admitted':False,
        'teacher_authorized':False,
        'permissions_verified':False,
        'world_release_verified':False,
        'dispatch_allowed':False,
        'may_publish_to_child':False,
    }


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description='Akor Tandem P1: verification synthetique locale (aucun Orgo apply)')
    for flag in ('kontexte','kompose','ekole','preview'):
        parser.add_argument('--'+flag,required=True,type=Path)
    for flag in ('tenant-id','world-id','world-release-id'):
        parser.add_argument('--'+flag,required=True)
    args=parser.parse_args(argv)
    try:
        result=verify_handoff(kontexte=args.kontexte,kompose=args.kompose,ekole=args.ekole,
                              preview=args.preview,tenant_id=args.tenant_id,world_id=args.world_id,
                              world_release_id=args.world_release_id)
    except (GateError,OSError) as exc:
        print('[REFUS] '+str(exc))
        return 1
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
