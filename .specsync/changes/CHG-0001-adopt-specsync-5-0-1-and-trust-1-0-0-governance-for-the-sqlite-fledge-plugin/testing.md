---
change: CHG-0001-adopt-specsync-5-0-1-and-trust-1-0-0-governance-for-the-sqlite-fledge-plugin
artifact: testing
---

# Testing

Local acceptance requires Bash syntax, all 26 database safety cases, manifest validation, strict SpecSync checks at threshold 0, four integrations, healthy Trust doctor, and a clean diff.

Hosted acceptance requires the new `trust` job and existing integration-test job to pass on Ubuntu while Pages remains independent.
