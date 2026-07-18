from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from modwire_architecture import Modwire
from wireup import injectable

from .config import ConfigService
from .extraction import ExtractionService
from .pipeline.runner import ReportPipelineRunner


@injectable
@dataclass(frozen=True)
class FitnessFacade:
    config_service: ConfigService
    extraction_service: ExtractionService
    pipeline_runner: ReportPipelineRunner

    def reports(
        self,
        dot_dir: Path,
        architecture_root: Path,
        language: str,
    ) -> int:
        config = self.config_service.load(dot_dir)
        code_map = self.extraction_service.load(architecture_root, language)
        reports = Modwire().architecture(config).report(code_map)
        return self.pipeline_runner.run(reports)
