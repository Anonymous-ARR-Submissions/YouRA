# MLR-Bench Hallucination Human Evaluation — Inter-rater Reliability (n=90)

Inter-rater reliability bundle for the human evaluation of AI-judge
hallucination flags. Three primary annotators (A/B/C) each labeled 90
non-overlapping flags as True (real hallucination) / False (false positive);
an anchor annotator then blindly re-judged a stratified 90-item overlap
(30 per primary annotator, collected in two batches). All annotators are
anonymous (Annotator A/B/C, Anchor).

Item ids of the form `results/evaluations/...#idx` are repository-root-relative
paths into `results/evaluations/mlrbench_hallucination/`. The analysis scripts
join labels by id only (they never open those files), and the evaluation GUIs
resolve the same ids against the repository root, so everything works directly
from a fresh clone of this repository.

## Key results
- On the 90-item overlap: agreement 69/90 = 76.7%, Cohen's kappa = 0.541
  (95% CI [0.37, 0.71], moderate)
- 18 of the 21 disagreements go in the single direction "primary True ->
  anchor False": the anchor applied a systematically stricter threshold
  rather than random label noise
- Per-system agreement: YouRA 26/30 (86.7%) > AI Scientist V2 22/30 >
  MLR-Agent 21/30
- Details: `reliability_report.docx`

## Files
[data]
- `labels_a/b/c_Annotator*.json` : the three primary annotators' True/False labels (90 each)
- `labels_d_anchor_1-30.json` / `labels_d1_anchor_31-90.json` : anchor re-evaluation (30 + 60 items)
- `selection_anchor_30.json` / `selection_anchor_60_batch2.json` : stratified-sampling manifests
- `selection_manifest*.csv` : CSV versions of the manifests
- `eval_gui_A/B/C.html` : the annotation GUIs shown to the primary annotators
  (also the inputs of the sampling scripts). Open them in a browser from inside
  the downloaded repository so the cross-check links to papers/code resolve.

[analysis code]  (Python 3; deps: scipy, python-docx)
- `reliability_analysis.py` : pairwise/pooled agreement + Cohen's kappa
- `report_stats.py` : full statistics for the report -> `report_stats.json`
- `build_reliability_report.py` : `report_stats.json` -> `reliability_report.docx`
- `_build_reliability_set*.py` : stratified overlap-sample builders
  (deterministic, fixed seed; also regenerate the blind anchor GUIs
  `eval_gui_D_anchor.html` / `eval_gui_D1_anchor.html`)

[results]
- `reliability_report.docx` : final report (n=90)
- `reliability_result.json` / `report_stats.json` : numeric outputs

## Reproduce
Run from this directory (`analysis/MLRbench_hallucination_human_eval/`):

    python reliability_analysis.py      # agreement / kappa (console + reliability_result.json)
    python report_stats.py              # full report statistics (report_stats.json)
    python build_reliability_report.py  # regenerate reliability_report.docx
