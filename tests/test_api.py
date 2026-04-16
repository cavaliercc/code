from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_recognize_escalation() -> None:
    payload = {
        "file_path": "sample.pdf",
        "force_complex_layout": True,
        "export_preference": ["md"],
    }
    response = client.post("/recognize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"]["selected_path"] == "pro"
    assert data["decision"]["upgraded"] is True


def test_feedback_and_learning_job() -> None:
    feedback = {
        "doc_id": "doc::sample.pdf",
        "page_no": 1,
        "region": "header",
        "before_text": "0CR",
        "after_text": "OCR",
        "allow_training": True,
    }
    fb_resp = client.post("/feedback", json=feedback)
    assert fb_resp.status_code == 200

    job = {"job_type": "template_learning", "payload": {"template_id": "contract_v1"}}
    job_resp = client.post("/learning/job", json=job)
    assert job_resp.status_code == 200
    assert job_resp.json()["accepted"] is True
