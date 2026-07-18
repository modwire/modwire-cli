from __future__ import annotations

from dataclasses import dataclass, replace
from typing import cast

from modwire_architecture.shared.report.base import ReportNode
from rich.console import Console


@dataclass(frozen=True)
class ReportPipelineContext:
    reports: tuple[ReportNode, ...]
    console: Console
    failed: bool = False

    def has_report(self, report_type: type[ReportNode]) -> bool:
        return any(type(report) is report_type for report in self.reports)

    def report[ReportType: ReportNode](self, report_type: type[ReportType]) -> ReportType:
        for report in self.reports:
            if type(report) is report_type:
                return cast(ReportType, report)
        raise LookupError(f"Missing report: {report_type.__name__}")

    def fail(self) -> ReportPipelineContext:
        return replace(self, failed=True)
