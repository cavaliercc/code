from __future__ import annotations

from app.schemas import Document, ExportFormat, ExportMode, ExportRequest


def export_document(document: Document, request: ExportRequest) -> str:
    """
    Return serialized content as a string placeholder.
    Real implementation can write files under exports/.
    """
    meta = f"doc_id={document.doc_id}; mode={request.mode.value}"

    if request.format == ExportFormat.txt:
        return "\n".join(_iter_text(document))

    if request.format == ExportFormat.md:
        body = "\n\n".join(f"- {line}" for line in _iter_text(document))
        return f"# OCR Result\n\n{body}\n"

    if request.format == ExportFormat.docx:
        return f"[DOCX_PLACEHOLDER] {meta}"

    if request.format == ExportFormat.xlsx:
        split_info = "split" if request.split_table_to_sheets else "single-sheet"
        return f"[XLSX_PLACEHOLDER] {meta}; table_strategy={split_info}"

    raise ValueError(f"Unsupported format: {request.format}")


def _iter_text(document: Document) -> list[str]:
    lines: list[str] = []
    for page in document.pages:
        for block in page.blocks:
            if block.paragraph:
                lines.append(block.paragraph.text)
            elif block.table:
                lines.append(f"[table:{block.table.id}]")
            else:
                lines.append(f"[{block.kind}:{block.id}]")
    return lines
