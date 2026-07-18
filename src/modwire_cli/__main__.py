from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from rich.console import Console
from wireup import create_sync_container, instance

import modwire_cli

from .facade import FitnessFacade


def main() -> int:
    return run(sys.argv[1:])


def run(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dot-dir", type=Path, default=Path(".modwire"))
    parser.add_argument("--architecture-root", type=Path, default=Path("."))
    parser.add_argument("--language", required=True)
    arguments = parser.parse_args(argv)

    container = create_sync_container(
        injectables=[modwire_cli, instance(Console(), as_type=Console)]
    )
    try:
        facade = container.get(FitnessFacade)
        return facade.reports(
            dot_dir=arguments.dot_dir,
            architecture_root=arguments.architecture_root,
            language=arguments.language,
        )
    finally:
        container.close()
