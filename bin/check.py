#!/usr/bin/env python3
"""Run the repository's focused checks as stable, named validation groups.

The individual checkers remain independently runnable for focused debugging.
This entry point is the CI/local contract: it supplies one interpreter, one
working directory, consistent headings, and a stable ordering.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PREBUILD = (
    ("i18n", "bin/check-i18n.py"),
    ("taxonomy", "bin/check-taxonomy.py"),
    ("vendor", "bin/check-vendor.py"),
    ("font-tokens", "bin/check-font-tokens.py"),
    ("navigation", "bin/check-navigation-contract.py"),
    ("runtime-isolation", "bin/check-runtime-isolation.py"),
    ("sidebar-icons", "bin/check-sidebar-icons.py"),
    ("search", "bin/check-search.py"),
    ("actions", "bin/check-actions.py"),
    ("palette", "bin/check-palette.py"),
    ("starter", "bin/check-starter.py"),
    ("reading", "bin/check-reading.py"),
    ("release-assets", "bin/check-release-assets.py"),
    ("download", "bin/check-download.py"),
    ("landing", "bin/check-landing.py"),
    ("book", "bin/check-book.py"),
    ("book-migrations", "bin/check-book-migrations.py"),
    ("shared-scenarios", "bin/check-shared-scenarios.py"),
    ("keyboard", "bin/check-keyboard.py"),
    ("shell", "bin/check-shell.py"),
    ("annotation", "bin/check-annotation.py"),
)

POSTBUILD = (
    ("code-blocks", "bin/check-code-blocks.py"),
    ("content-primitives", "bin/check-content-primitives.py"),
    ("media-primitives", "bin/check-media-primitives.py"),
    ("image-zoom", "bin/check-image-zoom.py"),
    ("gallery", "bin/check-gallery.py"),
    ("components", "bin/check-components.py"),
    ("migration-toolkit", "-m", "unittest", "discover", "-s", "tests/migrations", "-t", "."),
    ("checker-inputs", "tests/test_checker_inputs.py"),
    ("output", "bin/check-output.py", "--public", "tests/site/public"),
    ("namespace", "bin/check-namespace.py", "--public", "tests/site/public"),
    ("params", "bin/check-params.py"),
    ("config-schema", "bin/generate-config-schema.py", "--check"),
    ("site-markup", "bin/check-site-markup.py", "--site", "tests/site"),
    ("agent-indexes", "bin/check-agent-indexes.py"),
    ("backlinks", "bin/check-backlinks.py"),
    ("goldens", "bin/check-goldens.py"),
)

GROUPS = {"prebuild": PREBUILD, "postbuild": POSTBUILD}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--group",
        choices=("prebuild", "postbuild", "all"),
        default="all",
        help="validation group to run (default: all)",
    )
    parser.add_argument("--list", action="store_true", help="list checks without running them")
    return parser.parse_args()


def selected(group: str) -> tuple[tuple[str, ...], ...]:
    if group == "all":
        return (*GROUPS["prebuild"], *GROUPS["postbuild"])
    return GROUPS[group]


def main() -> int:
    args = parse_args()
    checks = selected(args.group)
    if args.list:
        for check in checks:
            print(check[0])
        return 0

    for check in checks:
        name, script, *script_args = check
        command = (
            [sys.executable, script, *script_args]
            if script.startswith("-")
            else [sys.executable, str(ROOT / script), *script_args]
        )
        print(f"\n== {name} ==", flush=True)
        environment = os.environ.copy()
        # Checkers inspect UTF-8 Hugo output. Make their default text mode
        # deterministic on Windows as well as Linux runners.
        environment["PYTHONUTF8"] = "1"
        environment["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(command, cwd=ROOT, env=environment, check=False)
        if result.returncode:
            print(f"\nCHECK FAILED: {name} (exit {result.returncode})", file=sys.stderr)
            return result.returncode
    print(f"\n{args.group} checks passed ({len(checks)} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
