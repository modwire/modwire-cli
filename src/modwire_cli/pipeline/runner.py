from __future__ import annotations

from collections.abc import Hashable, Mapping
from dataclasses import dataclass

from modwire_architecture.shared.report.base import ReportNode
from rich.console import Console
from wireup import injectable

from .context import ReportPipelineContext
from .step import ReportPipelineStep


@injectable
@dataclass(frozen=True)
class ReportPipelineRunner:
    steps: Mapping[Hashable, ReportPipelineStep]
    console: Console

    def run(self, reports: tuple[ReportNode, ...], *, summary: bool = False) -> int:
        context = ReportPipelineContext(reports=reports, console=self.console, summary=summary)
        result = self.process(context)
        return int(result.failed)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        for _, step in sorted(
            self.steps.items(),
            key=lambda item: int(str(item[0]).partition("-")[0]),
        ):
            if step.should_process(context):
                context = step.process(context)
        return context
