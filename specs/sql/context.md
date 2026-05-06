---
spec: sql.spec.md
---

## Context

Extracted from corvid-agent's SQLite database management. Provides a standalone, reusable database layer that any fledge project (or agent) can use for structured local storage.

## Related Modules

- fledge-plugin-memory (uses sql plugin for ephemeral tier storage)

## Design Decisions

- Shell script wrapping `sqlite3` CLI rather than a compiled binary — keeps the plugin zero-dependency and immediately editable
- Migrations tracked in a `_migrations` table rather than a separate state file — the database itself is the source of truth
- Uses fledge-v1 `store` capability for DB path rather than a config file — integrates with fledge's plugin storage system
