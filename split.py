import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.model_selection import train_test_split

SENT_PATH  = Path("sentences.jsonl")
SPLIT_PATH = Path("split.json")

N_TEST = 36
N_DEV  = 36
SEED   = 42
ORDER = ["train","dev","test"]

def load_paper_to_annotator():
    "scan sentences,jsonl, return paper_id:annotator"
    paper_to_ann = {}
    with SENT_PATH.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            paper_to_ann[r["paper"]] = r["annotator"]
    return paper_to_ann


def make_split(paper_to_ann):
    "return {'train': [...], 'dev': [...], 'test': [...]} of paper IDs"
    papers = list(paper_to_ann.keys())
    annots = [paper_to_ann[p] for p in papers]

    #slice out the test
    train_dev, test = train_test_split(papers, test_size=N_TEST, stratify=annots, random_state=SEED,)
    #slice out dev
    remaining_annots=[paper_to_ann[p] for p in train_dev]
    train, dev = train_test_split(train_dev, test_size=N_DEV, stratify=remaining_annots, random_state=SEED,)

    split = {
        "train": sorted(train),
        "dev":   sorted(dev),
        "test":  sorted(test),
    }

    #check
    assert sum(len(v) for v in split.values()) == len(papers)
    assert len(set(train) & set(dev)) == 0
    assert len(set(train) & set(test)) == 0
    assert len(set(dev) & set(test)) == 0

    return split

def report(split, paper_to_ann):
    split_of_paper = {p: name for name, ids in split.items() for p in ids}

    ann_cnt = defaultdict(Counter)
    for p, name in split_of_paper.items():
        ann_cnt[name][paper_to_ann[p]] += 1

    sent_cnt = Counter()
    label_cnt = defaultdict(Counter)
    with SENT_PATH.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            name = split_of_paper[r["paper"]]
            sent_cnt[name] += 1
            label_cnt[name][r["label"]] += 1

    all_labels = sorted({lab for c in label_cnt.values() for lab in c})

    for name in ORDER:
        n_p = len(split[name])
        n_s = sent_cnt[name]
        print(f"\n=== {name.upper()} ===")
        print(f"papers: {n_p}   sentences: {n_s}")
        print(f"  annotators: {dict(sorted(ann_cnt[name].items()))}")
        print(f"  {'label':>4s}  {'count':>6s}  {'pct':>6s}")
        for lab in all_labels:
            c = label_cnt[name][lab]
            pct = 100.0 * c / n_s if n_s else 0.0
            print(f"  {lab:>4s}  {c:>6d}  {pct:5.1f}%")

    total_p = sum(len(v) for v in split.values())
    total_s = sum(sent_cnt.values())
    print(f"\ntotal: {total_p} papers / {total_s} sentences  (expected 225 / 34680)")


def main():
    paper_to_ann = load_paper_to_annotator()
    print(f"papers: {len(paper_to_ann)}")

    split = make_split(paper_to_ann)

    with SPLIT_PATH.open("w", encoding="utf-8") as f:
        json.dump(split, f, indent=2, ensure_ascii=False)
    print(f"wrote: {SPLIT_PATH}")

    if "--check" in sys.argv:
        report(split, paper_to_ann)

if __name__ == "__main__":
    main()