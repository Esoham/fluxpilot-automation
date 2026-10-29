import sys,unittest,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import analyze
class PipelineTests(unittest.TestCase):
    def test_expected_exceptions(self):
        result=analyze(Path(__file__).resolve().parents[1]/'data'/'applications.csv')
        self.assertEqual(result['records'],6)
        self.assertEqual(result['issue_counts'],{'missing_agent_id':1,'missing_email':1,'possible_duplicate_customer_stage':1})
    def test_unknown_stage(self):
        with tempfile.TemporaryDirectory() as temp:
            file=Path(temp)/'test.csv'
            file.write_text('application_id,borrower_key,email,stage,agent_id,updated_at\nX1,C1,a@example.test,unknown,A1,2026-01-01\n')
            self.assertEqual(analyze(file)['issue_counts']['unknown_stage'],1)
if __name__=='__main__':unittest.main()
