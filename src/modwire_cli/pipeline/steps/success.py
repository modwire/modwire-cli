from __future__ import annotations

from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="100-success")
class Success(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return not context.failed

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        context.console.print("[green]Architecture checks passed.[/green]")
        return context
