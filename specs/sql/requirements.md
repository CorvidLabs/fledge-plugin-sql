---
spec: sql.spec.md
---

## User Stories

- As a developer, I want to create a project-local SQLite database with a single command
- As a developer, I want to run SQL migration files in order and track which have been applied
- As a developer, I want to run ad-hoc queries against my project database
- As an AI agent, I want to manage structured data storage without manual setup

## Acceptance Criteria

### REQ-sql-001

`fledge sql init` creates the selected project database and stores its path through the host protocol.

### REQ-sql-002

`fledge sql migrate` applies unapplied SQL files in filename order, transactionally, and records them idempotently.

### REQ-sql-003

`fledge sql query` executes SQL against the initialized database and returns formatted results.

### REQ-sql-004

`fledge sql schema` shows user tables, indexes, and views for the initialized database.

### REQ-sql-005

All commands use the fledge-v1 protocol for input, output, persistence, and host execution.

## Constraints

- Must work without any dependencies beyond sqlite3
- Shell script implementation (no compile step)

## Out of Scope

- GUI or TUI interfaces
- Multi-database support
- Database replication or backup
