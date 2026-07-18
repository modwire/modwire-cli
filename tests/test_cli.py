from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from textwrap import dedent


def test_cli_succeeds_for_a_valid_project(tmp_path: Path) -> None:
    write_project(tmp_path, max_functions_per_file=1)

    result = run_modwire(tmp_path)

    assert result.returncode == 0, result.stderr
    assert "Architecture checks passed." in result.stdout


def test_cli_returns_failure_for_a_shape_violation(tmp_path: Path) -> None:
    write_project(tmp_path, max_functions_per_file=0)

    result = run_modwire(tmp_path)

    assert result.returncode == 1
    assert "Shape violations:" in result.stdout
    assert "max_functions_per_file" in result.stdout


def test_cli_summary_renders_non_empty_layers_beneath_modules(tmp_path: Path) -> None:
    write_layered_project(tmp_path)

    result = run_modwire(tmp_path, "--summary")

    assert result.returncode == 0, result.stderr
    assert "orders" in result.stdout
    for layer in ("wiring", "adapters", "use_cases", "ports", "domain"):
        assert layer in result.stdout
    assert "bootstrap.py" not in result.stdout
    assert "repository.py" not in result.stdout


def test_cli_keeps_detailed_map_by_default(tmp_path: Path) -> None:
    write_layered_project(tmp_path)

    result = run_modwire(tmp_path)

    assert result.returncode == 0, result.stderr
    assert "bootstrap.py" in result.stdout
    assert "repository.py" in result.stdout


def run_modwire(project_root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    executable = Path(sys.executable).with_name("modwire")
    return subprocess.run(
        [str(executable), "--language", "python", *arguments],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )


def write_project(project_root: Path, *, max_functions_per_file: int) -> None:
    dot_dir = project_root / ".modwire"
    source_dir = project_root / "src"
    dot_dir.mkdir()
    source_dir.mkdir()
    (source_dir / "example.py").write_text("def example() -> None:\n    pass\n")
    (dot_dir / "architecture.yaml").write_text(
        dedent(
            f"""\
            boundaries:
              tags:
                - name: package
                  match: src
              flow:
                module_tag: package
                analyzers:
                  - module-boundaries
            shape:
              max_functions_per_file: {max_functions_per_file}
            """
        )
    )


def write_layered_project(project_root: Path) -> None:
    dot_dir = project_root / ".modwire"
    source_dir = project_root / "src" / "orders"
    dot_dir.mkdir()
    for layer, filename in (
        ("wiring", "bootstrap.py"),
        ("adapters", "repository.py"),
        ("use_cases", "place_order.py"),
        ("ports", "order_repository.py"),
        ("domain", "order.py"),
    ):
        layer_dir = source_dir / layer
        layer_dir.mkdir(parents=True)
        (layer_dir / filename).write_text("pass\n")
    (dot_dir / "architecture.yaml").write_text(
        dedent(
            """\
            boundaries:
              tags:
                - name: module
                  match: src/*
                - name: wiring
                  match: src/*/wiring
                - name: adapters
                  match: src/*/adapters
                - name: use_cases
                  match: src/*/use_cases
                - name: ports
                  match: src/*/ports
                - name: domain
                  match: src/*/domain
              flow:
                module_tag: module
                layers: [wiring, adapters, use_cases, ports, domain]
            """
        )
    )
