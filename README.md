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
| `fledge sql query <sql>` | Execute a query and display results |
| `fledge sql schema` | Dump the current database schema |

## Prerequisites

- `sqlite3` on PATH (pre-installed on macOS)

## Development

```bash
fledge plugins validate .
fledge spec check
```
