"""Configurable, deterministic multi-feed validation and exception export."""
import argparse,csv,json,logging
from collections import Counter
from datetime import date
from pathlib import Path

LOG=logging.getLogger('fluxpilot')
def process(paths,config,as_of):
    seen=set();exceptions=[];stage_counts=Counter();total=0
    required=set(config['required_columns'])
    for path in paths:
        with Path(path).open(newline='',encoding='utf-8-sig') as stream:
            reader=csv.DictReader(stream)
            if not required.issubset(set(reader.fieldnames or [])):
                raise ValueError(f'{path}: missing columns {sorted(required-set(reader.fieldnames or []))}')
            for line,row in enumerate(reader,start=2):
                total+=1;rid=row['application_id'].strip();stage=row['stage'].strip().lower();stage_counts[stage]+=1
                def flag(issue):
                    exceptions.append({'source':Path(path).name,'line':line,'application_id':rid,'issue':issue})
                if not rid:flag('missing_application_id')
                if rid in seen:flag('duplicate_application_id')
                seen.add(rid)
                for field in ('borrower_key','email','agent_id'):
                    if not row[field].strip():flag('missing_'+field)
                if stage not in config['allowed_stages']:flag('unknown_stage')
                try:
                    age=(as_of-date.fromisoformat(row['updated_at'])).days
                    if age>config['stale_after_days']:flag('stale_record')
                    if age<0:flag('future_update_date')
                except ValueError:flag('invalid_update_date')
    return {'data_classification':'synthetic_demo','as_of':as_of.isoformat(),'processed_records':total,
            'stage_counts':dict(sorted(stage_counts.items())),
            'issue_counts':dict(sorted(Counter(e['issue'] for e in exceptions).items())),
            'exceptions':exceptions}
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs',nargs='*',type=Path)
    parser.add_argument('--config',type=Path,default=Path(__file__).parent/'rules.json')
    parser.add_argument('--as-of',type=date.fromisoformat,default=date(2026,9,15))
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'output')
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,format='%(levelname)s %(message)s')
    config=json.loads(args.config.read_text(encoding='utf-8'))
    inputs=args.inputs or [Path(__file__).parent/'data'/'applications.csv']
    report=process(inputs,config,args.as_of)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    with (args.output_dir/'exceptions.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=['source','line','application_id','issue'])
        writer.writeheader();writer.writerows(report['exceptions'])
    LOG.info('Processed %d records, flagged %d exceptions',report['processed_records'],len(report['exceptions']))
if __name__=='__main__':main()
