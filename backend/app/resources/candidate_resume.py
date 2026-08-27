from pathlib import Path

CANDIDATE_RESUME_PDF_FILENAME = "mei_chang_resume.pdf"
CANDIDATE_RESUME_PDF_SHA256 = (
    "20a4d191dcc675b67a55da4296c2200cf2ceed1b3deb9aca4fbdf9e5e8cb08bd"
)
CANDIDATE_RESUME_CONTEXT_FILENAME = "mei_chang_resume.md"
CANDIDATE_RESUME_CONTEXT_SHA256 = (
    "9e1db40802663dd49fc5ece9637a7b386f3f7a7dcc552bdc7444ae1cf17e1c04"
)


def _resume_directory() -> Path:
    return Path(__file__).resolve().parent / "resume"


def get_candidate_resume_path() -> Path:
    return _resume_directory() / CANDIDATE_RESUME_PDF_FILENAME


def get_candidate_resume_context_path() -> Path:
    return _resume_directory() / CANDIDATE_RESUME_CONTEXT_FILENAME
