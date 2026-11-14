class JobPostingError(Exception):
    """Base class for exceptions in this module."""
    pass
class InvalidPostingError(JobPostingError):
    """Exception raised for invalid job postings."""
    pass
class StorageError(JobPostingError):
    """Exception raised for storage-related errors."""
    pass