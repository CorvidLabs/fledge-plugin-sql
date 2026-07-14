## MODIFIED

### SPEC SECTION Purpose
SQLite database management for Fledge projects, including project-local initialization, transactional migrations, guarded queries, parameter binding, result formatting, schema inspection, and version/help output through fledge-v1 host capabilities.

### REQUIREMENT REQ-sql-001
`fledge sql init` SHALL create the selected project database and store its path through the host protocol.

Acceptance Criteria
- The hermetic init case verifies database creation and the host-observed success output.

### REQUIREMENT REQ-sql-002
`fledge sql migrate` SHALL apply unapplied SQL files in filename order, transactionally, and record them idempotently.

Acceptance Criteria
- Migration apply, repeat, failure, rollback-state, and tracking-row cases all pass.

### REQUIREMENT REQ-sql-003
`fledge sql query` SHALL use a selected or stored database and support column, list, CSV, and JSON output, including the documented empty-result forms.

Acceptance Criteria
- The native query cases exercise formatted and JSON results against temporary databases.

### REQUIREMENT REQ-sql-004
Query parameters SHALL validate their names and bind arbitrary values as data without allowing quotes, semicolons, or SQL-looking values to become SQL syntax.

Acceptance Criteria
- Simple, quoted, double-quoted, injection-shaped, malformed, and invalid-name parameter cases pass.

### REQUIREMENT REQ-sql-005
User-supplied multi-statement queries SHALL be rejected, while one trailing semicolon SHALL be accepted.

Acceptance Criteria
- The multi-statement rejection and trailing-semicolon acceptance cases pass.

### REQUIREMENT REQ-sql-006
`DROP`, `ALTER`, and `TRUNCATE` SHALL be rejected unless the caller explicitly passes `--allow-destructive`.

Acceptance Criteria
- All three guarded keywords and the explicit override are verified by the native suite.

### REQUIREMENT REQ-sql-007
`INSERT`, `UPDATE`, and `DELETE` SHALL return a successful JSON object containing the row count reported by `changes()` in the same SQLite session.

Acceptance Criteria
- Insert, update, delete, and explicit change-count cases pass.

### REQUIREMENT REQ-sql-008
`fledge sql schema` SHALL show tables, indexes, and views with SQL definitions in text or JSON form, using a selected or stored database.

Acceptance Criteria
- The schema case verifies the temporary database table in JSON output.

### REQUIREMENT REQ-sql-009
Missing initialization, invalid parameter syntax or names, failed migrations, and SQLite query/schema errors SHALL produce clear diagnostics and non-zero exits; missing or empty migration directories SHALL remain successful no-ops.

Acceptance Criteria
- The hermetic failure and no-op cases assert the documented diagnostics and exit boundaries.

### REQUIREMENT REQ-sql-010
Help SHALL expose every supported command and guarded-query flag, version SHALL read the manifest version, and unknown commands SHALL fail with guidance.

Acceptance Criteria
- Version and help cases verify the manifest version and both guarded-query flags.

### REQUIREMENT REQ-sql-011
All host execution, persistence, prompts, diagnostics, and user output SHALL use the fledge-v1 protocol.

Acceptance Criteria
- The full harness mediates every case as a fledge-v1 host and fails on malformed protocol traffic.

### SPEC SECTION Change Log
| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-05-06 | Initial spec |
| 2 | 2026-07-14 | Document the existing guarded-query, parameter, output-format, schema, version, and help behavior for SpecSync 5.0.1 adoption; runtime behavior is unchanged. |
