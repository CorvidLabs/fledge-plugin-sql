---
change: CHG-0001-adopt-specsync-5-0-1-and-trust-1-0-0-governance-for-the-sqlite-fledge-plugin
artifact: context
---

# Context

The SQLite plugin manages project-local initialization, transactional migrations, guarded ad-hoc queries, and schema inspection through fledge-v1. The rollout adopts its active contract without weakening persistence or destructive-query safety.
