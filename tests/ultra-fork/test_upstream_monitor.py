import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from urllib.error import HTTPError, URLError


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts/check-upstream.py"


def load_monitor():
    spec = importlib.util.spec_from_file_location("check_upstream", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load upstream monitor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload, headers=None):
        self.payload = json.dumps(payload).encode("utf-8")
        self.headers = headers or {}

    def read(self):
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


class FakeOpener:
    def __init__(self, routes=None, error=None):
        self.routes = routes or {}
        self.error = error
        self.calls = []

    def open(self, request, timeout):
        self.calls.append(request.full_url)
        if self.error is not None:
            raise self.error
        path = request.full_url.removeprefix("https://api.github.com")
        if path not in self.routes:
            raise AssertionError(f"unexpected network route: {path}")
        return FakeResponse(self.routes[path])


def valid_routes():
    return {
        "/repos/obra/superpowers/releases/latest": {
            "tag_name": "v6.1.1",
            "html_url": "https://github.com/obra/superpowers/releases/tag/v6.1.1",
        },
        "/repos/obra/superpowers/commits/v6.1.1": {"sha": "release-sha"},
        "/repos/obra/superpowers/commits/dev": {"sha": "dev-sha"},
        "/repos/prime-radiant-inc/superpowers-evals/commits/main": {
            "sha": "evals-sha"
        },
        "/repos/obra/superpowers/issues?state=open&per_page=100&sort=updated&direction=desc": [
            {
                "number": 19,
                "title": "Unrelated documentation typo",
                "body": "No scheduler content",
                "state": "open",
                "html_url": "https://example.test/19",
                "updated_at": "2026-07-14T00:00:00Z",
                "labels": [],
            },
            {
                "number": 8,
                "title": "Codex wait_agent behavior",
                "body": "A wait timeout should not fail.",
                "state": "open",
                "html_url": "https://example.test/8",
                "updated_at": "2026-07-15T01:00:00Z",
                "labels": [{"name": "Codex"}, {"name": "Runtime"}],
                "pull_request": {"url": "https://api.example.test/pulls/8"},
            },
            {
                "number": 3,
                "title": "SDD context reuse",
                "body": None,
                "state": "open",
                "html_url": "https://example.test/3",
                "updated_at": "2026-07-15T02:00:00Z",
                "labels": [{"name": "enhancement"}],
            },
        ],
        "/repos/obra/superpowers/compare/release-sha...dev-sha": {
            "files": [
                {
                    "filename": "docs/notes.md",
                    "status": "modified",
                },
                {
                    "filename": "skills/subagent-driven-development/SKILL.md",
                    "status": "modified",
                },
                {
                    "filename": "scripts/package-codex-plugin.sh",
                    "status": "renamed",
                    "previous_filename": "scripts/package-plugin.sh",
                },
                {
                    "filename": "skills/dispatching-parallel-agents/SKILL.md",
                    "status": "modified",
                },
            ]
        },
    }


class UpstreamMonitorTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT_PATH.exists(), "upstream monitor script is required")
        self.monitor = load_monitor()

    def test_collects_and_normalizes_all_semantic_fields(self):
        opener = FakeOpener(valid_routes())
        client = self.monitor.GitHubClient(token="test-token", opener=opener)

        state = self.monitor.collect_state(client)

        self.assertEqual(
            state["upstream"]["release"],
            {
                "tag": "v6.1.1",
                "sha": "release-sha",
                "url": "https://github.com/obra/superpowers/releases/tag/v6.1.1",
            },
        )
        self.assertEqual(state["upstream"]["dev_sha"], "dev-sha")
        self.assertEqual(state["evals"]["sha"], "evals-sha")
        self.assertEqual(
            [item["number"] for item in state["relevant_items"]],
            [3, 8],
        )
        self.assertEqual(state["relevant_items"][1]["kind"], "pull_request")
        self.assertEqual(state["relevant_items"][1]["labels"], ["codex", "runtime"])
        self.assertEqual(
            [change["filename"] for change in state["high_value_changes"]],
            [
                "scripts/package-codex-plugin.sh",
                "skills/dispatching-parallel-agents/SKILL.md",
                "skills/subagent-driven-development/SKILL.md",
            ],
        )
        self.assertTrue(all(url.startswith("https://api.github.com/") for url in opener.calls))

    def test_write_if_changed_preserves_semantically_identical_file(self):
        state = {"schema_version": 1, "upstream": {"dev_sha": "same"}}
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "state.json"
            original = '{"upstream":{"dev_sha":"same"},"schema_version":1}\n'
            output.write_text(original, encoding="utf-8")

            changed = self.monitor.write_if_changed(output, state)

            self.assertFalse(changed)
            self.assertEqual(output.read_text(encoding="utf-8"), original)

            changed = self.monitor.write_if_changed(
                output,
                {"schema_version": 1, "upstream": {"dev_sha": "new"}},
            )
            self.assertTrue(changed)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["upstream"]["dev_sha"], "new")

    def test_rate_limit_network_and_schema_errors_exit_nonzero(self):
        rate_limit = HTTPError(
            "https://api.github.com/test",
            403,
            "rate limited",
            {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "123"},
            None,
        )
        failures = (
            (FakeOpener(error=rate_limit), "rate limit"),
            (FakeOpener(error=URLError("offline")), "network error"),
            (
                FakeOpener(
                    routes={
                        "/repos/obra/superpowers/releases/latest": {
                            "html_url": "https://example.test/missing-tag"
                        }
                    }
                ),
                "schema error",
            ),
        )

        for opener, expected in failures:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as temp_dir:
                stderr = io.StringIO()
                client = self.monitor.GitHubClient(opener=opener)
                with redirect_stderr(stderr):
                    exit_code = self.monitor.run(
                        Path(temp_dir) / "state.json",
                        client=client,
                    )
                self.assertNotEqual(exit_code, 0)
                self.assertIn(expected, stderr.getvalue().lower())


if __name__ == "__main__":
    unittest.main()
