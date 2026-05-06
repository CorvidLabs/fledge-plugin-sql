# fledge-plugin-sql

SQLite database management plugin for [fledge](https://github.com/CorvidLabs/fledge).

## Install

```bash
fledge plugins install CorvidLabs/fledge-plugin-sql
```

## Commands

| Command | Description |
|---------|-------------|
| `fledge sql init [--path <db>]` | Create a project SQLite database |
| `fledge sql migrate [--dir <dir>]` | Run SQL migration files |
| `fledge sql query [--path <db>] [--list\|--csv] <sql>` | Execute a query and display results |
| `fledge sql schema [--path <db>]` | Dump the current database schema |

## Prerequisites

- `sqlite3` on PATH (pre-installed on macOS)

## Data Persistence

Database files live in your project directory (default: `data.db`). Reinstalling the plugin (`fledge plugins install`) does **not** affect your database files — they are stored outside the plugin directory.

## Security

- SQL input is shell-escaped via `printf '%q'` before execution to prevent injection.
- Migration filenames are validated and escaped before use.

## Development

```bash
fledge plugins validate .
fledge spec check
```
