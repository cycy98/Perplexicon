from perplexicon import Category, Entry, Sense

# Test __post_init__ enforcement — these should ALL raise ValueError
tests = [
    ("empty category name", lambda: Category(name="", abbr="n.")),
    ("empty category abbr", lambda: Category(name="noun", abbr="")),
    ("empty glosses", lambda: Sense(cat=Category("noun", "n."), glosses=())),
    ("empty gloss string", lambda: Sense(cat=Category("noun", "n."), glosses=("",))),
    ("duplicate gloss", lambda: Sense(cat=Category("noun", "n."), glosses=("a", "a"))),
    (
        "empty entry term",
        lambda: Entry(term="", senses=(Sense(cat=Category("noun", "n."), glosses=("x",)),)),
    ),
    ("empty entry senses", lambda: Entry(term="x", senses=())),
    (
        "duplicate sense key",
        lambda: Entry(
            term="x",
            senses=(
                Sense(cat=Category("verb", "v."), glosses=("a",)),
                Sense(cat=Category("verb", "v."), glosses=("b",)),
            ),
        ),
    ),
]

for name, fn in tests:
    try:
        fn()
        print(f"  MISSED: {name}")
    except ValueError as e:
        print(f"  CAUGHT: {name} → {e}")

# Test that valid construction works
cat = Category("noun", "n.")
sense = Sense(cat=cat, glosses=("thing",))
entry = Entry(term="x", senses=(sense,))
print(f"  VALID:  Entry({entry.term!r}) with {len(entry.senses)} sense(s)")
