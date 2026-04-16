from __future__ import annotations

from fastapi import FastAPI

from app.engine import run_recognition
from app.exporters import export_document
from app.learning import LearningStore
from app.schemas import (
    ExportRequest,
    FeedbackRecord,
    LearningJob,
    LearningJobResult,
    RecognizeRequest,
    RecognizeResult,
)

app = FastAPI(title="OCR Local Platform API", version="0.1.0")
learning_store = LearningStore()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recognize", response_model=RecognizeResult)
def recognize(payload: RecognizeRequest) -> RecognizeResult:
    return run_recognition(payload)


@app.post("/feedback")
def submit_feedback(payload: FeedbackRecord) -> dict[str, str]:
    learning_store.add_feedback(payload)
    return {"status": "stored", "doc_id": payload.doc_id}


@app.post("/learning/job", response_model=LearningJobResult)
def submit_learning_job(payload: LearningJob) -> LearningJobResult:
    return learning_store.run_job(payload)


@app.post("/export")
def export(payload: RecognizeRequest, export: ExportRequest) -> dict[str, str]:
    result = run_recognition(payload)
    content = export_document(result.document, export)
    return {"format": export.format.value, "content": content}
