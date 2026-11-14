from pathlib import Path
from .exceptions import InvalidPostingError
from .models import JobPosting
import re

KNOWN_SKILLS: set[str] = {
    "java", "spring boot", "docker", "kubernetes", "postgresql",
    "rabbitmq", "react", "python", "c++", "kafka", "aws",
    "rest api", "microservices",
}

STOPWORDS: set[str] = {"the", "and", "a", "of", "to", "in", "with", 
                        "for", "is", "are", "we", "you", "our", "will", "be", "or", "on", "as", "an"}

def read_jd(path: Path) -> str:
    if not path.suffix.lower() == ".txt":
        raise InvalidPostingError(f"Invalid file type: {path}. Expected a .txt file.")
    try:
        content =path.read_text(encoding="utf-8")
    except FileNotFoundError as  e:
        raise InvalidPostingError(f"File not found: {path}") from e

    if( content.strip() ==""):
        raise InvalidPostingError(f"File is empty: {path}")
    return content

def parse_header(text : str) -> dict[str,str]:
    required_keys={"title","company","location"}
    header={}
    lines = text.splitlines()
    for line in lines:
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        header[key.strip().lower()] = value.strip()
    for key in required_keys:
        if key not in header:
            raise InvalidPostingError(f"Missing required header field: {key}")
    return header

# to do 
def tokenize(text:str) -> list[str]:
    raw_tokens= re.findall(r"[a-z0-9+#.]+", text.lower())
    print(raw_tokens)
    return [token.rstrip('.') for token in raw_tokens]


def word_count(text:str, top: int = 10) -> list[tuple[str,int]]:
    tokens = tokenize(text)
    count={}
    for token in tokens:
        if token not in STOPWORDS:  
            count[token]=count.get(token,0)+1
    ans=sorted(count.items(),key=lambda x: x[1],reverse=True)[:top]
    return ans

def detect_skills(text:str) ->list[str]:
    ans=[]
    for skill in KNOWN_SKILLS:
        if skill in text.lower():
            ans.append(skill)
    return ans

def parse_posting(path: Path) -> JobPosting: 
    content = read_jd(path)
    header = parse_header(content)
    skills = detect_skills(content)
    added_at= path.stat().st_mtime
    return JobPosting(
        title=header["title"],
        company=header["company"],
        location=header["location"],
        skills=skills,
        source_file=str(path),
        added_at=str(added_at)
    )

