# FluxPilot — Python Workflow Automation & Exception Monitoring

An **independent portfolio project** demonstrating configurable CSV validation, cross-feed exception monitoring, automated reporting, and unit tests using fictional loan operations data.

## Business problem
Manual spreadsheet reviews are inconsistent and difficult to audit. FluxPilot standardizes checks while leaving correction decisions with a human reviewer.

## Quick start (Python 3, standard library only)
```bash
python automation.py --as-of 2026-09-15
python -m unittest discover -s tests -v
```
The enhanced workflow writes `output/summary.json` and `output/exceptions.csv`. Use multiple inputs with `python automation.py feed1.csv feed2.csv --as-of 2026-09-15`. The original `pipeline.py` remains available as a simpler introductory demonstration.

## Features
- Required-header validation with clear errors
- Configurable rules in `rules.json`
- Cross-file duplicate application-ID checks
- Missing-field and unknown-stage detection
- Stale, future and malformed update-date flags using an explicit as-of date
- JSON management summary and CSV exception register
- Automated unit tests and GitHub Actions test workflow

## Files
- `automation.py` — enhanced multi-feed workflow
- `pipeline.py` — original lightweight demonstration
- `rules.json` — configurable rules
- `data/applications.csv` — fictional input records
- `tests/` — unit tests for both workflows
- `docs/PROCESS_MAP.md` — business process and acceptance criteria

## Scope and limitations
This is not a production lender system. No actual customer information, financial decisions, real cost savings or deployment results are claimed. In production, data access, PII safeguards, audit logs, alert routing and operational ownership would be required.

## Resume-ready description
**FluxPilot | Python, CSV, JSON, GitHub Actions:** Built a configurable, multi-feed operations validation prototype that flags missing values, duplicates and stale records, exports exception reports, and runs automated tests.
