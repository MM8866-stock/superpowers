#!/usr/bin/env python3
"""Track semantic upstream changes without model calls."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, build_opener


API_BASE = "https://api.github.com"
UPSTREAM_REPOSITORY = "obra/superpowers"
EVALS_REPOSITORY = "prime-radiant-inc/superpowers-evals"
RELEVANT_TERMS = (
    "codex",
    "gpt-5.6",
    "gpt 5.6",
    "ultra",
    "sdd",
    "subagent",
    "wait_agent",
    "wait timeout",
)
HIGH_VALUE_PREFIXES = (
    ".claude-plugin/",
    ".codex-plugin/",
    "skills/dispatching-parallel-agents/",
    "skills/subagent-driven-development/",
    "skills/using-superpowers/references/codex-tools.md",
    "tests/codex/",
)
HIGH_VALUE_FILES = (
    "scripts/package-codex-plugin.sh",
    "scripts/sync-to-codex-plugin.sh",
)


class MonitorError(RuntimeError):
    """A clear, operator-actionable monitor failure."""


class GitHubClient:
    def __init__(self, token: str | None = None, opener: Any | None = None):
        self.token = token if token is not None else os.environ.get("GITHUB_TOKEN")
        self.opener = opener if opener is not None else build_opener()

    def get(self, path: str) -> Any:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "superpowers-ultra-upstream-monitor",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(f"{API_BASE}{path}", headers=headers)

        try:
            with self.opener.open(request, timeout=30) as response:
                payload = response.read()
        except HTTPError as error:
            remaining = error.headers.get("X-RateLimit-Remaining")
            if error.code in (403, 429) and remaining == "0":
                reset = error.headers.get("X-RateLimit-Reset", "unknown")
                raise MonitorError(
                    f"GitHub rate limit exceeded (reset {reset})"
                ) from error
            raise MonitorError(
                f"GitHub HTTP error {error.code} for {path}: {error.reason}"
            ) from error
        except URLError as error:
            raise MonitorError(f"GitHub network error for {path}: {error.reason}") from error
        except OSError as error:
            raise MonitorError(f"GitHub network error for {path}: {error}") from error

        try:
            return json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise MonitorError(f"GitHub schema error for {path}: invalid JSON") from error


def require_mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MonitorError(f"GitHub schema error for {context}: expected object")
    return value


def require_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise MonitorError(f"GitHub schema error for {context}: expected list")
    return value


def require_string(mapping: dict[str, Any], field: str, context: str) -> str:
    value = mapping.get(field)
    if not isinstance(value, str) or not value:
        raise MonitorError(
            f"GitHub schema error for {context}: missing non-empty {field}"
        )
    return value


def relevant_item(item: dict[str, Any]) -> bool:
    labels = item.get("labels", [])
    label_names = [
        label.get("name", "")
        for label in labels
        if isinstance(label, dict) and isinstance(label.get("name"), str)
    ]
    text = " ".join(
        part
        for part in (
            item.get("title", ""),
            item.get("body") or "",
            " ".join(label_names),
        )
        if isinstance(part, str)
    ).lower()
    return any(term in text for term in RELEVANT_TERMS)


def normalize_item(raw: Any) -> dict[str, Any]:
    item = require_mapping(raw, "issue/PR")
    number = item.get("number")
    if not isinstance(number, int):
        raise MonitorError("GitHub schema error for issue/PR: missing integer number")
    labels = require_list(item.get("labels", []), f"issue/PR #{number} labels")
    normalized_labels = sorted(
        {
            require_string(
                require_mapping(label, f"issue/PR #{number} label"),
                "name",
                f"issue/PR #{number} label",
            ).lower()
            for label in labels
        }
    )
    return {
        "number": number,
        "kind": "pull_request" if "pull_request" in item else "issue",
        "title": require_string(item, "title", f"issue/PR #{number}"),
        "state": require_string(item, "state", f"issue/PR #{number}"),
        "url": require_string(item, "html_url", f"issue/PR #{number}"),
        "updated_at": require_string(item, "updated_at", f"issue/PR #{number}"),
        "labels": normalized_labels,
    }


def high_value_path(filename: str) -> bool:
    lower = filename.lower()
    return (
        filename in HIGH_VALUE_FILES
        or filename.startswith(HIGH_VALUE_PREFIXES)
        or lower.startswith("docs/releases/")
        or lower.startswith("release-notes")
        or lower.startswith("changelog")
    )


def normalize_change(raw: Any) -> dict[str, str] | None:
    change = require_mapping(raw, "compare file")
    filename = require_string(change, "filename", "compare file")
    if not high_value_path(filename):
        return None
    normalized = {
        "filename": filename,
        "status": require_string(change, "status", f"compare file {filename}"),
    }
    previous = change.get("previous_filename")
    if isinstance(previous, str) and previous:
        normalized["previous_filename"] = previous
    return normalized


def collect_state(client: GitHubClient) -> dict[str, Any]:
    release = require_mapping(
        client.get(f"/repos/{UPSTREAM_REPOSITORY}/releases/latest"),
        "latest release",
    )
    release_tag = require_string(release, "tag_name", "latest release")
    release_url = require_string(release, "html_url", "latest release")
    release_commit = require_mapping(
        client.get(
            f"/repos/{UPSTREAM_REPOSITORY}/commits/{quote(release_tag, safe='')}"
        ),
        "release commit",
    )
    release_sha = require_string(release_commit, "sha", "release commit")

    dev_commit = require_mapping(
        client.get(f"/repos/{UPSTREAM_REPOSITORY}/commits/dev"),
        "upstream dev commit",
    )
    dev_sha = require_string(dev_commit, "sha", "upstream dev commit")

    evals_commit = require_mapping(
        client.get(f"/repos/{EVALS_REPOSITORY}/commits/main"),
        "evals main commit",
    )
    evals_sha = require_string(evals_commit, "sha", "evals main commit")

    raw_items = require_list(
        client.get(
            f"/repos/{UPSTREAM_REPOSITORY}/issues"
            "?state=open&per_page=100&sort=updated&direction=desc"
        ),
        "open issues/PRs",
    )
    items = sorted(
        (
            normalize_item(item)
            for item in raw_items
            if isinstance(item, dict) and relevant_item(item)
        ),
        key=lambda item: item["number"],
    )

    comparison = require_mapping(
        client.get(
            f"/repos/{UPSTREAM_REPOSITORY}/compare/"
            f"{quote(release_sha, safe='')}...{quote(dev_sha, safe='')}"
        ),
        "release-to-dev comparison",
    )
    raw_files = require_list(comparison.get("files"), "release-to-dev files")
    changes = sorted(
        (
            normalized
            for raw in raw_files
            if (normalized := normalize_change(raw)) is not None
        ),
        key=lambda change: change["filename"],
    )

    return {
        "schema_version": 1,
        "upstream": {
            "repository": UPSTREAM_REPOSITORY,
            "release": {
                "tag": release_tag,
                "sha": release_sha,
                "url": release_url,
            },
            "dev_sha": dev_sha,
        },
        "evals": {
            "repository": EVALS_REPOSITORY,
            "default_branch": "main",
            "sha": evals_sha,
        },
        "relevant_items": items,
        "high_value_changes": changes,
    }


def write_if_changed(output: Path, state: dict[str, Any]) -> bool:
    if output.exists():
        try:
            existing = json.loads(output.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise MonitorError(f"existing state is unreadable: {output}") from error
        if existing == state:
            return False

    output.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=output.parent,
            prefix=f".{output.name}.",
            delete=False,
        ) as temporary:
            temporary.write(rendered)
            temporary_name = temporary.name
        os.replace(temporary_name, output)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)
    return True


def run(output: Path, client: GitHubClient | None = None) -> int:
    try:
        state = collect_state(client or GitHubClient())
        changed = write_if_changed(output, state)
    except MonitorError as error:
        print(f"upstream monitor error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"upstream monitor error: filesystem error: {error}", file=sys.stderr)
        return 2

    print(f"{'updated' if changed else 'unchanged'} {output}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tracking/upstream-state.json"),
        help="canonical state file to update",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
