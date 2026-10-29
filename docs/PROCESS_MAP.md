# Business workflow and controls

## Current-state scenario (fictional)
Operations analysts manually open multiple CSV exports, check missing fields, compare duplicate IDs, and compile exception reports. Rules and outputs vary by reviewer.

## Automated workflow
1. Load one or more input CSVs.
2. Validate required column headers.
3. Normalize stages for validation and reporting.
4. Flag missing values, repeated application IDs across files, unknown stages, stale records, future dates and malformed dates.
5. Produce machine-readable JSON summary and reviewable CSV exception register.
6. Keep human review as the final decision point; the pipeline does not delete or edit source records.

## Acceptance criteria
- Invalid source schemas fail with a useful error.
- Duplicate application IDs across multiple feeds are reported.
- Stale-age calculations use an explicit as-of date for reproducibility.
- Results contain no actual customer information.
- Automated unit tests cover normal, duplicate and malformed-date cases.

## Production considerations
Authentication, authorization, PII minimization, audit retention, orchestration, source ownership, schema versioning and monitoring are required before deployment.
