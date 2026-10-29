import sys,unittest,tempfile,json
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from automation import process
ROOT=Path(__file__).resolve().parents[1]
class AutomationTests(unittest.TestCase):
 def setUp(self):self.config=json.loads((ROOT/'rules.json').read_text())
 def test_demo_feed(self):
  report=process([ROOT/'data'/'applications.csv'],self.config,date(2026,9,15))
  self.assertEqual(report['processed_records'],6)
  self.assertEqual(report['issue_counts']['missing_email'],1)
  self.assertEqual(report['issue_counts']['missing_agent_id'],1)
 def test_cross_file_duplicate(self):
  with tempfile.TemporaryDirectory() as d:
   paths=[]
   for n in range(2):
    path=Path(d)/f'feed{n}.csv'
    path.write_text('application_id,borrower_key,email,stage,agent_id,updated_at\nX1,C1,a@example.test,submitted,A1,2026-09-14\n')
    paths.append(path)
   report=process(paths,self.config,date(2026,9,15))
   self.assertEqual(report['issue_counts']['duplicate_application_id'],1)
 def test_bad_date(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'bad.csv'
   path.write_text('application_id,borrower_key,email,stage,agent_id,updated_at\nX2,C1,a@example.test,submitted,A1,bad-date\n')
   self.assertEqual(process([path],self.config,date(2026,9,15))['issue_counts']['invalid_update_date'],1)
if __name__=='__main__':unittest.main()
