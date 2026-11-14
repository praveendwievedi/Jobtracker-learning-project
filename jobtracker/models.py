from dataclasses import dataclass
from typing import Any

@dataclass
class JobPosting:
    title: str
    company: str
    location: str
    skills: list[str]
    source_file: str
    added_at : str
    def __post_init__(self):
        self.skills  =[skill.strip().lower() for skill in self.skills]
        self.skills.sort()
        self.title =self.title.strip().lower()
        self.company = self.company.strip().lower()
        self.location = self.location.strip().lower()
    def key (self):
        return f"{self.title}-{self.company}-{self.location}"
    def matches_skills(self, skill: str) -> bool:
        return skill.strip().lower() in self.skills
    def to_dict(self) -> dict[str,any]:
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "skills": self.skills,
            "source_file": self.source_file,
            "added_at": self.added_at
        }
    @classmethod
    def from_dict(cls, data: dict[str,Any]) -> 'JobPosting':
        return cls(
            title=data.get("title", ""),
            company=data.get("company", ""),
            location=data.get("location", ""),
            skills=data.get("skills", []),
            source_file=data.get("source_file", ""),
            added_at=data.get("added_at", "")
        )