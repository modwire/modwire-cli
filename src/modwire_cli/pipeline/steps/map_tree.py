from __future__ import annotations

from modwire_architecture.architecture.map.collector import ArchitectureGroup, MapReport
from rich.tree import Tree
from wireup import injectable

from ..context import ReportPipelineContext
from ..step import ReportPipelineStep


@injectable(as_type=ReportPipelineStep, qualifier="10-map")
class MapTree(ReportPipelineStep):
    def should_process(self, context: ReportPipelineContext) -> bool:
        return True

    def process(self, context: ReportPipelineContext) -> ReportPipelineContext:
        report = context.report(MapReport)
        tree = Tree("Architecture Map")
        if context.summary:
            self._add_summary(tree, report.modules, report.layers)
        else:
            self._add_groups(tree, "Modules", report.modules)
            self._add_groups(tree, "Layers", report.layers)
        context.console.print(tree)
        return context

    def _add_summary(
        self,
        tree: Tree,
        modules: tuple[ArchitectureGroup, ...],
        layers: tuple[ArchitectureGroup, ...],
    ) -> None:
        for module in modules:
            module_branch = tree.add(module.name)
            module_source_ids = set(module.source_ids)
            for layer in layers:
                if module_source_ids.intersection(layer.source_ids):
                    module_branch.add(layer.name)

    def _add_groups(
        self,
        tree: Tree,
        title: str,
        groups: tuple[ArchitectureGroup, ...],
    ) -> None:
        branch = tree.add(title)
        for group in groups:
            group_branch = branch.add(group.name)
            for source_id in group.source_ids:
                group_branch.add(source_id)
