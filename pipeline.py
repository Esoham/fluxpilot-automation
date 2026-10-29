"""Synthetic application feed validator and reporting export; standard library only."""
from __future__ import annotations
import csv,json,argparse
from collections import Counter
from pathlib import Path

def analyze(source:Path)->dict:
    with source.open(newline='',encoding='utf-8') as file:
        records=list(csv.DictReader(file))
    required=('application_id','borrower_key','email','stage','agent_id','updated_at')
    if records and any(key not in records[0] for key in required):
        raise ValueError('Missing required CSV columns')
    flags=[];seen_ids=set();seen_customer_stage=set();stages=Counter()
    for record in records:
        rid=record['application_id'];stage=record['stage'].strip().lower();stages[stage]+=1
        if rid in seen_ids: flags.append({'application_id':rid,'issue':'duplicate_application_id'})
        seen_ids.add(rid)
        customer_stage=(record['borrower_key'].strip(),stage)
        if customer_stage in seen_customer_stage: flags.append({'application_id':rid,'issue':'possible_duplicate_customer_stage'})
        seen_customer_stage.add(customer_stage)
        if not record['email'].strip(): flags.append({'application_id':rid,'issue':'missing_email'})
        if not record['agent_id'].strip(): flags.append({'application_id':rid,'issue':'missing_agent_id'})
        if stage not in {'submitted','approved','funded','declined'}: flags.append({'application_id':rid,'issue':'unknown_stage'})
    return {'dataset':'synthetic_demo','records':len(records),'stage_counts':dict(sorted(stages.items())),
            'issue_counts':dict(sorted(Counter(f['issue'] for f in flags).items())), 'exceptions':flags}

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).resolve().parent/'data'/'applications.csv')
    p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'report.json');args=p.parse_args()
    result=analyze(args.input);args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f"Validated {result['records']} synthetic records; {len(result['exceptions'])} exceptions -> {args.output}")
if __name__=='__main__':main()
