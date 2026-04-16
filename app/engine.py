from __future__ import annotations

from app.schemas import (
    Block,
    Document,
    EngineDecision,
    EnginePath,
    Page,
    Paragraph,
    RecognizeRequest,
    RecognizeResult,
    Table,
)


def decide_engine(request: RecognizeRequest) -> EngineDecision:
    triggers: list[str] = []

    if request.force_complex_layout:
        triggers.append("complex_layout")
    if request.table_restore_failed:
        triggers.append("table_restore_failed")
    if request.field_conflict:
        triggers.append("field_conflict")
    if request.low_confidence_segments > 0:
        triggers.append("low_confidence_segments")

    if triggers:
        return EngineDecision(
            selected_path=EnginePath.pro,
            upgraded=True,
            reason="Detected hard cases; escalated from Lite to Pro.",
            triggers=triggers,
        )

    return EngineDecision(
        selected_path=EnginePath.lite,
        upgraded=False,
        reason="No hard-case trigger detected; Lite path is sufficient.",
    )


def run_recognition(request: RecognizeRequest) -> RecognizeResult:
    decision = decide_engine(request)

    intro = (
        "这是一份模拟识别结果。"
        "在生产环境中将接入 PP-OCRv5/PP-StructureV3 与 PaddleOCR-VL-1.5。"
    )

    paragraph = Paragraph(id="p1", text=intro, confidence=0.97)
    table = Table(id="t1", cells=[])
    page = Page(
        page_no=1,
        blocks=[
            Block(id="b1", kind="paragraph", paragraph=paragraph),
            Block(id="b2", kind="table", table=table),
        ],
    )

    document = Document(
        doc_id=f"doc::{request.file_path}",
        pages=[page],
        reading_order=["b1", "b2"],
        confidence=0.97 if decision.selected_path == EnginePath.pro else 0.94,
    )

    chain = [EnginePath.lite]
    if decision.upgraded:
        chain.append(EnginePath.pro)

    return RecognizeResult(
        document=document,
        raw_text=intro,
        tables=[table],
        reading_order=document.reading_order,
        confidence=document.confidence,
        engine_chain=chain,
        decision=decision,
    )
