# Data: the ART Corpus (CoreSC annotation)

This folder contains the dataset used in this project, unchanged except that a
macOS `.DS_Store` file was removed.

## Source and license

- Dataset page: https://research.aber.ac.uk/en/datasets/the-art-corpus/
- DOI: 10.20391/f1c7c532-61fb-4914-8845-33463ff13105
- License: Creative Commons Attribution Non-Commercial 3.0 (CC BY-NC 3.0)

## Citations

- Liakata, M. and Soldatova, L. (2009). The ART Corpus. Technical report,
  Aberystwyth University. http://hdl.handle.net/2160/1979
- Liakata, M., Teufel, S., Siddharthan, A. and Batchelor, C. (2010). Corpora for
  the conceptualisation and zoning of scientific papers. In Proceedings of LREC 2010.
- Liakata, M., Saha, S., Dobnik, S., Batchelor, C. and Rebholz-Schuhmann, D. (2012).
  Automatic recognition of conceptualization zones in scientific articles and two
  life science applications. Bioinformatics 28(7), 991-1000.

## Contents

- `ART_Corpus/ann1` ... `ART_Corpus/ann9`: 225 papers in XML (a SciXML variant),
  25 per folder. Each folder holds the papers annotated by one of the 9 annotators.
  The papers are from Royal Society of Chemistry journals (physical chemistry and
  biochemistry).
- `Description_ART_Corpus.pdf`: the original corpus documentation.

## Format

Each sentence is an `<s sid="...">` element containing one `<annotationART>`
element. Its `type` attribute is the sentence's label (one of 11 Core Scientific
Concepts). Sentence text can contain inline markup such as `<REF>` (citations),
`<XREF>` (figure/table references), `<SB>` (subscripts), `<SP>` (superscripts)
and `<IT>` (italics).

## Statistics (as counted from these files)

225 papers, 34,680 sentences (titles and abstracts included).

| Code | Label        | Sentences |
|------|--------------|-----------|
| Res  | Result       | 7,373     |
| Bac  | Background   | 6,657     |
| Obs  | Observation  | 4,659     |
| Met  | Method       | 3,751     |
| Mod  | Model        | 3,456     |
| Con  | Conclusion   | 3,083     |
| Exp  | Experiment   | 2,841     |
| Obj  | Object       | 1,190     |
| Hyp  | Hypothesis   | 656       |
| Goa  | Goal         | 548       |
| Mot  | Motivation   | 466       |

Note: the corpus documentation reports 35,040 sentences; the released XML files
contain 34,680 annotated sentences, which is the number used in this project.
