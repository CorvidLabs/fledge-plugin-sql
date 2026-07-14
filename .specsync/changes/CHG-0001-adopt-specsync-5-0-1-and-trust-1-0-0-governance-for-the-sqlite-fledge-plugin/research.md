---
change: CHG-0001-adopt-specsync-5-0-1-and-trust-1-0-0-governance-for-the-sqlite-fledge-plugin
artifact: research
---

# Research

The hermetic Python harness covers 26 initialization, migration ordering/idempotence/rollback, parameter binding and injection, destructive-operation blocking and override, DML counts, schema, version, and help cases.

The implementation audit found eleven stable contract areas: initialization,
migrations, query formats, bound parameters, multi-statement rejection,
destructive-DDL approval, DML change counts, schema formats, diagnostics, help
and version, and fledge-v1 host mediation. The canonical spec and requirements
now describe those existing behaviors rather than only the headline commands.

SpecSync 5.0.1 reports 0/0 measurable files and LOC for the governed extensionless
Bash executable. Coverage therefore remains explicitly advisory rather than
misrepresenting 0/0 as 100%; full semantic mapping, syntax, 26 hermetic cases,
manifest validation, and a repository-specific governance check are blocking.
