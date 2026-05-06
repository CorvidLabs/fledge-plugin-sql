---
spec: sql.spec.md
---

## Test Plan

### Integration Tests

- Pipe fledge-v1 init message to the plugin binary, verify JSON output
- Test `init` creates a database file
- Test `migrate` applies .sql files and records them
- Test `migrate` is idempotent
- Test `query` returns formatted results
- Test `schema` returns table definitions
- Test error cases: missing sqlite3, no DB initialized, bad SQL
