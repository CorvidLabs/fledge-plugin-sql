#!/usr/bin/env python3
"""Integration tests for fledge-plugin-sql.

Spawns the plugin as a subprocess; this test script acts as the fledge
host, dispatching the plugin's exec/store/load/prompt requests against
real $WORK state. SQL behavior (transactional rollback, parameter
binding, injection prevention) is exercised end-to-end against real
sqlite3.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent
BIN = PLUGIN_DIR / "bin" / "fledge-sql"


class PluginRunner:
    def __init__(self, work: Path):
        self.work = work
        self.store: dict[str, str] = {}
        # Persist store across runs by reading/writing files in .fledge.
        self._store_dir = work / ".fledge" / "_test_store"
        self._store_dir.mkdir(parents=True, exist_ok=True)
        for f in self._store_dir.iterdir():
            self.store[f.name] = f.read_text()

    def _persist(self, key: str, value: str) -> None:
        (self._store_dir / key).write_text(value)
        self.store[key] = value

    def run(self, args: list[str]) -> str:
        captured: list[str] = []
        proc = subprocess.Popen(
            [str(BIN)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        assert proc.stdin and proc.stdout
        init = {
            "type": "init",
            "version": "fledge-v1",
            "project": {"root": str(self.work), "name": "t"},
            "plugin": {"dir": str(PLUGIN_DIR), "name": "fledge-plugin-sql"},
            "command": "sql",
            "args": args,
        }
        proc.stdin.write(json.dumps(init) + "\n")
        proc.stdin.flush()

        for line in proc.stdout:
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                captured.append(f"[malformed] {line}")
                continue
            mtype = msg.get("type")
            if mtype == "output":
                captured.append(msg.get("text", ""))
            elif mtype == "log":
                captured.append(f"[{msg.get('level','log')}] {msg.get('message','')}")
            elif mtype == "exec":
                self._handle_exec(msg, proc)
            elif mtype == "load":
                self._handle_load(msg, proc)
            elif mtype == "store":
                self._persist(msg["key"], msg.get("value", ""))
            elif mtype == "prompt":
                self._handle_prompt(msg, proc)
        proc.wait(timeout=10)
        return "\n".join(captured)

    def _handle_exec(self, msg: dict, proc: subprocess.Popen) -> None:
        cmd = msg["command"]
        cwd = msg.get("cwd") or str(self.work)
        result = subprocess.run(
            ["bash", "-c", cmd],
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        resp = {
            "type": "response",
            "id": msg["id"],
            "value": {
                "code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        }
        proc.stdin.write(json.dumps(resp) + "\n")
        proc.stdin.flush()

    def _handle_load(self, msg: dict, proc: subprocess.Popen) -> None:
        val = self.store.get(msg["key"])
        resp = {"type": "response", "id": msg["id"], "value": val}
        proc.stdin.write(json.dumps(resp) + "\n")
        proc.stdin.flush()

    def _handle_prompt(self, msg: dict, proc: subprocess.Popen) -> None:
        resp = {"type": "response", "id": msg["id"], "value": msg.get("default", "")}
        proc.stdin.write(json.dumps(resp) + "\n")
        proc.stdin.flush()


passed = 0
failed = 0


def assert_in(name: str, output: str, needle: str) -> None:
    global passed, failed
    if needle in output:
        print(f"  ok {name}")
        passed += 1
    else:
        print(f"  FAIL {name}")
        print(f"       expected substring: {needle!r}")
        print(f"       output:")
        for line in output.splitlines():
            print(f"         {line}")
        failed += 1


def assert_not_in(name: str, output: str, needle: str) -> None:
    global passed, failed
    if needle not in output:
        print(f"  ok {name}")
        passed += 1
    else:
        print(f"  FAIL {name} (unexpected substring {needle!r})")
        failed += 1


def main() -> int:
    work = Path(tempfile.mkdtemp(prefix="fledge-sql-test."))
    try:
        (work / ".fledge").mkdir()
        (work / "migrations").mkdir()
        runner = PluginRunner(work)

        # 1. init
        out = runner.run(["init", "--path", ".fledge/data.db"])
        assert_in("init creates db", out, "Created database")

        # 2. migrate happy
        (work / "migrations" / "001_init.sql").write_text(
            "CREATE TABLE agents (name TEXT PRIMARY KEY, role TEXT);\n"
            "INSERT INTO agents VALUES ('Rook', 'security');\n"
            "INSERT INTO agents VALUES ('Corvin', 'ci');\n"
        )
        out = runner.run(["migrate"])
        assert_in("migrate applies file", out, "Applied: 001_init.sql")

        # 3. migrate idempotency
        out = runner.run(["migrate"])
        assert_in("migrate idempotent", out, "All migrations already applied")

        # 4. transactional rollback
        bad = work / "migrations" / "002_bad.sql"
        bad.write_text(
            "CREATE TABLE good_table (id INTEGER);\n"
            "INSERT INTO nonexistent_table VALUES (1);\n"
        )
        out = runner.run(["migrate"])
        assert_in("bad migration errors", out, "Migration failed")
        out = runner.run(["query",
                          "SELECT name FROM sqlite_master WHERE name='good_table'"])
        assert_not_in("rollback hides good_table", out, "good_table")
        out = runner.run(["query", "SELECT filename FROM _migrations"])
        assert_not_in("rollback skips _migrations row", out, "002_bad.sql")
        bad.unlink()

        # 5. parameterized query
        out = runner.run(["query",
                          "SELECT role FROM agents WHERE name = @name",
                          "--param", "name=Rook", "--json"])
        assert_in("param simple", out, '"role":"security"')

        # 6. param value with single quote
        out = runner.run(["query", "SELECT @name AS got",
                          "--param", "name=O'Brien", "--json"])
        assert_in("param with single quote", out, "O'Brien")

        # 7. SQL injection blocked through --param
        runner.run(["query",
                    "SELECT * FROM agents WHERE name = @name",
                    "--param", "name=x'; DROP TABLE agents; --", "--json"])
        out = runner.run(["query", "SELECT count(*) AS n FROM agents", "--json"])
        assert_in("SQL injection blocked via --param", out, '"n":2')

        # 7b. destructive DDL blocked by default (DROP)
        out = runner.run(["query", "DROP TABLE agents"])
        assert_in("DROP blocked by default", out, "Destructive operation blocked")

        # 7c. destructive DDL blocked (ALTER)
        out = runner.run(["query", "ALTER TABLE agents ADD COLUMN email TEXT"])
        assert_in("ALTER blocked by default", out, "Destructive operation blocked")

        # 7d. destructive DDL blocked (TRUNCATE, case-insensitive)
        out = runner.run(["query", "truncate table agents"])
        assert_in("TRUNCATE blocked (lowercase)", out, "Destructive operation blocked")

        # 7e. --allow-destructive bypasses DDL guard
        # Use ALTER as it is non-destructive in practice for this test.
        out = runner.run(["query", "ALTER TABLE agents ADD COLUMN email TEXT",
                          "--allow-destructive"])
        assert_not_in("--allow-destructive bypasses guard", out,
                       "Destructive operation blocked")

        # 7f. multi-statement blocked
        out = runner.run(["query",
                          "SELECT 1; DROP TABLE agents"])
        assert_in("multi-statement blocked", out,
                  "Multi-statement queries are not supported for safety")

        # 7g. trailing semicolons are not flagged as multi-statement
        out = runner.run(["query", "SELECT count(*) AS n FROM agents;", "--json"])
        assert_not_in("trailing semicolon OK", out,
                       "Multi-statement queries are not supported")

        # 7h. DML success indicator (INSERT returns changes count)
        out = runner.run(["query",
                          "INSERT INTO agents (name, role) VALUES ('Piper', 'deploy')",
                          "--json"])
        assert_in("DML insert returns ok+changes", out, '"ok":true')
        assert_in("DML insert changes count", out, '"changes":1')

        # 7i. DML success indicator (UPDATE)
        out = runner.run(["query",
                          "UPDATE agents SET role='ops' WHERE name='Piper'",
                          "--json"])
        assert_in("DML update returns ok+changes", out, '"ok":true')

        # 7j. DML success indicator (DELETE)
        out = runner.run(["query",
                          "DELETE FROM agents WHERE name='Piper'",
                          "--json"])
        assert_in("DML delete returns ok+changes", out, '"ok":true')

        # 8. bad --param syntax rejected
        out = runner.run(["query", "SELECT 1", "--param", "not-a-kv-pair"])
        assert_in("bad --param syntax rejected", out, "Bad --param syntax")

        # 9. bad --param name rejected
        out = runner.run(["query", "SELECT 1", "--param", "1bad=value"])
        assert_in("bad --param name rejected", out, "Bad --param name")

        # 10. schema dump
        out = runner.run(["schema", "--json"])
        assert_in("schema lists agents table", out, '"name":"agents"')

        # 11. param value with double quotes (regression)
        out = runner.run(["query", 'SELECT length(@x) AS n',
                          "--param", 'x=has "double" quotes', "--json"])
        assert_in("param with double quotes", out, '"n":19')

        # 12. --version flag
        out = runner.run(["--version"])
        assert_in("--version shows version", out, "fledge-plugin-sql 0.2.0")

        # 13. help text mentions --param and --allow-destructive
        out = runner.run(["help"])
        assert_in("help mentions --param", out, "--param name=value")
        assert_in("help mentions --allow-destructive", out, "--allow-destructive")

    finally:
        shutil.rmtree(work, ignore_errors=True)

    print()
    print(f"tests: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
