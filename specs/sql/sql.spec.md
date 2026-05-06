---
module: sql
version: 1
status: active
files:
  - bin/fledge-sql

db_tables: []
depends_on: []
---

# Sql

## Purpose

SQLite database management for fledge projects. Provides project-local database initialization, migration tracking, ad-hoc queries, and schema inspection. Wraps the `sqlite3` CLI via the fledge-v1 protocol's `exec` capability.

## Public API

### Commands

| Command | Args | Description |
|---------|------|-------------|
| `init` | `[--path <db-path>]` | Create a SQLite database. Default: `.fledge/data.db`. Stores path via `store`. |
| `migrate` | `[--dir <migrations-dir>]` | Run `*.sql` files from `migrations/` in filename order. Tracks in `_migrations` table. |
| `query` | `<sql>` | Execute SQL, display results as formatted table. |
| `schema` | | Dump schema via `sqlite_master`. |

### Protocol Messages Used

| Message Type | Direction | Purpose |
|-------------|-----------|---------|
| `init` | inbound | Receive project context and args |
| `exec` | outbound | Run `sqlite3` commands |
| `store` | outbound | Persist DB path |
| `load` | outbound | Retrieve stored DB path |
| `output` | outbound | Display results to user |
| `log` | outbound | Diagnostic messages |
| `prompt` | outbound | Ask user for DB path if not specified |

## Invariants

1. The plugin never creates a database without user confirmation (either `--path` flag or interactive prompt).
2. Migrations are idempotent — re-running `migrate` skips already-applied files.
3. The `_migrations` table is created automatically on first `migrate` run.
4. Migration files are sorted by filename (lexicographic) and applied in order.
5. Each migration runs inside a transaction — if it fails, none of that file's changes persist.
6. The stored DB path is project-scoped via the fledge-v1 `store` capability.
7. `query` and `schema` fail with a clear error if no database has been initialized.
8. All `sqlite3` invocations go through the fledge-v1 `exec` message, never direct shell execution.

## Behavioral Examples

```
$ fledge sql init
  Created database at .fledge/data.db

$ fledge sql init --path myapp.db
  Created database at myapp.db

$ fledge sql migrate
  Applied 3 migrations:
    001_create_users.sql
    002_create_posts.sql
    003_add_indexes.sql

$ fledge sql migrate
  All migrations already applied.

$ fledge sql query "SELECT * FROM users LIMIT 5"
  id  | name    | email
  1   | alice   | alice@example.com
  2   | bob     | bob@example.com

$ fledge sql schema
  CREATE TABLE _migrations (id INTEGER PRIMARY KEY, filename TEXT UNIQUE, applied_at TEXT);
  CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE);
```

## Error Cases

| Error | When | Behavior |
|-------|------|----------|
| `sqlite3 not found` | `sqlite3` not on PATH | Log error, exit 1 |
| `No database initialized` | `query`/`schema`/`migrate` before `init` | Log error with hint to run `fledge sql init` |
| `Migration failed` | SQL error in a migration file | Roll back that file's transaction, log error with filename and line, exit 1 |
| `Database already exists` | `init` when DB file exists | Log warning, skip creation |
| `No migrations directory` | `migrate` when `migrations/` doesn't exist | Log info, exit 0 |

## Dependencies

- `sqlite3` CLI (external, must be on PATH)
- fledge-v1 protocol (exec, store, load capabilities)

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-05-06 | Initial spec |
