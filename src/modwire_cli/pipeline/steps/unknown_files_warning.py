from __future__ import annotations

from modwire_architecture.architecture.map.collector import MapReport
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="20-unknown-files")
class UnknownFilesWarning(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return bool(context.report(MapReport).unknown_files)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(MapReport)
        context.console.print("[yellow]Warning:[/yellow] Files not included in the architecture map:")
        for source_id in report.unknown_files:
            context.console.print(f"  - {source_id}", markup=False)
        return context
