# Perplexicon: A Complete Guide

> **Requirement:** Python 3.13 or newer. Check with `python --version`. No other installs needed.

---

## The One Thing to Know Before You Start

Everything in Perplexicon is a container holding smaller containers:

```
Lexicon
  └── Word          (a term in your language)
        └── Sense   (one grammatical role of that word)
              └── Gloss (one definition within that role)
```

A word like *nit* can be both a verb and a noun — that's two **senses**. "To see" and "to watch" are two **glosses** inside the verb sense. Everything this tool does — building the file, running commands, calling the API — is either putting something into this hierarchy or looking something up in it.

Hold that picture. Every step below is just filling it in.

---

## What You're Working Towards

Given a two-word language, running:

```
python cli.py mylang.json
```

prints:

```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
writ - (v.) 1. to hear 2. to listen (n.) 1. hearing
```

Each line is one word. The abbreviation in parentheses marks the sense. Numbered items are its glosses. *nit* carries two senses — verb and noun — on a single line.

Everything in Part 1 is about producing this output. Parts 2 and 3 show you what to do once it works.

---

## Part 1: Building Your Lexicon File

Your lexicon is a single JSON file. JSON is plain text where quotes, colons, commas, and brackets carry meaning — one missing comma will cause an error, so copy the examples carefully.

---

### Step 1: Create the file

Create `mylang.json` and paste in this skeleton:

```json
{
    "poses": [],
    "terms": []
}
```

`poses` is where you declare your grammatical categories. `terms` is where your words go. That's the whole file — two lists.

---

### Step 2: Declare your parts of speech

Add noun and verb to `poses`:

```json
{
    "poses": [
        {"pos": "noun", "abbr": "n."},
        {"pos": "verb", "abbr": "v."}
    ],
    "terms": []
}
```

`pos` is the full name used internally; `abbr` is what prints in the output.

**Why declare them separately?** Because every sense you write on a word must reference a category that exists here. Perplexicon checks this when it loads your file and rejects anything inconsistent. You'll never end up with a word that references a part of speech you forgot to define.

> If you use a category in a word before declaring it here, you'll see:
> ```
> nit: undeclared POS 'adjective'
> ```
> Add `{"pos": "adjective", "abbr": "adj."}` to `poses` and run again.

---

### Step 3: Add your first word with one sense and one gloss

Now add *nit* as a verb meaning "to see":

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

A **sense** is one grammatical role of a word — here, *nit* as a verb. A **gloss** is one definition within that role — here, "to see". One word, one sense, one gloss.

Run it:

```
python cli.py mylang.json
```

You should see:

```
nit - (v.) 1. to see
```

If you do, everything is working. If not, check for a missing quote or comma.

> **Note:** `pos` appears in two places. In `poses` you are *declaring* a category. Inside a sense, you are *referencing* one. The string must match exactly — `"verb"` and `"Verb"` are not the same.

---

### Step 4: Add more glosses to the same sense

*nit* also means "to watch" and "to appear". Add them to the same `glosses` list:

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
python cli.py mylang.json
```

```
nit - (v.) 1. to see 2. to watch 3. to appear
```

The order you write the glosses is the order they print. The first is the primary meaning.

---

### Step 5: Give the word a second sense

*nit* is also a noun meaning "sight". Add a second sense — a second grammatical role — to the same word:

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
python cli.py mylang.json
```

```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
```

One word, two senses, four glosses total. A word can carry as many senses as your language needs, each with its own definitions.

> Every sense must have at least one gloss. If you accidentally leave one empty, you'll see:
> ```
> nit: sense needs ≥1 gloss
> ```

---

### Step 6: Add a second word

