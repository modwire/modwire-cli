from __future__ import annotations

from abc import ABC, abstractmethod

from .context import ReportPipelineContext


class ReportPipelineStep(ABC):
    @abstractmethod
    def should_process(self, context: ReportPipelineContext) -> bool: ...

    @abstractmethod
    def process(self, context: ReportPipelineContext) -> ReportPipelineContext: ...
