"""Perplexicon — a conlang lexicon tool.

Data model:
  Lexicon → Entry → Sense → gloss strings
  Each sense belongs to a Category (part of speech).

All domain types are frozen dataclasses that validate on construction.
If you have a Category/Sense/Entry/Lexicon instance, it's already valid.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

# - Domain types ---


@dataclass(frozen=True, slots=True)
class Category:
    """A part of speech (e.g. "noun" abbreviated "n.")."""

    name: str
    abbr: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            msg = "Category.name must be non-empty"
            raise ValueError(msg)
        if not self.abbr or not self.abbr.strip():
            msg = f"Category({self.name!r}).abbr must be non-empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Sense:
    """One meaning of a term: a category plus one or more glosses (translations).

    Glosses are ordered and unique within a sense. The optional label
    disambiguates when a term has multiple senses under the same category
    (e.g. "run" as a verb meaning both "to sprint" and "to operate").
    """

    cat: Category
    glosses: tuple[str, ...]
    label: str | None = None

    def __post_init__(self) -> None:
        if not self.glosses:
            msg = f"Sense({self.cat.name!r}): glosses must be non-empty"
            raise ValueError(msg)
        seen: set[str] = set()
        for g in self.glosses:
            if not g or not g.strip():
                msg = f"Sense({self.cat.name!r}): empty gloss"
                raise ValueError(msg)
            if g in seen:
                msg = f"Sense({self.cat.name!r}): duplicate gloss {g!r}"
                raise ValueError(msg)
            seen.add(g)


@dataclass(frozen=True, slots=True)
class Entry:
    """A single term in the lexicon with one or more senses.

    No two senses may share the same (category, label) pair — that
    would make them indistinguishable.
    """

    term: str
    senses: tuple[Sense, ...]

    def __post_init__(self) -> None:
        if not self.term or not self.term.strip():
            msg = "Entry.term must be non-empty"
            raise ValueError(msg)
        if not self.senses:
            msg = f"Entry({self.term!r}): senses must be non-empty"
            raise ValueError(msg)
        seen: set[tuple[str, str | None]] = set()
        for s in self.senses:
            key = (s.cat.name, s.label)
            if key in seen:
                msg = f"Entry({self.term!r}): duplicate sense {key}"
                raise ValueError(msg)
            seen.add(key)


@dataclass(frozen=True, slots=True)
class Lexicon:
    categories: Mapping[str, Category]  # name → Category
    entries: Mapping[str, Entry]  # term → Entry (insertion-ordered)


# - Type aliases ---

type Predicate = Callable[[Entry], bool]
type SortKey = Callable[[Entry], str]


# - Loading & saving -


class LexiconError(Exception):
    """Raised when a lexicon JSON file is malformed or violates constraints."""


def load(source: str | Path) -> Lexicon:
    """Read a lexicon JSON file and return a validated Lexicon.

    Checks that every sense references a declared part of speech and that
    no term appears twice.  Per-field checks (non-empty, no duplicate
    glosses, etc.) are handled by the dataclass __post_init__ methods.
    """
    raw = json.loads(Path(source).read_text(encoding="utf-8"))

    # Build the category lookup table from the "poses" array.
    categories: dict[str, Category] = {}
    for p in raw.get("poses", []):
        name = p["pos"]
        if name in categories:
            msg = f"Duplicate POS {name!r}"
            raise LexiconError(msg)
        categories[name] = Category(name=name, abbr=p["abbr"])

    # Parse each term and its senses, resolving POS names to Category objects.
    entries: dict[str, Entry] = {}
    for t in raw.get("terms", []):
        term: str = t["term"]
        if term in entries:
            msg = f"Duplicate term {term!r}"
            raise LexiconError(msg)
        raw_senses: list[dict[str, object]] = t["senses"]
        if not raw_senses:
            msg = f"{term!r}: no senses"
            raise LexiconError(msg)
        senses: list[Sense] = []
        for s in raw_senses:
            pos_name = s["pos"]
            if pos_name not in categories:
                msg = f"{term!r}: undeclared POS {pos_name!r}"
                raise LexiconError(msg)
            glosses = s["glosses"]
            if not glosses:
                msg = f"{term!r}: sense needs ≥1 gloss"
                raise LexiconError(msg)
            senses.append(Sense(cat=categories[pos_name], glosses=tuple(glosses)))
        entries[term] = Entry(term=term, senses=tuple(senses))

    return Lexicon(categories=categories, entries=entries)


def serialize(lex: Lexicon) -> dict[str, object]:
    """Convert a Lexicon back to the JSON-compatible dict format."""
    return {
        "poses": [{"pos": c.name, "abbr": c.abbr} for c in lex.categories.values()],
        "terms": [
            {
                "term": e.term,
                "senses": [{"pos": s.cat.name, "glosses": list(s.glosses)} for s in e.senses],
            }
            for e in lex.entries.values()
        ],
    }


def save(lex: Lexicon, path: str | Path) -> None:
    """Serialize a Lexicon and write it to a JSON file."""
    Path(path).write_text(
        json.dumps(serialize(lex), indent=4, ensure_ascii=False), encoding="utf-8"
    )


# - Templates & rendering --


@dataclass(frozen=True, slots=True)
class Template:
    """Controls how entries are formatted as text.

    Each level of the entry tree (term, sense, gloss) has a prefix and suffix.
    Senses are joined by sense_joiner.  When numbered=True, glosses get a
    numeric prefix (1. 2. 3. ...).
    """

    term_prefix: str = ""
    term_suffix: str = " - "
    sense_prefix: str = "("
    sense_suffix: str = ") "
    sense_joiner: str = ""
    numbered: bool = True
    gloss_prefix: str = ". "
    gloss_suffix: str = " "
    after: str = "\n"


TEMPLATES: dict[str, Template] = {
    "default": Template(),
    "multiline": Template(
        term_suffix=":",
        sense_prefix="\n  ",
        sense_suffix="",
        numbered=False,
        gloss_prefix="\n    - ",
        gloss_suffix="",
        after="\n",
    ),
    "html": Template(
        term_prefix="<b>",
        term_suffix="</b> - ",
        sense_prefix="<i>(",
        sense_suffix=")</i> ",
        after="<br>\n",
    ),
    "multiline-html": Template(
        term_prefix="<p><b>",
        term_suffix="</b><br><ul>",
        sense_prefix="<li>",
        sense_suffix="<ul>",
        numbered=False,
        gloss_prefix="<li>",
        gloss_suffix="</li>",
        sense_joiner="</ul>",
        after="</ul></ul></p>\n",
    ),
    "latex": Template(
        term_prefix="\\textbf{",
        term_suffix="} - ",
        sense_prefix="\\textit{(",
        sense_suffix=")} ",
    ),
    "webster": Template(
        term_suffix=" ",
        sense_prefix="",
        sense_suffix=": ",
        sense_joiner="  ",
    ),
    "webster-html": Template(
        term_prefix="<b>",
        term_suffix="</b> ",
        sense_prefix="<i>",
        sense_suffix="</i> ",
        after="<br>\n",
    ),
}


def _render_gloss(tmpl: Template, index: int, gloss: str) -> str:
    """Format a single gloss, optionally with a number prefix."""
    num = str(index) if tmpl.numbered else ""
    return f"{num}{tmpl.gloss_prefix}{gloss}{tmpl.gloss_suffix}"


def _render_sense(tmpl: Template, sense: Sense) -> str:
    """Format a sense: the POS abbreviation followed by its glosses."""
    glosses = "".join(_render_gloss(tmpl, i, g) for i, g in enumerate(sense.glosses, 1))
    return f"{tmpl.sense_prefix}{sense.cat.abbr}{tmpl.sense_suffix}{glosses}"


def render(tmpl: Template, entry: Entry) -> str:
    """Format a full entry by rendering each sense and joining them."""
    parts = [_render_sense(tmpl, s) for s in entry.senses]
    return f"{tmpl.term_prefix}{entry.term}{tmpl.term_suffix}{tmpl.sense_joiner.join(parts)}{tmpl.after}"


# - Query predicates -
# Each predicate factory returns a function Entry → bool.
# Compose them with and_pred / or_pred / not_pred, then pass to select().


def match_all(_e: Entry) -> bool:
    """Accepts every entry."""
    return True


def by_term(q: str) -> Predicate:
    """Exact match on the term string."""
    return lambda e: e.term == q


def by_substring(q: str) -> Predicate:
    """Case-insensitive substring match on the term."""
    q_lower = q.casefold()
    return lambda e: q_lower in e.term.casefold()


def by_gloss(q: str) -> Predicate:
    """Case-insensitive substring match on any gloss in any sense."""
    q_lower = q.casefold()
    return lambda e: any(q_lower in g.casefold() for s in e.senses for g in s.glosses)


def by_category(cat: str) -> Predicate:
    """Match entries that have at least one sense in the given category."""
    return lambda e: any(s.cat.name == cat for s in e.senses)


def and_pred(a: Predicate, b: Predicate) -> Predicate:
    return lambda e: a(e) and b(e)


def or_pred(a: Predicate, b: Predicate) -> Predicate:
    return lambda e: a(e) or b(e)


def not_pred(p: Predicate) -> Predicate:
    return lambda e: not p(e)


def select(pred: Predicate, lex: Lexicon) -> list[Entry]:
    """Return all entries in the lexicon that satisfy the predicate."""
    return [e for e in lex.entries.values() if pred(e)]


# - View pipeline ---


def alphabetical(e: Entry) -> str:
    """Sort key for case-insensitive alphabetical ordering."""
    return e.term.casefold()


def view(
    lex: Lexicon,
    *,
    pred: Predicate = match_all,
    tmpl: Template = TEMPLATES["default"],
    sort_key: SortKey | None = None,
    index: int | None = None,
) -> str:
    """The main pipeline: filter → sort → pick → render → join.

    Applies the predicate to select matching entries, optionally sorts them,
    optionally picks a single entry by index, then renders each entry with the
    template and concatenates the results.
    """
    entries = select(pred, lex)
    if sort_key is not None:
        entries.sort(key=sort_key)
    if index is not None:
        entries = [entries[index]]
    return "".join(render(tmpl, e) for e in entries)


# - Statistics


@dataclass(frozen=True, slots=True)
class Stats:
    entries: int
    senses: int
    glosses: int
    polysemous: int  # entries with more than one sense
    categories: Mapping[str, int]  # category name → number of senses


def stats(lex: Lexicon) -> Stats:
    """Count entries, senses, glosses, and per-category sense totals."""
    cat_counts: dict[str, int] = {}
    n_senses = 0
    n_glosses = 0
    polysemous = 0
    for e in lex.entries.values():
        n_senses += len(e.senses)
        if len(e.senses) > 1:
            polysemous += 1
        for s in e.senses:
            n_glosses += len(s.glosses)
            cat_counts[s.cat.name] = cat_counts.get(s.cat.name, 0) + 1
    return Stats(
        entries=len(lex.entries),
        senses=n_senses,
        glosses=n_glosses,
        polysemous=polysemous,
        categories=cat_counts,
    )


# - Merge ---


def merge(a: Lexicon, b: Lexicon) -> Lexicon:
    """Merge two lexicons into one.

    Categories must be compatible (same name → same abbreviation).
    When both lexicons have the same term, their senses are combined:
    senses with the same (category, label) get their gloss lists merged
    (A's order preserved, B's novel glosses appended).
    """
    cats: dict[str, Category] = dict(a.categories)
    for name, cat_b in b.categories.items():
        if name in cats and cats[name] != cat_b:
            msg = f"Category conflict for {name!r}: {cats[name].abbr!r} vs {cat_b.abbr!r}"
            raise LexiconError(msg)
        cats[name] = cat_b

    entries: dict[str, Entry] = dict(a.entries)
    for term, eb in b.entries.items():
        if term not in entries:
            entries[term] = eb
            continue
        # Term exists in both — merge senses by (category, label) key.
        ea = entries[term]
        sense_map: dict[tuple[str, str | None], list[str]] = {}
        sense_cats: dict[str, Category] = {}
        for s in (*ea.senses, *eb.senses):
            key = (s.cat.name, s.label)
            sense_cats[s.cat.name] = s.cat
            existing = sense_map.setdefault(key, [])
            for g in s.glosses:
                if g not in existing:
                    existing.append(g)
        merged_senses = tuple(
            Sense(cat=sense_cats[k[0]], glosses=tuple(gs), label=k[1])
            for k, gs in sense_map.items()
        )
        entries[term] = Entry(term=term, senses=merged_senses)

    return Lexicon(categories=cats, entries=entries)


# - Synonym detection -


def find_synonyms(lex: Lexicon) -> dict[str, list[tuple[str, str]]]:
    """Find glosses that appear in more than one entry.

    Returns a dict mapping each shared gloss string to the list of
    (term, category) pairs where it appears.
    """
    index: dict[str, list[tuple[str, str]]] = {}
    for e in lex.entries.values():
        for s in e.senses:
            for g in s.glosses:
                index.setdefault(g, []).append((e.term, s.cat.name))
    return {g: locs for g, locs in index.items() if len(locs) > 1}
