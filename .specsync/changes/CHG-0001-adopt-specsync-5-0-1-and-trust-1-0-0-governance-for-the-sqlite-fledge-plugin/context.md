---
change: CHG-0001-adopt-specsync-5-0-1-and-trust-1-0-0-governance-for-the-sqlite-fledge-plugin
artifact: context
---

# Context

The extensionless Bash plugin manages project-local initialization, transactional
migrations, guarded queries, parameter binding, result formatting, schema
inspection, and version/help output through fledge-v1. The original rollout
captured only the four headline database commands and used generic SDD paths.
This migration completes the current contract and repository-specific policy
without changing the executable, existing CI, or Pages publication.
