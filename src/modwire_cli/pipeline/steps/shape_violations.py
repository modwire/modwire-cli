from __future__ import annotations

from modwire_architecture.architecture.shape.collector import ShapeReport
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="40-shape-violations")
class ShapeViolations(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return bool(context.report(ShapeReport).violations)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(ShapeReport)
        context.console.print("[red]Shape violations:[/red]")
        for violation in report.violations:
            symbol = f" {violation.symbol_kind} {violation.symbol_name}" if violation.symbol_kind else ""
            context.console.print(
                (
                    f"  - [{violation.rule_name}] {violation.source_id}{symbol}: "
                    f"{violation.actual} exceeds {violation.limit}"
                ),
                markup=False,
            )
        return context.fail()
