"""
features.py -- sentence-level feature extraction.

Public API
----------
featurize(rec, prev=None, next_=None, opts=None) -> dict[str, float]

    rec    : one record from sentences.jsonl (dict)
    prev   : the previous record in the SAME paper, or None
    next_  : the next record in the SAME paper, or None
    opts   : set/list of feature-group names to enable.
             None means DEFAULT_OPTS (currently: {"w"}).

Each feature is a string key -> float value. Features from different
groups live in disjoint namespaces via their prefix ("w=", "bi=", ...),
so a single flat dict is enough for DictVectorizer / torch.

Design note
-----------
Adding a new feature group later should require only:
  1. writing one function with signature (rec, prev, next_) -> dict
  2. registering it in FEATURE_GROUPS under its prefix name
No change to featurize() itself. Today only "w" (unigram) is wired.
"""

import json
import re
from pathlib import Path


SENT_PATH = Path("sentences.jsonl")


# ---------------------------------------------------------------- tokenizer
# One regex that handles the three things we care about today:
#   - words, including internal apostrophes ("don't", "film's")
#   - numbers, including a decimal part ("3.5", "2019")
#   - any other non-space char as its own token (punctuation)
# The step-1 output already has punctuation spaced out, but this works
# either way, so we don't depend on that property.
_TOKEN_RE = re.compile(r"[A-Za-z]+(?:['\u2019][A-Za-z]+)*|\d+(?:\.\d+)?|[^\s]")


def tokenize(text: str):
    """Return a lowercased token list for `text`."""
    return [t.lower() for t in _TOKEN_RE.findall(text)]


# ---------------------------------------------------------------- group: w
def feat_w(rec, prev, next_):
    """Unigram presence. 'the film .' -> {'w=the':1.0, 'w=film':1.0, 'w=.':1.0}

    Binary (presence), not term frequency: a word that appears twice still
    contributes 1.0. If we ever want tf instead, swap the assignment below
    for `feats[k] = feats.get(k, 0.0) + 1.0`.
    """
    feats = {}
    for tok in tokenize(rec["text"]):
        feats[f"w={tok}"] = 1.0
    return feats


# ---------------------------------------------------------------- registry
# Keys are the group names used in `opts`; values are group functions.
# Only implemented groups are listed here. Enabling an unregistered group
# raises a clear error in featurize() rather than silently doing nothing.
#
# Future groups, sketched for reference (each gets its own prefix):
#   "bi"    -> bigrams                  ("bi=the_film")
#   "reg"   -> region                    ("reg=body")
#   "sec"   -> header class              ("sec=intro" / "sec=methods" / ...)
#   "pos"   -> relative position, 1..10 ("pos=3")
#   "cite"  -> n_ref bucket             ("cite=0" / "cite=1" / "cite=2+")
#   "fig"   -> has xref                 ("fig=0" / "fig=1")
#   "chem"  -> sb/sp presence + shape   ("chem=sb", "chem=shape:Dw")
#   "hedge" -> hedge-cue hits           ("hedge=may")
#   "len"   -> sentence-length bucket   ("len=short" / "len=mid" / "len=long")
#   "ctx"   -> prev/next words          ("prev_w=the", "next_w=film")
FEATURE_GROUPS = {
    "w": feat_w,
}

DEFAULT_OPTS = frozenset({"w"})


# ---------------------------------------------------------------- entry point
def featurize(rec, prev=None, next_=None, opts=None):
    """Turn one sentence record into a feature dict.

    Parameters
    ----------
    rec    : dict, one line of sentences.jsonl
    prev   : dict or None, previous sentence in the same paper
    next_  : dict or None, next sentence in the same paper
    opts   : iterable of group names, or None for DEFAULT_OPTS

    Returns
    -------
    dict[str, float]
    """
    if opts is None:
        opts = DEFAULT_OPTS

    feats = {}
    for group in opts:
        fn = FEATURE_GROUPS.get(group)
        if fn is None:
            raise ValueError(
                f"unknown or not-yet-implemented feature group: {group!r}. "
                f"known groups: {sorted(FEATURE_GROUPS)}"
            )
        feats.update(fn(rec, prev, next_))
    return feats


# ---------------------------------------------------------------- smoke test
if __name__ == "__main__":
    import itertools

    if not SENT_PATH.exists():
        raise SystemExit(f"{SENT_PATH} not found -- run load_data.py first")

    with SENT_PATH.open(encoding="utf-8") as f:
        for line in itertools.islice(f, 3):
            rec = json.loads(line)
            feats = featurize(rec)
            print(f"\n--- {rec['paper']} #{rec['idx']}  label={rec['label']} ---")
            print("text:", rec["text"][:100])
            print("n_feats:", len(feats))
            # print first 15 features sorted, stable demo output
            for k in sorted(feats)[:15]:
                print(f"  {k:30s} {feats[k]}")