# fledge-plugin-sql

SQLite database management plugin for [fledge](https://github.com/CorvidLabs/fledge). Init databases, run migrations, query with multiple output formats.

## Install

```bash
fledge plugins install CorvidLabs/fledge-plugin-sql
```

## Commands

### `fledge sql init [--path <db>]`

Create a project SQLite database. Defaults to `.fledge/fledge.db`. Safe to run multiple times (idempotent).

```
$ fledge sql init
Created database: .fledge/fledge.db
```

### `fledge sql query <sql> [--path <db>] [--json | --csv | --list]`

Execute a SQL statement and display results. Defaults to table output.

```
$ fledge sql query "SELECT name, role FROM agents" --json
[{"name":"CorvidAgent","role":"lead"},{"name":"Magpie","role":"scout"}]

$ fledge sql query "SELECT * FROM agents" --csv
name,role
CorvidAgent,lead
Magpie,scout

$ fledge sql query "INSERT INTO agents VALUES ('Rook', 'security')"
OK
```

### `fledge sql schema [--path <db>] [--json]`

Dump the current database schema.

```
$ fledge sql schema
CREATE TABLE agents (name TEXT, role TEXT);
CREATE TABLE memories (key TEXT PRIMARY KEY, value TEXT);

$ fledge sql schema --json
[{"type":"table","name":"agents","sql":"CREATE TABLE agents (name TEXT, role TEXT)"}]
```

### `fledge sql migrate [--dir <dir>] [--path <db>]`

Run numbered SQL migration files from `migrations/` (or a custom directory). Tracks applied migrations so each file runs exactly once.

```
$ ls migrations/
001_create_agents.sql  002_add_timestamps.sql

$ fledge sql migrate
Applied: 001_create_agents.sql
Applied: 002_add_timestamps.sql

$ fledge sql migrate
No new migrations.
```

## Data Persistence

Database files live in your project directory (default: `.fledge/fledge.db`). Reinstalling the plugin does **not** affect your database files — they are stored outside the plugin directory.

## Security

This plugin shells out to the `sqlite3` CLI. The SQL string you pass is shell-escaped (via `printf '%q'`) before being piped to `sqlite3`, which prevents *shell* injection — your SQL won't be split into multiple commands or interpreted by the shell.

**It does not prevent SQL injection.** SQL is passed verbatim to sqlite3. If you compose SQL with untrusted values via shell interpolation, you are responsible for escaping them — for example, **do not** write `fledge sql query "SELECT * FROM t WHERE name = '$user_input'"`. Either validate `$user_input` against an allowlist before substituting, or split the query into a parameterized form using a SQL client that supports bind parameters.

Migration filenames are SQL-escaped before being inserted into the `_migrations` tracking table. Each migration runs inside a `BEGIN;…COMMIT;` transaction with `sqlite3 -bail`, so a partial failure rolls back cleanly.

The database file is created in the project-local `.fledge/` directory by default.

## Prerequisites

- `sqlite3` on PATH (pre-installed on macOS and most Linux distributions)

## Development

```bash
fledge plugins validate .
fledge spec check
```

## License

MIT
