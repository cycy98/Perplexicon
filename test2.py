from perplexicon import load, merge, view, LexiconError
import json

# Test merge category conflict detection
a_path, b_path = "/tmp/a.json", "/tmp/b.json"
json.dump(
    {
        "poses": [{"pos": "noun", "abbr": "n."}],
        "terms": [{"term": "x", "senses": [{"pos": "noun", "glosses": ["thing"]}]}],
    },
    open(a_path, "w"),
)
json.dump(
    {
        "poses": [{"pos": "noun", "abbr": "N."}],
        "terms": [{"term": "y", "senses": [{"pos": "noun", "glosses": ["stuff"]}]}],
    },
    open(b_path, "w"),
)

a, b = load(a_path), load(b_path)
try:
    merge(a, b)
    print("MISSED: should have caught category conflict")
except LexiconError as e:
    print(f"CAUGHT: {e}")

# Test merge with compatible categories
json.dump(
    {
        "poses": [{"pos": "noun", "abbr": "n."}, {"pos": "verb", "abbr": "v."}],
        "terms": [
            {
                "term": "x",
                "senses": [
                    {"pos": "noun", "glosses": ["thing"]},
                    {"pos": "verb", "glosses": ["to do"]},
                ],
            }
        ],
    },
    open(a_path, "w"),
)
json.dump(
    {
        "poses": [{"pos": "noun", "abbr": "n."}],
        "terms": [
            {"term": "x", "senses": [{"pos": "noun", "glosses": ["object"]}]},
            {"term": "y", "senses": [{"pos": "noun", "glosses": ["idea"]}]},
        ],
    },
    open(b_path, "w"),
)

a, b = load(a_path), load(b_path)
m = merge(a, b)
print("MERGED:", view(m), end="")
