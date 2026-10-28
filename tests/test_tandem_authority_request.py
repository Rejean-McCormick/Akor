import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from akor.tandem_authority_request import from_intent_bytes, from_intent_path, AdmissionRequestDenied

ROOT=Path(__file__).resolve().parents[1]
RAW=(ROOT/'examples/tandem/fete-sorciere.11-tasks.intent.synthetic.json').read_bytes()

class AuthorityRequestTests(unittest.TestCase):
    def test_11_tasks_are_only_request_not_permission(self):
        result=from_intent_bytes(RAW)
        self.assertEqual(result['task_count'],11)
        self.assertEqual(result['status'],'AWAITING_SERVER_VERIFICATION')
        for field in ('runtime_admitted','teacher_authorized','permissions_verified','world_release_verified','dispatch_allowed','may_publish_to_child'):
            self.assertIs(result[field],False)
        self.assertNotIn('tasks',result) # no payload to child
        self.assertNotIn('permissions',result)
    def test_stable_sha(self):
        self.assertEqual(from_intent_bytes(RAW), from_intent_path(ROOT/'examples/tandem/fete-sorciere.11-tasks.intent.synthetic.json'))
    def test_forged_permission_flag_denied(self):
        for flag in ('teacher_authorized','runtime_admitted','permissions_verified','dispatch_allowed'):
            with self.subTest(flag=flag):
                obj=json.loads(RAW);obj[flag]=True
                with self.assertRaises(AdmissionRequestDenied):from_intent_bytes(json.dumps(obj).encode())
    def test_extra_child_personal_field_denied(self):
        obj=json.loads(RAW);obj['child_name']='Fake'
        with self.assertRaises(AdmissionRequestDenied):from_intent_bytes(json.dumps(obj).encode())
    def test_duplicate_nested_field_denied(self):
        raw=RAW.replace(b'"task_ref":',b'"task_ref":"evil","task_ref":',1)
        with self.assertRaises(AdmissionRequestDenied):from_intent_bytes(raw)
    def test_duplicate_task_denied(self):
        obj=json.loads(RAW);obj['tasks'].append(dict(obj['tasks'][0]))
        with self.assertRaises(AdmissionRequestDenied):from_intent_bytes(json.dumps(obj).encode())
    def test_invalid_scope_denied(self):
        obj=json.loads(RAW);obj['world_id']='not-a-world'
        with self.assertRaises(AdmissionRequestDenied):from_intent_bytes(json.dumps(obj).encode())
    def test_no_overlarge_or_nan(self):
        for raw in (b' '*(262145),RAW[:-1]+b'Infinity}', b'{}'):
            with self.assertRaises(AdmissionRequestDenied):from_intent_bytes(raw)
