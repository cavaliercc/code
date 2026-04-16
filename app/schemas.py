from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PerformanceTier(str, Enum):
    cpu = "cpu"
    auto = "auto"
    gpu = "gpu"


class ExportFormat(str, Enum):
    txt = "txt"
    md = "md"
    docx = "docx"
    xlsx = "xlsx"


class ExportMode(str, Enum):
    layout_first = "layout_first"
    structured_first = "structured_first"


class EnginePath(str, Enum):
    lite = "lite"
    pro = "pro"


class Cell(BaseModel):
    row: int
    col: int
    text: str
    confidence: float = 1.0


class Table(BaseModel):
    id: str
    cells: list[Cell] = Field(default_factory=list)


class Paragraph(BaseModel):
    id: str
    text: str
    confidence: float = 1.0


class Block(BaseModel):
    id: str
    kind: str = Field(description="heading | paragraph | list | table | figure")
    paragraph: Paragraph | None = None
    table: Table | None = None


class Page(BaseModel):
    page_no: int
    blocks: list[Block] = Field(default_factory=list)


class CorrectionTrace(BaseModel):
    field: str
    original: str
    corrected: str
    scope: str


class Document(BaseModel):
    doc_id: str
    pages: list[Page]
    reading_order: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    correction_traces: list[CorrectionTrace] = Field(default_factory=list)


class EngineDecision(BaseModel):
    selected_path: EnginePath
    upgraded: bool = False
    reason: str
    triggers: list[str] = Field(default_factory=list)


class RecognizeRequest(BaseModel):
    file_path: str
    language: str = "zh+en"
    document_type_hint: str | None = None
    performance_tier: PerformanceTier = PerformanceTier.auto
    export_preference: list[ExportFormat] = Field(default_factory=lambda: [ExportFormat.md])
    enable_learning: bool = True
    force_complex_layout: bool = False
    low_confidence_segments: int = 0
    table_restore_failed: bool = False
    field_conflict: bool = False


class RecognizeResult(BaseModel):
    document: Document
    raw_text: str
    tables: list[Table] = Field(default_factory=list)
    reading_order: list[str] = Field(default_factory=list)
    confidence: float
    engine_chain: list[EnginePath]
    decision: EngineDecision


class FeedbackRecord(BaseModel):
    doc_id: str
    page_no: int
    region: str
    before_text: str
    after_text: str
    context: str | None = None
    template_id: str | None = None
    allow_training: bool = True


class ExportRequest(BaseModel):
    format: ExportFormat
    mode: ExportMode = ExportMode.layout_first
    split_table_to_sheets: bool = True
    include_metadata: bool = True


class LearningJobType(str, Enum):
    template_learning = "template_learning"
    lexicon_update = "lexicon_update"
    rule_update = "rule_update"
    local_finetune = "local_finetune"


class LearningJob(BaseModel):
    job_type: LearningJobType
    template_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class LearningJobResult(BaseModel):
    accepted: bool
    message: str
