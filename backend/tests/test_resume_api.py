from hashlib import sha256

from fastapi.testclient import TestClient

EXPECTED_RESUME_SHA256 = "20a4d191dcc675b67a55da4296c2200cf2ceed1b3deb9aca4fbdf9e5e8cb08bd"


def test_resume_preview_returns_the_approved_pdf(client: TestClient) -> None:
    response = client.get("/api/resume")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"].startswith("inline;")
    assert sha256(response.content).hexdigest() == EXPECTED_RESUME_SHA256


def test_resume_download_returns_the_same_approved_pdf(client: TestClient) -> None:
    response = client.get("/api/resume?download=true")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"].startswith("attachment;")
    assert sha256(response.content).hexdigest() == EXPECTED_RESUME_SHA256
