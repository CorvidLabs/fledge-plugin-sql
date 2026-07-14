---
change: CHG-0001-adopt-specsync-5-0-1-and-trust-1-0-0-governance-for-the-sqlite-fledge-plugin
artifact: testing
---

# Testing

Local acceptance requires the repository-specific governance check, Bash syntax,
all 26 hermetic database cases, manifest validation, strict forced SpecSync checks
at the explicit extensionless-file threshold, all four integrations, healthy
Trust doctor, full Trust verification, and a clean diff.

The native suite covers every REQ-sql contract area without a live service or
network dependency. Lifecycle evidence must be produced by supported SpecSync
commands after this lane passes, not by pre-completing approval or hosted-CI tasks.

Requirement evidence maps to the passing native cases as follows:

- `REQ-sql-001`: initialization creates the temporary database through the host.
- `REQ-sql-002`: migration apply, idempotence, failure rollback, and tracking-row cases.
- `REQ-sql-003`: query output and JSON-result cases against temporary databases.
- `REQ-sql-004`: simple, quoted, double-quoted, injection-shaped, malformed, and invalid-name parameters.
- `REQ-sql-005`: multi-statement rejection and trailing-semicolon acceptance.
- `REQ-sql-006`: DROP, ALTER, TRUNCATE, and explicit destructive override cases.
- `REQ-sql-007`: insert, update, delete, and same-session change-count cases.
- `REQ-sql-008`: schema JSON includes the expected temporary table definition.
- `REQ-sql-009`: migration, parameter, and guarded-query error/no-op boundaries.
- `REQ-sql-010`: manifest-backed version and complete guarded-query help cases.
- `REQ-sql-011`: the harness mediates all 26 cases as a fledge-v1 host.

Hosted acceptance requires the exact-head `trust`, existing integration tests,
and other applicable checks to pass on Ubuntu while Pages remains independent.
