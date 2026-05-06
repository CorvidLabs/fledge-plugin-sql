---
spec: sql.spec.md
---

## User Stories

- As a developer, I want to create a project-local SQLite database with a single command
- As a developer, I want to run SQL migration files in order and track which have been applied
- As a developer, I want to run ad-hoc queries against my project database
- As an AI agent, I want to manage structured data storage without manual setup

## Acceptance Criteria

- `fledge sql init` creates a database file and stores the path
- `fledge sql migrate` applies unapplied .sql files in order and tracks them
- `fledge sql query` executes SQL and returns formatted results
- `fledge sql schema` shows all tables, indexes, and views
- All commands use fledge-v1 protocol for I/O

## Constraints

- Must work without any dependencies beyond sqlite3
- Shell script implementation (no compile step)

## Out of Scope

- GUI or TUI interfaces
- Multi-database support
- Database replication or backup
