#!/usr/bin/env python3
"""Validate repository-specific SpecSync policy and complete SQL requirements."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MEANINGFUL_PATHS = [
    "bin/",
    "test/",
    "docs/",
    "plugin.toml",
    "fledge.toml",
    ".trust.toml",
    ".augur.toml",
    ".attest.json",
    ".github/",
    ".specsync/sdd.json",
    ".specsync/config.toml",
    ".specsync/version",
    ".claude/",
    ".cursor/",
    ".codex/",
    ".gemini/",
]
REQUIREMENT_IDS = [f"REQ-sql-{number:03d}" for number in range(1, 12)]
SPEC_BEHAVIORS = [
    "--allow-destructive",
    "--param name=value",
    "multi-statement",
    "changes()",
    "version",
    "Unknown commands",
]


def main() -> None:
    """Fail when the rollout policy or canonical contract becomes incomplete."""
    policy = json.loads((ROOT / ".specsync/sdd.json").read_text(encoding="utf-8"))
    assert policy["meaningful_paths"] == EXPECTED_MEANINGFUL_PATHS
    assert policy["verification_commands"] == ["fledge lanes run verify"]

    requirements = (ROOT / "specs/sql/requirements.md").read_text(encoding="utf-8")
    for requirement_id in REQUIREMENT_IDS:
        assert requirements.count(requirement_id) == 1, f"missing or duplicate {requirement_id}"

    canonical_spec = (ROOT / "specs/sql/sql.spec.md").read_text(encoding="utf-8").lower()
    for behavior in SPEC_BEHAVIORS:
        assert behavior.lower() in canonical_spec, f"canonical spec omits {behavior}"

    print("governance policy and REQ-sql-001..REQ-sql-011 validated")


if __name__ == "__main__":
    main()
