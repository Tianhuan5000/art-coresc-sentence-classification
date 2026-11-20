# COSI 114a Final Project, Fall 2026
This project builds classifiers that read a single sentence from a research paper and
predict its **scientific role**: is the sentence giving background, stating a hypothesis,
describing an experiment, presenting a model, or reporting a result? A particular focus is
whether a classifier can tell **modeling** content apart from **experimental** content.
 
All models are scikit-learn classifiers trained on hand-designed features represented with
`DictVectorizer`.

## Task
| | |
|---|---|
| Instance | One sentence from a full research paper (title, abstract, or body) |
| Label | One of 11 Core Scientific Concepts (CoreSC) |
| Task type | Single-label multiclass classification |
| Main metric | Macro-F1 (accuracy also reported) |
 
| Code | Label | Meaning |
|---|---|---|
| Bac | Background | Accepted background knowledge and previous work |
| Mot | Motivation | Why the investigation is carried out |
| Goa | Goal | The target state the investigation aims to achieve |
| Obj | Object | The main entity or product of the investigation |
| Hyp | Hypothesis | A statement not yet confirmed, to be tested |
| Met | Method | The means used to achieve a goal |
| Exp | Experiment | Concrete experimental steps and conditions |
| Mod | Model | A theoretical model, computational framework, or equation |
| Obs | Observation | Data or phenomena directly observed |
| Res | Result | A factual statement about the outcome of the investigation |
| Con | Conclusion | A statement linking results to goals or hypotheses, or broader implications |

## Data
The **ART corpus** (Liakata & Soldatova, 2009): 225 papers from Royal Society of Chemistry
journals (physical chemistry and biochemistry), with 34,680 sentences annotated by chemistry
experts. The papers are split evenly among 9 annotators (25 papers each). See
[`data/README.md`](data/README.md) for source, license, format, and label counts.

### Split
 
- The split is made at the **paper level**: all sentences from a paper stay in the same split.
- `train_test_split` is applied to the list of paper IDs, **stratified by annotator**,
  giving 153 / 36 / 36 papers for train / dev / test (17 / 4 / 4 per annotator).
- The split is saved in `split.json` and reused for every experiment.
- Random seed: `TBD`
| Split | Papers | Sentences |
|---|---|---|
| Train | 153 | TBD |
| Dev | 36 | TBD |
| Test | 36 | TBD |

## Features
 
Each feature group uses its own prefix so that groups never collide.
 
| Prefix | Feature group |
|---|---|
| `w=` | Lowercased unigrams in the sentence |
| `bi=` | Bigrams in the sentence |
| `sec=` | Region (title / abstract / body) and normalized section heading |
| `pos=` | Relative position of the sentence in the paper (10 bins) |
| `cite=` | Number of citations (0 / 1 / 2+) |
| `fig=` | Whether the sentence references a figure or table |
| `chem=` | Subscript/superscript markup and word shapes of tokens with digits |
| `hedge=` | Hedging cues (e.g., *may*, *might*, *suggest*, *likely*) |
| `len=` | Sentence length bin |
| `prev_w=`, `next_w=` | Unigrams of the previous and next sentence |
