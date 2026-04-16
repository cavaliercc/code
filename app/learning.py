from __future__ import annotations

from collections import defaultdict

from app.schemas import FeedbackRecord, LearningJob, LearningJobResult


class LearningStore:
    """In-memory placeholder for correction memory and learning jobs."""

    def __init__(self) -> None:
        self.feedback_records: list[FeedbackRecord] = []
        self.template_index: dict[str, list[FeedbackRecord]] = defaultdict(list)

    def add_feedback(self, record: FeedbackRecord) -> None:
        self.feedback_records.append(record)
        if record.template_id:
            self.template_index[record.template_id].append(record)

    def run_job(self, job: LearningJob) -> LearningJobResult:
        if job.job_type.value == "local_finetune":
            sample_size = len(self.feedback_records)
            if sample_size < 20:
                return LearningJobResult(
                    accepted=False,
                    message=f"Not enough samples for finetune: {sample_size}/20",
                )

        return LearningJobResult(
            accepted=True,
            message=f"Learning job accepted: {job.job_type.value}",
        )
