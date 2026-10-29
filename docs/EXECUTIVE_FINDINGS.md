# Operational exception analysis — fictional demonstration

## Business question
Can repeatable validation produce a reviewable exception queue before analysts rely on exported data?

## Verified baseline
`python pipeline.py` identified three issues across six fictional records: one possible duplicate customer/stage, one missing email, and one missing agent ID. Both original unit tests passed.

## Benchmark
`python benchmark.py` generates 5,000 clean fictional records and times the **original** validator. One local execution processed 5,000 records in about 0.0112 seconds. This is a machine-dependent sample, not production throughput or measured time savings.

## Recommended process
Validate source headers, route missing contacts and agent mappings to designated owners, review duplicates before changing records, and retain the JSON/CSV exception queue for audit review.

## Limits
No real customer information, production deployment, financial savings or comparison against manual processing is claimed. The enhanced multi-feed workflow requires separate verification.
