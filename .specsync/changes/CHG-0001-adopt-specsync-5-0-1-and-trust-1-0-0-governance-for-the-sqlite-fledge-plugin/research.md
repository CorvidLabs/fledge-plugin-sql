---
change: CHG-0001-adopt-specsync-5-0-1-and-trust-1-0-0-governance-for-the-sqlite-fledge-plugin
artifact: research
---

# Research

The hermetic Python harness covers 26 initialization, migration ordering/idempotence/rollback, parameter binding and injection, destructive-operation blocking and override, DML counts, schema, version, and help cases.

SpecSync does not measure the extensionless Bash executable, so coverage is explicitly advisory 0 and the native syntax/database suite is blocking. ShellCheck's pre-existing informational jq-quoting findings are not enforced by current CI and remain isolated.
