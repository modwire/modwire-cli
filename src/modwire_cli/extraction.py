from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from modwire_extraction import ModwireExtraction, QueryableCodeMap
from wireup import injectable


@injectable
@dataclass(frozen=True)
class ExtractionService:
    def load(self, architecture_root: Path, language: str) -> QueryableCodeMap:
        return ModwireExtraction(architecture_root).generate_queryable_map(language)
