from hashlib import sha256
from typing import get_args

from fastapi.testclient import TestClient

from app.ai.schemas import ResumeSourceReference
from app.resources.candidate_resume import (
    CANDIDATE_RESUME_CONTEXT_SHA256,
    CANDIDATE_RESUME_PDF_SHA256,
    get_candidate_resume_context_path,
    get_candidate_resume_path,
)


def test_resume_preview_returns_the_approved_pdf(client: TestClient) -> None:
    response = client.get("/api/resume")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"].startswith("inline;")
    assert response.headers["cache-control"] == "no-store, max-age=0"
    assert response.headers["pragma"] == "no-cache"
    assert sha256(response.content).hexdigest() == CANDIDATE_RESUME_PDF_SHA256


def test_resume_download_returns_the_same_approved_pdf(client: TestClient) -> None:
    response = client.get("/api/resume?download=true")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"].startswith("attachment;")
    assert response.headers["cache-control"] == "no-store, max-age=0"
    assert sha256(response.content).hexdigest() == CANDIDATE_RESUME_PDF_SHA256


def test_resume_preview_accepts_a_cache_busting_version(client: TestClient) -> None:
    response = client.get("/api/resume?v=03f5c8b961b6d136")

    assert response.status_code == 200
    assert sha256(response.content).hexdigest() == CANDIDATE_RESUME_PDF_SHA256


def test_fixed_resume_pair_has_approved_names_digests_and_utf8_context() -> None:
    resume_path = get_candidate_resume_path()
    context_path = get_candidate_resume_context_path()

    assert resume_path.name == "mei_chang_resume.pdf"
    assert context_path.name == "mei_chang_resume.md"
    assert sha256(resume_path.read_bytes()).hexdigest() == CANDIDATE_RESUME_PDF_SHA256
    assert sha256(context_path.read_bytes()).hexdigest() == CANDIDATE_RESUME_CONTEXT_SHA256
    assert context_path.read_text(encoding="utf-8").strip()


def test_evidence_source_references_match_visible_resume_headings() -> None:
    headings = {
        line.lstrip("#").strip()
        for line in get_candidate_resume_context_path().read_text(encoding="utf-8").splitlines()
        if line.startswith("#")
    }
    headings.remove("梅唱")

    assert set(get_args(ResumeSourceReference)) == headings
