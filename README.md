# PERPLEXICON

*Perplex*icon / Perp*lexicon*

A simple but capable system for making conlang lexicons. 

# What Makes it Special

The way Perplexicon will function is so easy that anyone could figure it out. Simply update a single JSON file with new words and you will immediately be able to export them to as many filetypes as you want. Perplexicon is built with languages where one word can function as multiple parts of speech and/or has different meanings in different contexts in mind, but that doesn't have to be the case -- Perplexicon works just as well with languages where there is one word for every meaning.


# List of Features:

- [x] Ability to specify more than one definition and part of speech for a word/term
- [x] Command line interface
    - [x] Opens lexicons
    - [x] Looks up certain definitions
    - [ ] Edits lexicons
    - [x] Outputs to file
- [ ] Graphical interface
- [x] Multiple styles for definitions
- [x] Abbreviations for parts of speech
- [ ] Alphabetizing lexicons
- [ ] IPA Support
- [ ] Clean Python code

# How It Works

Your lexicon lives in a single JSON file with two arrays: `poses` (your parts of speech and their abbreviations) and `terms` (your words, each with one or more senses and definitions). See [example.json](https://github.com/cycy98/Perplexicon/blob/master/examples/example.json) for a sample, or follow the [complete walkthrough in the guide](GUIDE.md).

## Command Line

Open up a command window in your working directory. Different parameters change what happens.

| You type: | What happens: |
|-----------|---------------|
| `python cli.py` | Error telling you that you need a lexicon file. |
| `python cli.py lexicon.json` | Prints every entry in lexicon.json. |
| `python cli.py lexicon.json -q uk` | Prints every entry in lexicon.json where the term contains "uk". |
| `python cli.py lexicon.json -q uk -m term` | Prints the entry in lexicon.json that the term is "uk" (See [Search Methods](#search-methods) below. |
| `python cli.py lexicon.json -t html` | Prints every entry in lexicon.json using template HTML (See [Templates](#templates) below. |
| `python cli.py lexicon.json -o output.txt` | Prints every entry in lexicon.json to the file output.txt |

## Search Methods

When searching for specific terms, there are different ways to get that information.

| Method | Explanation |
|--------|-------------|
| `term` | Returns the entry where the term *exactly* matches the query. |
| `term-part` | Returns any entry where the term contains the query (case-insensitive). **This is the default when `-q` is used without `-m`.** |
| `gloss` | Returns any entry where a gloss (definition) contains the query (case-insensitive). |
| `index` | Returns the entry at the specified position. |

## Templates

Perplexicon comes with several different templates from which to choose. These have no functional purpose, but they are useful when exporting to other filetypes.

| Template | Explanation |
|----------|-------------|
| `default` | Completely normal template. |
| `html` | Adds HTML tags to the default template. |
| `latex` | Uses same styling as `html`, but for LaTeX. |
| `multiline` | Prints each definition on a separate line. |
| `multiline-html` | Prints each definition on a separate line in HTML. |
| `webster` | Built to mimic the style Merriam-Webster uses for their dictionaries. |
| `webster-html` | Like `webster` but with HTML tags. |
# More
[Complete guide](GUIDE.md) — step-by-step walkthrough, error recovery, and Python API

[Discord server](https://discord.gg/Nkbzsrrebp)
