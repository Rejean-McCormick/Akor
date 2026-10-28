"""Akor integration guarantees; synthetic partner validators stand in during unit tests."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from akor.tandem_gate import GateError, main, verify_handoff

TENANT='11111111-1111-4111-8111-111111111111'
WORLD='22222222-2222-4222-8222-222222222222'
RELEASE='33333333-3333-4333-8333-333333333333'

# Test doubles exercise the Akor boundary; release validation must separately
# exercise real Kompose V3 and Ekole P1 owner modules.
KM="""import json
from pathlib import Path
def load_teacher_preview(path):
  p=Path(path)
  if p.is_symlink() or not p.is_file(): raise ValueError('file')
  def pairs(items):
    d={}
    for k,v in items:
      if k in d: raise ValueError('duplicates')
      d[k]=v
    return d
  v=json.loads(p.read_text('utf-8'),object_pairs_hook=pairs)
  if set(v)!={'format','mode','authority','tenant_id','world_id','world_release_id','scenario_ref','workflow_ref','tasks'} or v['mode']!='synthetic': raise ValueError('untrusted')
  return v
"""
EK="""def validate_synthetic_preview(v):
  if v['format']!='ekole.tandem-teacher-preview/1.0' or v['authority']!='orgo':raise ValueError('format')
  for t in v['tasks']:
    if set(t)!={'task_ref','role_code','state','fragment_refs'}:raise ValueError('fields')
  return v
"""

class TandemGateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='akor-tandem-tests-')
        self.addCleanup(self.temp.cleanup)
        r=Path(self.temp.name)
        self.ko=r/'Kontexte';self.km=r/'Kompose';self.ek=r/'ekole';self.preview=r/'fixture.json'
        for path, content in ((self.km/'src/kompose/tandem_handoff.py',KM), (self.ek/'tandem/projection.py',EK)):
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
        self.mission_file=self.ko/'data/missions/fete-sorciere.json'
        self.mission_file.parent.mkdir(parents=True)
        self.mission={'id':'fete-sorciere','format':'kontexte.mission/1','synthetic':True,
                      'steps':[{'id':'step-one','role':'sorciere'},{'id':'step-two','role':'marchand'}],
                      'fragments':[{'content':{'fr-CA':'ne jamais publier cet indice'}}]}
        self.document={'format':'ekole.tandem-teacher-preview/1.0','mode':'synthetic','authority':'orgo',
                       'tenant_id':TENANT,'world_id':WORLD,'world_release_id':RELEASE,
                       'scenario_ref':'fete-sorciere','workflow_ref':'sorciere-v1',
                       'tasks':[{'task_ref':x['id'],'role_code':x['role'],'state':'ready','fragment_refs':[]} for x in self.mission['steps']]}
        self.write()

    def write(self):
        self.mission_file.write_text(json.dumps(self.mission),encoding='utf-8')
        self.preview.write_text(json.dumps(self.document),encoding='utf-8')

    def verify(self, **kwargs):
        args=dict(kontexte=self.ko,kompose=self.km,ekole=self.ek,preview=self.preview,
                  tenant_id=TENANT,world_id=WORLD,world_release_id=RELEASE)
        args.update(kwargs)
        return verify_handoff(**args)

    def test_synthetic_valid_but_never_granted(self):
        result=self.verify()
        self.assertEqual(result['task_count'],2)
        for name in ('runtime_admitted','teacher_authorized','permissions_verified','world_release_verified',
                     'dispatch_allowed','may_publish_to_child'):
            self.assertFalse(result[name])
        self.assertTrue(result['declared_scope_matches'])
        self.assertNotIn('ne jamais publier',json.dumps(result))
        self.assertNotIn('tasks',result)

    def test_wrong_tenant_rejected(self):
        with self.assertRaises(GateError): self.verify(tenant_id=WORLD)

    def test_wrong_world_rejected(self):
        with self.assertRaises(GateError): self.verify(world_id=TENANT)

    def test_wrong_release_rejected(self):
        with self.assertRaises(GateError): self.verify(world_release_id=TENANT)

    def test_zero_expected_uuid_rejected(self):
        with self.assertRaises(GateError): self.verify(tenant_id='00000000-0000-0000-0000-000000000000')

    def test_private_field_rejected_by_owner(self):
        self.document['tasks'][0]['student_name']='fictional pupil'
        self.write()
        with self.assertRaises(GateError): self.verify()

    def test_non_synthetic_source_rejected(self):
        self.mission['synthetic']=False;self.write()
        with self.assertRaises(GateError): self.verify()

    def test_wrong_step_ref_rejected(self):
        self.document['tasks'][0]['task_ref']='invented';self.write()
        with self.assertRaises(GateError): self.verify()

    def test_wrong_role_rejected(self):
        self.document['tasks'][0]['role_code']='other';self.write()
        with self.assertRaises(GateError): self.verify()

    def test_duplicate_mission_json_rejected(self):
        self.mission_file.write_text('{"id":"fete-sorciere","id":"overridden"}',encoding='utf-8')
        with self.assertRaises(GateError): self.verify()

    def test_bad_scenario_ref_cannot_escape_root(self):
        self.document['scenario_ref']='../../sensitive';self.write()
        with self.assertRaises(GateError): self.verify()

    def test_missing_owner_module_fails_closed(self):
        (self.ek/'tandem/projection.py').unlink()
        with self.assertRaises(GateError): self.verify()

    def test_missing_source_fails_closed(self):
        self.mission_file.unlink()
        with self.assertRaises(GateError): self.verify()

    def test_symlink_mission_is_rejected(self):
        target=self.mission_file.with_name('other.json')
        self.mission_file.rename(target)
        try:self.mission_file.symlink_to(target)
        except OSError:self.skipTest('symlink privilege not available')
        with self.assertRaises(GateError):self.verify()

    def test_report_cli_never_mutates(self):
        before=self.preview.read_bytes();source=self.mission_file.read_bytes()
        args=['--kontexte',str(self.ko),'--kompose',str(self.km),'--ekole',str(self.ek),
              '--preview',str(self.preview),'--tenant-id',TENANT,'--world-id',WORLD,'--world-release-id',RELEASE]
        self.assertEqual(main(args),0)
        self.assertEqual(self.preview.read_bytes(),before)
        self.assertEqual(self.mission_file.read_bytes(),source)

if __name__=='__main__':unittest.main()
