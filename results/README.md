# `results/` — Evaluation Outputs and Generated Research Artifacts

```text
results/
+-- evaluations/    # Judge scores over the generated papers
+-- generations/    # The generated research artifacts themselves
```

## `evaluations/` Layout

```text
results/evaluations/
+-- mlrbench_overall_score/
|   +-- youra/<backbone>/                 # Main-table lanes: sonnet45, opus45, sonnet46
|   +-- youra_ablation_study/<lane>/      # Component-ablation lanes (see below)
|   +-- ai_scientist_v2/<backbone>/
|   +-- mlragent/<backbone>/
+-- mlrbench_hallucination/
|   +-- youra/<lane>/ , ai_scientist_v2/... , mlragent/...
+-- mlrbench_idea_proposal_score/
    +-- YouRA/{idea,proposal}/ , MLRBench/{idea,proposal}/
```

Within a lane, each judge has one batch folder holding one JSON per task:

```text
<lane>/reviews_<judge>_..._with_code/iclr2025_<task>/review_<judge>.json
```

Each `review_<judge>.json` contains the five rubric scores (Clarity, Novelty,
Soundness, Significance, Overall — each `{score, strengths, weaknesses}`) plus a
1–5 confidence value. The four judges are `gpt-5.4`,
`gemini-3.1-pro-preview`, `grok-4.3`, and `claude-opus-4.6` throughout.

### Ablation Study (`mlrbench_overall_score/youra_ablation_study/`)

Overall-review scores for five YouRA component-ablation conditions, each with
4 judges × 10 tasks = 40 review JSONs:

| Lane | Ablated component |
|:--|:--|
| `sonnet45_no_VSA` | Persistence-versus-context control: no durable verification-state files; equivalent state passed through prompt-visible context. |
| `sonnet45_no_mcp` | MCP tool stack removed (Sonnet 4.5). |
| `sonnet45_no_reflection` | Reflection routing disabled (Sonnet 4.5). |
| `sonnet46_no_mcp` | MCP tool stack removed (Sonnet 4.6). |
| `sonnet46_no_reflection` | Reflection routing disabled (Sonnet 4.6). |

Per-lane mean/SD statistics can be regenerated with
[`../analysis/README.md`](../analysis/README.md#ablation-study-score-statistics)
(`analysis/MLRbench_scores_analysis/build_ablation_score_stats.py` and the
accompanying notebook).

## `generations/` Layout

Benchmark-generation artifacts are mirrored under
`results/generations/<system>/<lane>/iclr2025_<task>/`. For YouRA lanes each
task folder contains:

```text
iclr2025_<task>/
+-- docs/youra_research/<run>/    # Full research-pipeline trace (see below)
+-- experiments/                  # Flat copy of experiment code/logs/results
|                                 # (what the with-code judges read)
+-- .serena/                      # Orchestrator project memory
```

The per-run research trace follows the standard YouRA layout:

```text
docs/youra_research/<run>/
+-- 00_brainstorm_session.md
+-- 01_targeted_research.md
+-- 01_targeted_research_full.md
+-- 02_synthesis.yaml
+-- 02b_verification_plan.md
+-- 03_refinement.md
+-- 03_refinement.yaml
+-- verification_state.yaml
+-- <h-id>/                       # One folder per sub-hypothesis
|   +-- 02c_experiment_brief.md
|   +-- 03_prd.md
|   +-- 03_architecture.md
|   +-- 03_logic.md
|   +-- 03_config.md
|   +-- 04_validation.md
|   +-- 04_checkpoint.yaml
|   +-- code/
+-- 045_validated_hypothesis.md
+-- paper/
    +-- 06_paper.md
    +-- sections/
    +-- 06_references.bib
    +-- 06_paper_final.md
    +-- review/065_review_summary.md
    +-- refinement/
        +-- 06_paper_refinement.md        -> final refined manuscript
        +-- overleaf_refinement/main.pdf  -> compiled paper PDF, when available
```

**Final generated paper:** the final refined manuscript is
`06_paper_refinement.md` inside the run's `paper/refinement/` directory.
Example:

```text
results/generations/youra/sonnet45/iclr2025_buildingtrust/docs/youra_research/2026_buildingtrust/paper/refinement/06_paper_refinement.md
```

### YouRA Lanes

| Lane | Condition |
|:--|:--|
| `sonnet45`, `opus45`, `sonnet46` | Full system per backbone (main-table runs). |
| `sonnet45_no_VSA` | Persistence-versus-context control: the task model neither reads nor writes durable verification-state files; equivalent state is supplied as prompt-visible context, while harness-side shadow files (`.ablation_shadow/`) preserve identical stage transitions. |
| `sonnet45_no_mcp`, `sonnet46_no_mcp` | MCP tool stack removed. |
| `sonnet45_no_reflection`, `sonnet46_no_reflection` | Reflection routing disabled. |

### Anonymization Note

Local filesystem paths inside logs, configs, and pipeline documents have been
anonymized for release: the workspace root is rewritten to `/workspace` and the
home directory to `/home/anonymous`. LaTeX build byproducts and credential-style
files were removed; the remaining `.env.example` files contain placeholders
only.
