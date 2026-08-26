from pathlib import Path


def get_candidate_resume_path() -> Path:
    return Path(__file__).resolve().parent / "resume" / "mei_chang_resume.pdf"
