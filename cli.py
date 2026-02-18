"""Command-line interface for Perplexicon.

Parses arguments, loads a lexicon JSON file, applies search/sort/template
options, and prints the result to stdout or writes it to a file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from perplexicon import (
    TEMPLATES,
    LexiconError,
    Predicate,
    alphabetical,
    by_gloss,
    by_substring,
    by_term,
    load,
    match_all,
    view,
)


def _build_pipeline(args: argparse.Namespace) -> tuple[Predicate, int | None]:
    """Turn the -m/--method and -q/--query flags into a (predicate, index) pair."""
    match args.method:
        case "term":
            return (by_term(args.query) if args.query else match_all), None
        case "term-part":
            return (by_substring(args.query) if args.query else match_all), None
        case "gloss":
            return (by_gloss(args.query) if args.query else match_all), None
        case "index":
            return match_all, (int(args.query) if args.query else None)
    return match_all, None  # unreachable, argparse limits choices above


def main() -> None:
    parser = argparse.ArgumentParser(description="Print or query a conlang lexicon.")
    parser.add_argument("lex", help="Lexicon JSON file.")
    parser.add_argument("-q", "--query", help="Search query.")
    parser.add_argument(
        "-m",
        "--method",
        default="term-part",
        choices=["term", "term-part", "gloss", "index"],
        help="Search method (default: term-part).",
    )
    parser.add_argument(
        "-t",
        "--template",
        default="default",
        choices=list(TEMPLATES),
        help="Output template.",
    )
    parser.add_argument("-s", "--sort", action="store_true", help="Alphabetize output.")
    parser.add_argument("-o", "--output", help="Write to file instead of stdout.")
    args = parser.parse_args()

    try:
        lex = load(args.lex)
    except FileNotFoundError:
        print(f"File not found: {args.lex}", file=sys.stderr)
        sys.exit(1)
    except LexiconError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    pred, index = _build_pipeline(args)

    sort_key = alphabetical if args.sort else None
    tmpl = TEMPLATES[args.template]

    try:
        result = view(lex, pred=pred, tmpl=tmpl, sort_key=sort_key, index=index)
    except IndexError:
        print(
            f"Index {args.query} out of range (lexicon has {len(lex.entries)} entries)",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
