#!/usr/bin/env python3
"""Verify the data-provenance statistics quoted in the author responses.

Recounts, from the bundled per-task classification JSONs under
``data_type_analysis_results/``, the Sonnet 4.5 provenance numbers cited in
the discussion-period responses:

  * YouRA outputs classified as real-data-based: 8/10 under EACH of the two
    automated pipelines (Claude-backed and Codex-backed),
  * MLR-Agent: 1/10 under each pipeline,
  * AI Scientist V2: 4/10 (Claude pipeline) and 5/10 (Codex pipeline).

Pure standard library; runs from any working directory in a fresh clone:

    python analysis/Data_type_fabrication_analysis/verify_provenance_claims.py

Also writes the full PASS/FAIL report (no timestamps, so re-runs are
byte-identical) to a *_results.txt file next to this script.
Exit code 0 iff every check passes.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "data_type_analysis_results"

CLAIMS = {  # (pipeline, system) -> claimed Real count out of 10
    ("claude", "youra"): 8,
    ("claude", "mlrbench"): 1,        # mlrbench = MLR-Agent outputs
    ("claude", "ai_scientist_v2"): 4,
    ("codex", "youra"): 8,
    ("codex", "mlrbench"): 1,
    ("codex", "ai_scientist_v2"): 5,
}

PASS: list[str] = []
FAIL: list[str] = []
REPORT: list[str] = []


def check(name: str, got, want) -> None:
    ok = got == want
    (PASS if ok else FAIL).append(name)
    line = f"[{'PASS' if ok else 'FAIL'}] {name}: computed={got} claimed={want}"
    REPORT.append(line)
    print(line)


def main() -> int:
    for (pipeline, system), want in CLAIMS.items():
        d = RESULTS / f"fabrication_analysis_{pipeline}_data_type_{system}"
        files = sorted(d.glob("*.json"))
        check(f"{pipeline}/{system} task count", len(files), 10)
        real = sum(1 for f in files
                   if json.load(f.open()).get("data_type") == "Real")
        check(f"{pipeline}/{system} Real classifications", real, want)

    summary = f"{len(PASS)} passed, {len(FAIL)} failed."
    report_path = HERE / (Path(__file__).stem + "_results.txt")
    report_path.write_text("\n".join(REPORT + ["", summary]) + "\n", encoding="utf-8")
    print(f"\n{summary}")
    print(f"Report saved to {report_path.name}")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
