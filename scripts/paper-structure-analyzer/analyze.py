#!/usr/bin/env python3
from __future__ import annotations
"""analyze.py — Step 4 of paper-structure-analyzer.

Compare structural features across citation tiers (T1 / T10 / M / B) assigned
within venue-year cohorts, and emit a CSV plus a Markdown report shaped like
docs/PaperAnatomy_HighCitation_Patterns_JA.md §2–§5.

Statistics: Mann–Whitney U (normal approximation) + Cliff's delta effect size.
Interpret |δ|: <0.147 negligible, <0.33 small, <0.474 medium, else large.
Report effect sizes, not bare p-values (report §7).

Usage:
  python analyze.py --in data/features.jsonl --out-dir results/
  python analyze.py --in data/features.jsonl --out-dir results/ --pair T10 B
"""
import argparse
import csv
import json
import math
import os
import statistics
from collections import defaultdict

FEATURES = [
    "title_words", "title_chars", "title_colon", "title_question",
    "title_acronym", "title_number",
    "title_for", "title_application", "title_country",
    "title_prep_count", "title_prep_density", "title_specific",
    "abs_words", "abs_flesch", "move_purpose", "move_method",
    "move_result", "move_conclusion", "has_quant_result",
    "n_refs", "price_index", "ref_year_median", "ref_cites_median",
    "ref_span_years", "n_authors",
]

# Mediation check for the generality hypothesis (report §2bis): after the tier
# comparison, re-run the title_words comparison restricted to title_specific==0
# vs ==1 subgroups. If the tier gap in title_words shrinks materially within
# subgroups, specificity markers mediate the length–tier association.


def mannwhitney_p(x, y):
    """Two-sided Mann–Whitney U, normal approximation with tie correction."""
    n1, n2 = len(x), len(y)
    if n1 < 8 or n2 < 8:
        return None
    allv = sorted((v, 0) for v in x) + sorted((v, 1) for v in y)
    allv.sort(key=lambda t: t[0])
    ranks, i = {}, 0
    vals = [v for v, _ in allv]
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[i]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = r
        i = j + 1
    r1 = sum(ranks[k] for k, (_, g) in enumerate(allv) if g == 0)
    u1 = r1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    # tie correction
    tie_sum, i = 0, 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[i]:
            j += 1
        t = j - i + 1
        tie_sum += t ** 3 - t
        i = j + 1
    n = n1 + n2
    var = n1 * n2 / 12 * ((n + 1) - tie_sum / (n * (n - 1)))
    if var <= 0:
        return None
    z = (u1 - mu) / math.sqrt(var)
    return 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))


def cliffs_delta(x, y):
    """δ = P(x>y) - P(x<y); O(n log n) via sorting."""
    ys = sorted(y)
    import bisect
    gt = lt = 0
    for v in x:
        lt += bisect.bisect_left(ys, v)          # y-values strictly below v → x>y
        gt += len(ys) - bisect.bisect_right(ys, v)  # y-values strictly above v → x<y
    n = len(x) * len(ys)
    return (lt - gt) / n if n else 0.0


def magnitude(d):
    a = abs(d)
    return "negligible" if a < 0.147 else "small" if a < 0.33 else \
           "medium" if a < 0.474 else "large"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out-dir", default="results")
    ap.add_argument("--pair", nargs=2, default=["T10", "B"],
                    help="tiers to compare (default: T10 vs B)")
    args = ap.parse_args()
    hi, lo = args.pair
    os.makedirs(args.out_dir, exist_ok=True)

    by_tier = defaultdict(lambda: defaultdict(list))
    n_by_tier = defaultdict(int)
    # for the mediation check: title_words split by title_specific within tiers
    length_by_spec = defaultdict(lambda: defaultdict(list))  # [tier][0/1] -> words
    for line in open(args.inp, encoding="utf-8"):
        rec = json.loads(line)
        t = rec.get("tier")
        if t in ("T1", "T10", "M", "B"):
            n_by_tier[t] += 1
            for feat in FEATURES:
                v = rec.get(feat)
                if isinstance(v, (int, float)):
                    by_tier[t][feat].append(v)
            if isinstance(rec.get("title_specific"), int) and \
               isinstance(rec.get("title_words"), int):
                length_by_spec[t][rec["title_specific"]].append(rec["title_words"])

    rows = []
    for feat in FEATURES:
        x, y = by_tier[hi][feat], by_tier[lo][feat]
        if not x or not y:
            continue
        d = cliffs_delta(x, y)
        rows.append({
            "feature": feat,
            f"median_{hi}": round(statistics.median(x), 3),
            f"median_{lo}": round(statistics.median(y), 3),
            "cliffs_delta": round(d, 3),
            "magnitude": magnitude(d),
            "p_mannwhitney": (lambda p: round(p, 5) if p is not None else "")(
                mannwhitney_p(x, y)),
            f"n_{hi}": len(x), f"n_{lo}": len(y),
        })

    csv_path = os.path.join(args.out_dir, f"tiers_{hi}_vs_{lo}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    md_path = os.path.join(args.out_dir, f"tiers_{hi}_vs_{lo}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Stratified comparison: {hi} vs {lo}\n\n")
        f.write("Cohort sizes: " + ", ".join(
            f"{t}={n_by_tier[t]}" for t in ("T1", "T10", "M", "B")) + "\n\n")
        f.write(f"| feature | median {hi} | median {lo} | Cliff's δ | magnitude | p |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in sorted(rows, key=lambda r: -abs(r["cliffs_delta"])):
            f.write(f"| {r['feature']} | {r[f'median_{hi}']} | {r[f'median_{lo}']} "
                    f"| {r['cliffs_delta']} | {r['magnitude']} | {r['p_mannwhitney']} |\n")
        f.write("\n> Interpret with docs/PaperAnatomy_HighCitation_Patterns_JA.md §6: "
                "correlational, small effects expected; override the guide's defaults "
                "with these venue-measured values.\n")

        # --- Generality hypothesis (§2bis) -----------------------------------
        f.write(f"\n## Generality hypothesis: title length by specificity, {hi} vs {lo}\n\n")
        f.write("| subgroup | median words " + hi + " | median words " + lo +
                " | Cliff's δ | n |\n|---|---|---|---|---|\n")
        overall = cliffs_delta(by_tier[hi]["title_words"], by_tier[lo]["title_words"])
        f.write(f"| all titles | {statistics.median(by_tier[hi]['title_words']):.1f} "
                f"| {statistics.median(by_tier[lo]['title_words']):.1f} "
                f"| {overall:.3f} | {len(by_tier[hi]['title_words'])}/"
                f"{len(by_tier[lo]['title_words'])} |\n")
        for spec, label in ((0, "generic (no country/application marker)"),
                            (1, "specific (country / applied-to / case-study)")):
            x, y = length_by_spec[hi][spec], length_by_spec[lo][spec]
            if x and y:
                d = cliffs_delta(x, y)
                f.write(f"| {label} | {statistics.median(x):.1f} "
                        f"| {statistics.median(y):.1f} | {d:.3f} "
                        f"| {len(x)}/{len(y)} |\n")
        f.write("\n> If |δ| for title_words shrinks within the subgroups relative to "
                "'all titles', specificity markers mediate the length–tier gap "
                "(supporting the generality hypothesis); if it persists, length "
                "carries information beyond specificity.\n")
    print(f"wrote {csv_path} and {md_path}")


if __name__ == "__main__":
    main()
