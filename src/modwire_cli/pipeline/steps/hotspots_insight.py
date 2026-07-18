from __future__ import annotations

from modwire_architecture.architecture.insights.reporters.hotspots import HotspotsReport
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="60-hotspots")
class HotspotsInsight(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return context.has_report(HotspotsReport) and bool(context.report(HotspotsReport).hotspots)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(HotspotsReport)
        context.console.print("[blue]Dependency hotspots:[/blue]")
        for hotspot in report.hotspots:
            context.console.print(
                (
                    f"  - {hotspot.source_id} (pressure: {hotspot.pressure_score}, "
                    f"incoming: {hotspot.incoming_count}, outgoing: {hotspot.outgoing_count})"
                ),
                markup=False,
            )
        return context
