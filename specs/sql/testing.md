---
spec: sql.spec.md
---

## Test Plan

### Hermetic integration suite

`python3 test/test.py` acts as the fledge-v1 host and executes 26 cases against
temporary SQLite databases. It covers initialization, ordered and idempotent
migrations, transactional rollback, every query format, safe parameter binding,
SQL-injection-shaped values, destructive-operation and multi-statement guards,
DML change counts, schema JSON, version, help, and invalid parameter input.

### Verification lane

`fledge lanes run verify` runs the deterministic governance check, Bash syntax,
the 26-case database suite, and manifest validation. No external database,
network service, or persistent project data is used.
