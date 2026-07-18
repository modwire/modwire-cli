from __future__ import annotations

from modwire_architecture.architecture.insights.reporters.exports import ExportsReport
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="90-unused-exports")
class UnusedExportsInsight(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return context.has_report(ExportsReport) and bool(context.report(ExportsReport).unused_exports)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(ExportsReport)
        context.console.print("[blue]Unused exports:[/blue]")
        for export in report.unused_exports:
            context.console.print(
                (
                    f"  - {export.source_id}: {export.kind} {export.name} "
                    f"({export.crossing_type}; {export.reason})"
                ),
                markup=False,
            )
        return context
