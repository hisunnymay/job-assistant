from pathlib import Path

CANDIDATE_RESUME_PDF_FILENAME = "mei_chang_resume.pdf"
CANDIDATE_RESUME_PDF_SHA256 = (
    "30ebd7e42087fe6975ef7d4e067d88f2ab7a075844e370ccbddf14257c80fe79"
)
CANDIDATE_RESUME_CONTEXT_FILENAME = "mei_chang_resume.md"
CANDIDATE_RESUME_CONTEXT_SHA256 = (
    "8bcb54a37a4e6b15a44ed853708d0401eea170bf1b337fa860d8d41d171aa685"
)


def _resume_directory() -> Path:
    return Path(__file__).resolve().parent / "resume"


def get_candidate_resume_path() -> Path:
    return _resume_directory() / CANDIDATE_RESUME_PDF_FILENAME


def get_candidate_resume_context_path() -> Path:
    return _resume_directory() / CANDIDATE_RESUME_CONTEXT_FILENAME
