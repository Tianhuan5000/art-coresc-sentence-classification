import json
import os
import random
import sys
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

CORPUS_DIR = Path('data/ART_Corpus')
OUT_PATH = Path('sentences.jsonl')

def xml_to_sentences (xml_path: Path):
    "Parse an XML and return the dict of all sentences of the paper (excluding idx/n_in_paper)"
    annotator = xml_path.parent.name
    paper_id = xml_path.stem

    try:
        root = ET.parse(xml_path).getroot()

    except ET.ParseError as e:
        print(f"PARSE ERROR {xml_path}: {e}")
        return []

    region = None #title / abstract / body
    header = "" #the closest header
    out = []

    #traverse all elements, recording while it goes
    for el in root.iter():
        if el.tag == "TITLE":
            region = "title"
        elif el.tag == "ABSTRACT":
            region = "abstract"
        elif el.tag == "BODY":
            region = "body"
        elif el.tag == "HEADER":
            header = " ".join("".join(el.itertext()).split())
        elif el.tag == "s":
            #1. tagging the labels
            ann = el.find("annotationART")
            label = ann.get("type") if ann is not None else None

            #2. count the labels before taking the text (it will gone after take them)
            n_ref = sum(1 for _ in el.iter("REF"))
            n_xref = sum(1 for _ in el.iter("XREF"))
            n_sb = sum(1 for _ in el.iter("SB"))
            n_sp = sum(1 for _ in el.iter("SP"))

            #REF to CITATION
            for ref in el.iter("REF"):
                ref[:] = []
                ref.text = " CITATION "

            #iterate the text and glue them up
            text = " ".join("".join(el.itertext()).split())

            out.append({
                "paper": paper_id,
                "annotator": annotator,
                "region": region,
                "header": header,
                "text": text,
                "label": label,
                "n_ref": n_ref,
                "n_xref": n_xref,
                "n_sb": n_sb,
                "n_sp": n_sp,
            })
    #after reading each paper up, make up idx / n_in_paper
    n = len(out)
    for i, s in enumerate(out):
        s["idx"] = i
        s["n_in_paper"] = n
    return out

def sanity_check(records):
    n_papers = len({r["paper"] for r in records})
    print(f"number of paper: {n_papers}  (expected: 255)")
    print(f"number of sentence: {len(records)}  (expected: 34,680)")
    expected = {...}
    counts = Counter(r["label"] for r in records)
    for lab in sorted(counts, key=lambda x: -counts[x]):
        exp = expected.get(lab)
        flag = "" if exp in (None, counts[lab]) else f"  (expected: {exp})"
        print(f"  {lab:>4s}: {counts[lab]:>6d}{flag}")
    n_empty = sum(1 for r in records if not r["text"].strip())
    print(f"empty sentences: {n_empty}  (expected: 0)")
    random.seed(0)
    for r in random.sample(records, 3):
        print(" ", json.dumps(r, ensure_ascii=False))


def main():
    if not CORPUS_DIR.is_dir():
        raise SystemExit(f"ERROR {CORPUS_DIR} does not exist")

    xml_files = sorted(CORPUS_DIR.glob("ann*/*.xml"))
    print(f"Found {len(xml_files)} xml files")

    all_records = []
    for xml_path in xml_files:
        all_records.extend(xml_to_sentences(xml_path))

    with OUT_PATH.open("w", encoding= "utf-8") as f:
        for r in all_records:
            ordered = {
                "paper": r["paper"],
                "annotator": r["annotator"],
                "idx": r["idx"],
                "n_in_paper": r["n_in_paper"],
                "region": r["region"],
                "header": r["header"],
                "text": r["text"],
                "label": r["label"],
                "n_ref": r["n_ref"],
                "n_xref": r["n_xref"],
                "n_sb": r["n_sb"],
                "n_sp": r["n_sp"],
            }
            f.write(json.dumps(ordered, ensure_ascii=False) + "\n")

    #OG check
    print(f" write: {OUT_PATH} ({len(all_records)} line)")
    if "--check" in sys.argv or os.getenv("CHECK"):
        sanity_check(all_records)


if __name__ == "__main__":
    main()