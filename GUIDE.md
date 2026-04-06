# Perplexicon: A Complete Guide

Here is what Perplexicon produces. Read it carefully — every term used in this guide appears in it:

```
nit - (v.) 1. to see  2. to watch  3. to appear  (n.) 1. sight
writ - (v.) 1. to hear  2. to listen  (n.) 1. hearing
```

Each line is one **word**. A label in parentheses — `(v.)`, `(n.)` — opens a **sense**: one grammatical role of that word. Each numbered item inside a sense is a **gloss**: one definition. *nit* has two senses and four glosses. *writ* has two senses and three glosses.

That's the whole model. Everything else is filling it in.

> **Requirement:** Python 3.13 or newer. Check with `python --version`. No other installs needed.

---

## Part 1: Build It

Your lexicon lives in a single JSON file. JSON is plain text — quotes, colons, commas, and brackets all carry meaning, and a single missing comma will cause an error. Copy the examples carefully.

---

### Step 1: Create the file

Create `mylang.json` and paste in this skeleton:

```json
{
    "poses": [],
    "terms": []
}
```

`poses` is where you declare your parts of speech. `terms` is where your words go.

---

### Step 2: Declare your parts of speech

```json
{
    "poses": [
        {"pos": "noun", "abbr": "n."},
        {"pos": "verb", "abbr": "v."}
    ],
    "terms": []
}
```

`pos` is the full name; `abbr` is what prints in the output. You declare them here separately so Perplexicon can reject any word that references a category you haven't defined.

`nit: undeclared POS 'adjective'` — add `{"pos": "adjective", "abbr": "adj."}` to `poses`.

---

### Step 3: First word — one sense, one gloss

```json
{
    "poses": [
        {"pos": "noun", "abbr": "n."},
        {"pos": "verb", "abbr": "v."}
    ],
    "terms": [
        {
            "term": "nit",
            "senses": [
                {"pos": "verb", "glosses": ["to see"]}
            ]
        }
    ]
}
```

Run it:

```
python cli.py mylang.json
```

```
nit - (v.) 1. to see
```

One word, one sense, one gloss. The `pos` inside a sense must match a name in `poses` exactly — `"verb"` and `"Verb"` are different.

`nit: sense needs ≥1 gloss` — every sense must have at least one item in `glosses`.

---

### Step 4: One sense, three glosses

Add "to watch" and "to appear" to the same sense:

```json
{
    "poses": [
        {"pos": "noun", "abbr": "n."},
        {"pos": "verb", "abbr": "v."}
    ],
    "terms": [
        {
            "term": "nit",
            "senses": [
                {"pos": "verb", "glosses": ["to see", "to watch", "to appear"]}
            ]
        }
    ]
}
```

```
nit - (v.) 1. to see 2. to watch 3. to appear
```

Glosses print in the order you write them. The first is the primary meaning.

---

### Step 5: One word, two senses

*nit* is also a noun meaning "sight". Add a second sense to the same word:

```json
{
    "poses": [
        {"pos": "noun", "abbr": "n."},
        {"pos": "verb", "abbr": "v."}
    ],
    "terms": [
        {
            "term": "nit",
            "senses": [
                {"pos": "verb", "glosses": ["to see", "to watch", "to appear"]},
                {"pos": "noun", "glosses": ["sight"]}
            ]
        }
    ]
}
```

```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
```

A word can carry as many senses as your language needs, each with its own glosses.

---

### Step 6: Two words

```json
{
    "poses": [
        {"pos": "noun", "abbr": "n."},
        {"pos": "verb", "abbr": "v."}
    ],
    "terms": [
        {
            "term": "nit",
            "senses": [
                {"pos": "verb", "glosses": ["to see", "to watch", "to appear"]},
                {"pos": "noun", "glosses": ["sight"]}
            ]
        },
        {
            "term": "writ",
            "senses": [
                {"pos": "verb", "glosses": ["to hear", "to listen"]},
                {"pos": "noun", "glosses": ["hearing"]}
            ]
        }
    ]
}
```

```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
writ - (v.) 1. to hear 2. to listen (n.) 1. hearing
```

You've just built the lexicon from the opening.

`Duplicate term 'nit'` — the same word appears twice. Remove one entry or merge their senses into a single one.

---

## Part 2: Query It

Every command runs your lexicon through one pipeline: filter, then sort, then format, then output. The flags below control one stage each and compose freely.

**Search by word** (`-q` matches any word containing your query):

```
python cli.py mylang.json -q nit
```
```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
```

**Search by definition** (`-m gloss` searches inside glosses):

```
python cli.py mylang.json -q hear -m gloss
```
```
writ - (v.) 1. to hear 2. to listen (n.) 1. hearing
```

For all search modes, see [README.md#search-methods](README.md#search-methods).

**Sort alphabetically** (`-s`):

```
python cli.py mylang.json -s
```

**Change the output format** (`-t`):

```
python cli.py mylang.json -t multiline
```
```
nit:
  verb
    - to see
    - to watch
    - to appear
  noun
    - sight
```

Available templates: `default`, `multiline`, `webster`, `html`, `latex`, and their HTML variants. See [README.md#templates](README.md#templates).

**Write to a file** (`-o`):

```
python cli.py mylang.json -o output.txt
```

**Combining flags:**

```
python cli.py mylang.json -s -t html -o dictionary.html
python cli.py mylang.json -q hear -m gloss -t latex -o results.tex
```

---

## Part 3: Own It

`load()` returns the same structure you built in Part 1 — words, senses, glosses — as Python objects. Everything in the API is an operation on that structure.

```python
from perplexicon import load, save, merge, stats, find_synonyms
```

**Merge two lexicons.** Words in both are combined by sense; novel words are added:

```python
combined = merge(load("dialect_a.json"), load("dialect_b.json"))
save(combined, "merged.json")
```

**Get statistics.** The same counts you tracked through Part 1 — words, senses, glosses — plus more:

```python
s = stats(load("mylang.json"))
print(s.entries, s.senses, s.glosses)
# s.polysemous = number of words with more than one sense
```

**Find accidental synonyms** — different words sharing the exact same gloss:

```python
dupes = find_synonyms(load("mylang.json"))
# {"to see": [("nit", "verb"), ("vitar", "verb")]}
```

---

## Quick Reference

**Minimum valid file:**
```json
{
    "poses": [{"pos": "noun", "abbr": "n."}],
    "terms": [
        {"term": "kala", "senses": [{"pos": "noun", "glosses": ["fish"]}]}
    ]
}
```

**Common commands:**
```bash
python cli.py mylang.json                          # print all
python cli.py mylang.json -q nit                   # filter by word
python cli.py mylang.json -q hear -m gloss         # filter by definition
python cli.py mylang.json -s -t html -o out.html   # sort, format, and save
```
