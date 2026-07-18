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


def run_modwire(project_root: Path) -> subprocess.CompletedProcess[str]:
    executable = Path(sys.executable).with_name("modwire")
    return subprocess.run(
        [str(executable), "--language", "python"],
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
