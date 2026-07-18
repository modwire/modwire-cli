from __future__ import annotations

from modwire_architecture.architecture.boundaries.collector import FlowReport
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="30-flow-violations")
class FlowViolations(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return bool(context.report(FlowReport).violations)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(FlowReport)
        context.console.print("[red]Flow violations:[/red]")
        for violation in report.violations:
            context.console.print(
                f"  - [{violation.rule_name}] {violation.message}",
                markup=False,
            )
            context.console.print(f"    {' -> '.join(violation.path)}", markup=False)
        return context.fail()
