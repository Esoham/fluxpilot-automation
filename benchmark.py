"""Repeatable synthetic processing benchmark for the original lightweight validator."""
import csv,tempfile,time
from pathlib import Path
from pipeline import analyze
def benchmark(n=5000):
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'synthetic.csv'
        with path.open('w',newline='',encoding='utf-8') as file:
            writer=csv.writer(file)
            writer.writerow(['application_id','borrower_key','email','stage','agent_id','updated_at'])
            for i in range(n):
                writer.writerow([f'APP{i:06d}',f'B{i:06d}',f'b{i}@example.test','submitted','AG1','2026-09-15'])
        start=time.perf_counter()
        report=analyze(path)
        elapsed=time.perf_counter()-start
        assert report['records']==n and not report['exceptions']
        return n,elapsed
if __name__=='__main__':
    n,seconds=benchmark()
    print(f'{n} fictional records processed in {seconds:.4f}s (single machine-dependent run)')
