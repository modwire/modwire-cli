from __future__ import annotations

from modwire_architecture.architecture.insights.reporters.callables import CallablesReport
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="80-callables")
class CallablesInsight(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return context.has_report(CallablesReport) and bool(context.report(CallablesReport).entries)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(CallablesReport)
        context.console.print("[blue]Callable graph:[/blue]")
        for entry in report.entries:
            context.console.print(entry.source_callable, markup=False)
            for call in entry.calls:
                context.console.print(f"  calls: {call}", markup=False)
            for caller in entry.callers:
                context.console.print(f"  called by: {caller}", markup=False)
        return context
