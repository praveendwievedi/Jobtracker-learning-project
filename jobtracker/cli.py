import sys
import argparse
from pathlib import Path
from .parser import parse_posting
import json
from .exceptions import JobPostingError
from .storage import PostingStorage

def handle_add(args : argparse.Namespace) -> int:
        posting = parse_posting(args.file)
        store = PostingStorage(args.store)
        is_new = store.add(posting)

        if is_new:
            print(f"Added: {posting.title} @ {posting.company}")
        else:
            print(f"Already exists: {posting.title} @ {posting.company}")
        return 0

def handle_list(args : argparse.Namespace) -> int:
        store = PostingStorage(args.store)
        posting = store.all()

        for p in posting:
            skills = ",".join(p.skills) if p.skills else "None"
            print(f"• {p.title.title()} @ {p.company.title()} [{p.location.title()}]")
            print(f"  Skills: {skills}\n")
        return 0

def build_parser()-> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description="Job Tracker CLI")
    subparser = parser.add_subparsers(dest="command", required=True)

    parser_add = subparser.add_parser("add", help="Add a new Job Posting")
    parser_add.add_argument("file", type= Path, help="Path to JD .txt file")
    parser_add.add_argument("--store", type= Path,default=Path("data/postings.json"))
    parser_add.set_defaults(handler= handle_add)

    parser_list= subparser.add_parser("list", help="List all saved job postings")
    parser_list.add_argument("--store", type= Path , default=Path("data/postings.json"))
    parser_list.add_argument("--json", action="store_true", help="Output as JSON")
    parser_list.set_defaults(handler= handle_list)
    return parser


def main(argv: str | None =None) -> int :
    parser= build_parser()
    args=  parser.parse_args(argv)
    try:
        return args.handler(args)
    except JobPostingError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())