from pathlib import Path
import json
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from akor.tandem_intent import prepare_intent
import test_tandem_gate as fixtures
TENANT, WORLD, RELEASE = fixtures.TENANT, fixtures.WORLD, fixtures.RELEASE

class IntentTests(unittest.TestCase):
    setUp = fixtures.TandemGateTests.setUp
    write = fixtures.TandemGateTests.write
    def intent(self):
        return prepare_intent(kontexte=self.ko,kompose=self.km,ekole=self.ek,
            preview=self.preview,tenant_id=TENANT,world_id=WORLD,world_release_id=RELEASE)
    def test_minimal_intent_has_no_private_fragments_or_student_info(self):
        result=self.intent()
        self.assertEqual(len(result['tasks']),2)
        self.assertEqual(result['format'],'akor.tandem-execution-intent/1.0')
        self.assertNotIn('ne jamais publier',json.dumps(result))
        self.assertTrue(all(set(t)=={'task_ref','role_code'} for t in result['tasks']))
    def test_all_authorizations_denied(self):
        result=self.intent()
        for key in ('runtime_admitted','teacher_authorized','permissions_verified',
                'world_release_verified','dispatch_allowed','may_publish_to_child'):
            self.assertIs(result[key],False)
    def test_reject_wrong_references(self):
        with self.assertRaises(ValueError):
            prepare_intent(kontexte=self.ko,kompose=self.km,ekole=self.ek,
               preview=self.preview,tenant_id=WORLD,world_id=WORLD,world_release_id=RELEASE)
    def test_reject_private_field(self):
        self.document['tasks'][0]['child_name']='not allowed'
        self.write()
        with self.assertRaises(ValueError): self.intent()

if __name__=='__main__':unittest.main()
