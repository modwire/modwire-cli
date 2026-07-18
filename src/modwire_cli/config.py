from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from modwire_architecture import ArchitectureConfig
from pydantic_yaml import parse_yaml_file_as
from wireup import injectable


@injectable
@dataclass(frozen=True)
class ConfigService:
    def load(self, dot_dir: Path) -> ArchitectureConfig:
        return parse_yaml_file_as(ArchitectureConfig, dot_dir / "architecture.yaml")
