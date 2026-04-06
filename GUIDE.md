# Perplexicon: A Complete Guide

Perplexicon is a tool for building dictionaries for invented languages. You keep your words in a text file and use the command line to view, search, and export them.

> **Requirement:** Python 3.13 or newer. Check with `python --version`. No other installs needed.

---

## What You're Working Towards

Before anything else, here's what Perplexicon produces. Given a two-word language, running:

```
python cli.py mylang.json
```

prints:

```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
writ - (v.) 1. to hear 2. to listen (n.) 1. hearing
```

Each line is one word. The abbreviation in parentheses is the part of speech. The numbered items are its definitions. *nit* has two grammatical roles — verb and noun — on the same line.

Everything in this guide is about producing that output, then doing more with it.

---

## Part 1: Building Your Lexicon File

Your lexicon is a single file written in JSON — a plain text format where quotes, colons, commas, and brackets all have meaning. A single missing comma will cause an error, so copy the examples carefully.

The file has exactly two sections: one for declaring your parts of speech, one for your words.

---

### Step 1: Create the empty file

Create a file called `mylang.json` and paste in this skeleton:

```json
{
    "poses": [],
    "terms": []
}
```

`poses` is where you declare your grammatical categories. `terms` is where your words go.

---

### Step 2: Declare your parts of speech

Our example language uses nouns and verbs. Add them to `poses`:

```json
{
    "poses": [
        {"pos": "noun", "abbr": "n."},
        {"pos": "verb", "abbr": "v."}
    ],
    "terms": []
}
```

Each entry has two fields: `pos` is the full name, `abbr` is what appears in the output. You can name them anything — `"pos": "adjective", "abbr": "adj."` works just as well.

> **Important:** Every part of speech you use on a word must be declared here first. Perplexicon will reject the file if a word references a category that doesn't exist in `poses`.

---

### Step 3: Add your first word

Now add *nit* with a single meaning:

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

A **sense** is one grammatical role of a word. A **gloss** is a definition within that sense.

Run it now:

```
python cli.py mylang.json
```

You should see:

```
nit - (v.) 1. to see
```

If you do, everything is working. If not, check for a missing quote or comma in the file.

> **Note on `pos` appearing twice:** In `poses` you are *declaring* a category. Inside a sense you are *referencing* one you already declared. The string must match exactly — `"verb"` and `"Verb"` are different.

---

### Step 4: Add more definitions

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

Run it:

```
python cli.py mylang.json
```

```
nit - (v.) 1. to see 2. to watch 3. to appear
```

The order you write the glosses is the order they print. The first one is the primary meaning.

---

### Step 5: Give a word two parts of speech

*nit* is also a noun meaning "sight". Add a second sense:

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

Run it:

```
python cli.py mylang.json
```

```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
```

One word, two senses. This is the core of Perplexicon — a word can carry as many grammatical roles as your language needs, each with its own set of definitions.

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

Run it:

```
python cli.py mylang.json
```

```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
writ - (v.) 1. to hear 2. to listen (n.) 1. hearing
```

That's the output from the top of this guide. Your lexicon is complete.

---

### When things go wrong

Perplexicon checks your file when it loads and gives a clear error if something is wrong. Here are the ones you're most likely to see:

**Right after Step 2** — if you use a part of speech in a word that isn't in `poses`:
```
nit: undeclared POS 'adjective'
```
Add `{"pos": "adjective", "abbr": "adj."}` to `poses`.

**Right after Step 6** — if you accidentally write the same word twice:
```
Duplicate term 'nit'
```
Remove one entry, or combine their senses into a single entry.

**Any time** — if a sense has no definitions at all:
```
nit: sense needs ≥1 gloss
```
Every sense must have at least one item in its `glosses` list.

---

## Part 2: Using the Command Line

All commands are run from the same folder as your `mylang.json` file.

### Print everything

```
python cli.py mylang.json
```

### Search by word

`-q` filters the output. By default it matches any word that *contains* your query:

```
python cli.py mylang.json -q nit
```
```
nit - (v.) 1. to see 2. to watch 3. to appear (n.) 1. sight
```

### Search by definition

Use `-m gloss` to search inside definitions instead:

```
python cli.py mylang.json -q hear -m gloss
```
```
writ - (v.) 1. to hear 2. to listen (n.) 1. hearing
```

For the full list of search modes, see the [README](README.md#search-methods).

### Sort alphabetically

```
python cli.py mylang.json -s
```

### Change the output format

`-t` switches the template. Here is *nit* rendered in three formats:

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

For the full list of templates, see the [README](README.md#templates).

### Save to a file

`-o` writes the output to a file instead of printing it:

```
python cli.py mylang.json -o output.txt
```

### Combining flags

All flags work together:

```
python cli.py mylang.json -s -t html -o dictionary.html
```

```
python cli.py mylang.json -q hear -m gloss -t latex -o results.tex
```

---

## Part 3: Going Further

Once your lexicon grows you may want to do more than the command line allows — bulk checks, merging files from collaborators, generating statistics. Everything is available as Python functions you can call directly from your own scripts.

```python
from perplexicon import load, save, merge, stats, find_synonyms
```

**Merge two lexicons.** Words that exist in both are combined automatically:
```python
combined = merge(load("dialect_a.json"), load("dialect_b.json"))
save(combined, "merged.json")
```

**Get statistics:**
```python
s = stats(load("mylang.json"))
print(s.entries, s.senses, s.glosses)
# s.polysemous = number of words with more than one sense
```

**Find accidental synonyms** — two different words with the exact same definition:
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

**Common commands:**
```bash
python cli.py mylang.json                         # print all
python cli.py mylang.json -q nit                  # search by word
python cli.py mylang.json -q hear -m gloss        # search by definition
python cli.py mylang.json -s -t html -o out.html  # sorted HTML export
```
