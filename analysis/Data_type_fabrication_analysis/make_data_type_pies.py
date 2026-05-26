#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RESULTS_ROOT = HERE / "data_type_analysis_results"
OUT_PNG = HERE / "vanilla_data_type_pies.png"
OUT_PDF = HERE / "vanilla_data_type_pies.pdf"

PIPELINES = ["codex", "claude"]
SYSTEMS = ["youra", "mlrbench", "ai_scientist_v2"]
SYSTEM_LABELS = {
    "youra": "YouRA",
    "mlrbench": "MLR-Agent",
    "ai_scientist_v2": "AI Sci. V2",
}
PIPELINE_LABELS = {
    "codex": "Codex pipeline (GPT-5.4)",
    "claude": "Claude pipeline (Opus 4.6)",
}

CATEGORIES = ["Real", "Synthetic", "Fabricated"]
COLORS = {
    "Real":       "#4daf4a",
    "Synthetic":  "#ffd92f",
    "Fabricated": "#e41a1c",
}


def count_data_types(folder: Path) -> Counter:
    counts = Counter({c: 0 for c in CATEGORIES})
    for jf in sorted(folder.glob("iclr2025_*_fabrication_analysis_data_type.json")):
        with jf.open(encoding="utf-8") as f:
            data = json.load(f)
        dt = data.get("data_type")
        if dt in counts:
            counts[dt] += 1
        else:
            print(f"[WARN] unexpected data_type={dt!r} in {jf.name}")
    return counts


def main() -> None:
    if not RESULTS_ROOT.is_dir():
        raise SystemExit(f"Results root not found: {RESULTS_ROOT}")

    grid = {}
    for pipeline in PIPELINES:
        for system in SYSTEMS:
            folder = RESULTS_ROOT / f"fabrication_analysis_{pipeline}_data_type_{system}"
            if not folder.is_dir():
                print(f"[SKIP] missing: {folder.name}")
                continue
            counts = count_data_types(folder)
            grid[(pipeline, system)] = counts
            print(f"  {pipeline:6s} | {system:16s} | "
                  f"R={counts['Real']:>2}  S={counts['Synthetic']:>2}  F={counts['Fabricated']:>2}")

    n_rows = len(PIPELINES)
    n_cols = len(SYSTEMS)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(3.6 * n_cols, 3.3 * n_rows))
    if n_rows == 1:
        axes = [axes]

    for r, pipeline in enumerate(PIPELINES):
        for c, system in enumerate(SYSTEMS):
            ax = axes[r][c]
            counts = grid.get((pipeline, system))
            if counts is None:
                ax.set_axis_off()
                continue
            sizes = [counts[k] for k in CATEGORIES]
            colors = [COLORS[k] for k in CATEGORIES]
            wedge_data = [(s, col) for s, col in zip(sizes, colors) if s > 0]
            if wedge_data:
                vals, cols = zip(*wedge_data)
                ax.pie(
                    vals,
                    colors=cols,
                    startangle=90,
                    counterclock=False,
                    wedgeprops={"width": 0.35, "edgecolor": "white", "linewidth": 1.5},
                )
            else:
                ax.set_axis_off()

            total = sum(sizes)
            real = counts["Real"]
            ax.text(0, 0,
                    f"{real}/{total}\nReal",
                    ha="center", va="center",
                    fontsize=14, fontweight="bold")

            if r == 0:
                ax.set_title(SYSTEM_LABELS[system], fontsize=13, fontweight="bold", pad=10)
            if c == 0:
                ax.text(-1.45, 0, PIPELINE_LABELS[pipeline],
                        rotation=90, ha="center", va="center",
                        fontsize=11)

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=COLORS[c], edgecolor="white") for c in CATEGORIES
    ]
    fig.legend(handles, CATEGORIES, loc="upper center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, 0.99), fontsize=12,
               title="Vanilla Data Type", title_fontsize=13,
               handletextpad=0.5, columnspacing=2.0)
    fig.subplots_adjust(left=0.06, right=0.99, top=0.85, bottom=0.03, wspace=0.10, hspace=0.18)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=200)
    fig.savefig(OUT_PDF, bbox_inches="tight")
    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
