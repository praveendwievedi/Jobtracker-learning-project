import json
from .models import JobPosting 
from pathlib import Path
from .exceptions import StorageError

class PostingStorage:
    def __init__(self, path:Path):
        self.path =path
        self.path.parent.mkdir(parents=True,exist_ok=True)
    def list(self) ->list[JobPosting]:
        if not self.path.exists():
            return []
        try:
            postings= json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise StorageError(f"Failed to decode JSON from storage: {self.path}") from e
        return [JobPosting.from_dict(posting) for posting in postings]
    def save(self,postings:list[JobPosting]) -> None:
        data=[posting.to_dict() for posting in postings]
        posting_data=json.dumps(data,indent=2)
        try:
            self.path.write_text(posting_data,encoding="utf-8")
        except OSError as e:
            raise StorageError(f"Failed to put into the storage: {self.path}") from e
    def all(self) -> list[JobPosting]:
        return self.list()
    def add(self,posting: JobPosting) -> bool:
        postings=self.list()
        for post in postings:
            if post.key() == posting.key():
                return False
        postings.append(posting)
        self.save(postings)
        return True
    def search(self,skill:str | None , location : str | None = None) -> list[JobPosting]:
        postings = self.list()
        if skill:
            postings= [p for p in postings if p.matches_skills(skill)]
        if location:
            postings=[p for p in postings if location.strip().lower() in p.location().lower()]
        return postings