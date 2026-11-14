""" Job Tracker CLI - Track , search and analyse job description """
__version__ = "0.1.0"

from .models import JobPosting
from .storage import PostingStorage
from .exceptions import JobPostingError, InvalidPostingError,StorageError
from .cli import main


__all__=[
    "__version__",
    "JobPosting",
    "PostingStorage",
    "JobPostingError",
    "InvalidPostingError",
    "StorageError"
]
