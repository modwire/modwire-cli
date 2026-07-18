from __future__ import annotations

from modwire_architecture.architecture.insights.reporters.coherence import CoherenceReport
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="70-coherence")
class CoherenceInsight(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        if not context.has_report(CoherenceReport):
            return False
        report = context.report(CoherenceReport)
        return bool(report.roots or report.leaves or report.isolated or report.external_dependencies)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(CoherenceReport)
        context.console.print("[blue]Dependency coherence:[/blue]")
        self._print_section(context, "Roots", report.roots)
        self._print_section(context, "Leaves", report.leaves)
        self._print_section(context, "Isolated", report.isolated)
        self._print_section(context, "External dependencies", report.external_dependencies)
        return context

    def _print_section(
        self,
        context: ReportPipelineContext,
        title: str,
        entries: tuple[str, ...],
    ) -> None:
        if not entries:
            return
        context.console.print(title)
        for entry in entries:
            context.console.print(f"  - {entry}", markup=False)
