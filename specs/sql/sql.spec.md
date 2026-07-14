---
module: sql
version: 3
status: active
files:
  - bin/fledge-sql

db_tables: []
depends_on: []
---

# Sql

## Purpose

SQLite database management for Fledge projects, including project-local initialization, transactional migrations, guarded queries, parameter binding, result formatting, schema inspection, and version/help output through fledge-v1 host capabilities.

## Public API

### Commands

| Command | Args | Description |
|---------|------|-------------|
| `init` | `[--path <db-path>]` | Prompt with `.fledge/data.db` when no path is supplied, create parent directories and the database if absent, and store the absolute path. Existing databases are retained and stored. |
| `migrate` | `[--dir <migrations-dir>]` | Run previously unapplied `*.sql` files from `migrations/` (or the selected directory) in filename order and track them in `_migrations`. A missing/empty directory is a successful no-op. |
| `query` | `[--path <db>] [--json\|--csv\|--list] [--allow-destructive] [--param name=value]... <sql>` | Execute one SQL statement against the selected or stored database. Default output is header/column format; empty JSON results are `[]`, while other empty results are `(no results)`. |
| `schema` | `[--path <db>] [--json]` | Return tables, indexes, and views with non-null SQL from `sqlite_master`, ordered by name. |
| `version` | `--version`, `-V` | Read the plugin version from `plugin.toml`. |
| `help` | `--help`, `-h` | Print command and guarded-query usage. Unknown commands report an error and exit non-zero. |

### Query safety and results

- More than one user-supplied statement is rejected; one trailing semicolon is accepted.
- `DROP`, `ALTER`, and `TRUNCATE` are rejected unless `--allow-destructive` is present.
- Parameter names accept an optional `@` or `:` prefix and otherwise must match
  `[A-Za-z_][A-Za-z0-9_]*`. Values are encoded as hexadecimal SQLite parameters,
  so quotes and SQL-looking content remain values.
- `INSERT`, `UPDATE`, and `DELETE` return `{"ok":true,"changes":N}` using
  `changes()` from the same SQLite session.

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

1. The plugin never creates a database without a supplied path or a completed host prompt.
2. Migrations are idempotent — re-running `migrate` skips already-applied files.
3. The `_migrations` table is created automatically on first `migrate` run.
4. Migration files are sorted by filename (lexicographic) and applied in order.
5. Each migration runs inside a transaction — if it fails, none of that file's changes persist.
6. The stored DB path is project-scoped via the fledge-v1 `store` capability.
7. `query` and `schema` fail with a clear error if no database has been initialized.
8. All `sqlite3` invocations go through the fledge-v1 `exec` message, never direct host execution.
9. User-supplied multi-statement queries and unapproved destructive DDL are rejected before host execution.
10. Bound parameter names are validated and their values cannot become SQL syntax.
11. DML change counts come from the same SQLite session as the modifying statement.

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
| `Migration failed` | SQL error in a migration file | Roll back that file's transaction, report the filename and SQLite diagnostic, and exit non-zero. |
| `Database already exists` | `init` when DB file exists | Retain the file, store its path, and report that it already exists. |
| `No migrations directory` | `migrate` when the selected directory does not exist | Report the missing directory and exit successfully. |
| `Unsafe query` | The user supplies multiple statements or guarded destructive DDL without the override | Reject before sending an execution request. |
| `Invalid parameter` | `--param` lacks `name=value` or uses an invalid name | Report the invalid binding and exit non-zero. |
| `Query or schema failure` | SQLite returns a non-zero status | Surface the SQLite diagnostic and exit non-zero. |

## Dependencies

- `sqlite3` CLI (external, must be on PATH)
- fledge-v1 protocol (exec, store, load capabilities)

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-05-06 | Initial spec |
| 2 | 2026-07-14 | Document the existing guarded-query, parameter, output-format, schema, version, and help behavior for SpecSync 5.0.1 adoption; runtime behavior is unchanged. |
| 2026-07-14 | CHG-0001-adopt-specsync-5-0-1-and-trust-1-0-0-governance-for-the-sqlite-fledge-plugin: Adopt SpecSync 5.0.1 and Trust 1.0.0 governance for the SQLite Fledge plugin |