Add *writ* the same way:

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
python cli.py mylang.json
```

```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
writ - (v.) 1. to hear 2. to listen (n.) 1. hearing
```

Your lexicon now holds 2 words, 4 senses, and 5 glosses. That's the output from the top of this guide.

> If you write the same word twice by accident:
> ```
> Duplicate term 'nit'
> ```
> Remove one entry, or merge their senses into a single one.

---

## Part 2: Using the Command Line

Every command runs your lexicon through a simple pipeline:

```
filter  →  sort  →  format  →  output
```

The flags below are each a knob on one stage of that pipeline. You can combine any of them freely.

---

### Filter: search your lexicon

**By word** (`-q`, default behavior — matches any word containing your query):

```
python cli.py mylang.json -q nit
```
```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
```

**By definition** (`-m gloss` — searches inside glosses instead):

```
python cli.py mylang.json -q hear -m gloss
```
```
writ - (v.) 1. to hear 2. to listen (n.) 1. hearing
```

For all search modes, see [README.md#search-methods](README.md#search-methods).

---

### Sort: alphabetize the output

```
python cli.py mylang.json -s
```

Sorting and filtering work together — the filtered results are sorted.

---

### Format: change the output template

`-t` selects a template. Here is *nit* in three of them:

**`default`**
```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
```

**`multiline`**
```
nit:
  verb
    - to see
    - to watch
    - to appear
  noun
    - sight
```

**`webster`**
```
nit v.: 1. to see 2. to watch 3. to appear  n.: 1. sight
```

For the full list, see [README.md#templates](README.md#templates).

---

### Output: write to a file

`-o` sends the result to a file instead of the terminal:

```
python cli.py mylang.json -o output.txt
```

---

### Combining flags

All flags compose. Any stage of the pipeline can be set independently:

```
python cli.py mylang.json -s -t html -o dictionary.html
python cli.py mylang.json -q hear -m gloss -t latex -o results.tex
```

---

## Part 3: The Python API

The command line covers the common cases. For bulk operations, merging files from collaborators, or generating statistics, you can work with your lexicon directly in Python.

The same hierarchy you built in Part 1 — words, senses, glosses — is exactly what `load()` gives you back as Python objects. Everything else in the API is an operation on that structure.

```python
from perplexicon import load, save, merge, stats, find_synonyms
```

---

**Merge two lexicons.** Words that exist in both are combined by sense; novel words are added:

```python
combined = merge(load("dialect_a.json"), load("dialect_b.json"))
save(combined, "merged.json")
```

---

**Get statistics** — word count, sense count, gloss count, and more:

```python
s = stats(load("mylang.json"))
print(s.entries, s.senses, s.glosses)
# s.polysemous = number of words with more than one sense
```

This is the same count you tracked manually through Part 1: *nit* and *writ*, 4 senses, 5 glosses.

---

**Find accidental synonyms** — two different words mapped to the exact same definition:

```python
dupes = find_synonyms(load("mylang.json"))
# {"to see": [("nit", "verb"), ("vitar", "verb")]}
```

Useful once a lexicon grows large enough that duplicates are easy to miss.

---

## Quick Reference

**Minimum valid lexicon:**
```json
{
    "poses": [{"pos": "noun", "abbr": "n."}],
    "terms": [
        {"term": "kala", "senses": [{"pos": "noun", "glosses": ["fish"]}]}
    ]
}
```

**The hierarchy:**
```
Lexicon → Words → Senses → Glosses
```

**Common commands:**
```bash
python cli.py mylang.json                          # print all
python cli.py mylang.json -q nit                   # filter by word
python cli.py mylang.json -q hear -m gloss         # filter by definition
python cli.py mylang.json -s -t html -o out.html   # sort, format, and save
```

**Error quick-reference:**

| Message | Cause | Fix |
|---|---|---|
| `nit: undeclared POS 'adjective'` | Used a category not in `poses` | Add it to `poses` |
| `Duplicate term 'nit'` | Same word appears twice | Remove one or merge senses |
| `nit: sense needs ≥1 gloss` | A sense has an empty `glosses` list | Add at least one definition |
