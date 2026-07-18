from __future__ import annotations

from modwire_architecture.architecture.insights.reporters.clusters import ClustersReport
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="50-clusters")
class ClustersInsight(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return context.has_report(ClustersReport) and bool(context.report(ClustersReport).clusters)

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(ClustersReport)
        context.console.print("[blue]Dependency clusters:[/blue]")
        for cluster in report.clusters:
            context.console.print(
                (
                    f"{cluster.name} (pressure: {cluster.pressure_score}, "
                    f"incoming: {cluster.incoming_count}, outgoing: {cluster.outgoing_count})"
                ),
                markup=False,
            )
            for source_id in cluster.top_files:
                context.console.print(f"  - {source_id}", markup=False)
        return context
