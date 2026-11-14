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

        if not posting:
            print("No job postings found.")
            return 0
        if args.json:
            data = [p.to_dict() for p in posting]
            print(json.dumps(data, indent=2))
        else:
            for p in posting:
                skills = ", ".join(p.skills) if p.skills else "None"
                print(f"• {p.title.title()} @ {p.company.title()} [{p.location.title()}]")
                print(f"  Skills: {skills}\n")
        return 0

def handle_search( args: argparse.Namespace) -> int:
    store = PostingStorage(args.store)
    if not (args.skills or args.location or args.company):
        print("Error: At least one filter (--skill, --location, or --company) is required.", file=sys.stderr)
        return 1
    postings= store.search(skill=args.skills,location=args.location,comapny=args.company)

    if postings:
        print("No job posting found. ")
        return 0
    if args.json:
        data = [p.to_dict() for p in postings]
        print(json.dumps(data, indent=2))
    else:
        for p in postings:
            skills = ", ".join(p.skills) if p.skills else "None"
            print(f"• {p.title.title()} @ {p.company.title()} [{p.location.title()}]")
            print(f"  Skills: {skills}\n")
    
    return 0

# def handle_stats(args: argparse.Namespac) -> int:
#     pass

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

    parser_search=subparser.add_parser("search", help="Search the Jobs based on skills and location")
    parser_search.add_argument("--skills", type=str, help="Filter by skills")
    parser_search.add_argument("--location" , type=str, help="Filter by locaiton")
    parser_search.add_argument("--company" , type=str, help="Filter by company")
    parser_search.add_argument("--store",type= Path,default=Path("data/postings.json"), help="Path to JSON store")
    parser_search.add_argument("--json",action="store_true", help="Output as JSON")
    parser_search.set_defaults(handler= handle_search)

    # parser_stats= subparser.add_parser("stats", help="Stats of the Jobs Postings")
    # parser_stats.add_argument("file" , type=Path,help="Path to JD .txt file")
    # parser_stats.add_argument("--top",type= int,help="Stats of top job postings")
    # parser_stats.set_defaults(handler= handle_stats)
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