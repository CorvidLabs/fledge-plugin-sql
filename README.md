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

- SQL input is shell-escaped via `printf '%q'` before execution to prevent injection.
- Migration filenames are validated and escaped before use.
- The database file is created in the project-local `.fledge/` directory.

## Prerequisites

- `sqlite3` on PATH (pre-installed on macOS and most Linux distributions)

## Development

```bash
fledge plugins validate .
fledge spec check
```

## License

MIT
