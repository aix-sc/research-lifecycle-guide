#!/usr/bin/env python3
from __future__ import annotations
"""ai_markers.py — Step 8 of paper-structure-analyzer (offline).

Estimate the prevalence of LLM-ASSISTED WRITING in abstracts using the
"excess vocabulary" approach (Kobak et al. 2024/2025, Science Advances;
Liang et al. 2024): a small set of STYLE words became abruptly over-represented
after ChatGPT's release (Nov 2022) — delve, intricate, meticulous, realm,
pivotal, showcase, underscore, commendable, ...

Design principles (report §7bis):
  * POPULATION-LEVEL ONLY. Per-abstract "AI-written probability" is not
    scientifically defensible (detectors are unreliable at the individual level
    and biased against non-native English writers, Liang et al. 2023). This
    script therefore reports year- and tier-level aggregates; per-abstract hit
    counts are stored in the features file for research use but MUST NOT be
    used to label individual papers.
  * Two marker sets: HIGH (strongly LLM-associated style words, rare in
    pre-2023 CS writing) and BROAD (LLM-favored but common in CS: crucial,
    comprehensive, leverage, robust, ...). HIGH drives the estimate; BROAD is a
    sensitivity check.
  * Baseline = 2018–2022 (pre-LLM); post = 2023+ . Excess share = share of
    abstracts with >=1 HIGH marker in post minus the baseline share (a
    conservative lower bound on LLM-assisted abstracts, as in Kobak et al.).

Outputs (in --out-dir):
  ai_markers.md      year table, pre/post excess, tier comparison (post years)
  features file is rewritten with ai_high_hits / ai_broad_hits / ai_high_rate

Usage:
  python ai_markers.py --in data/features.jsonl --out-dir results/ [--post-from 2023]
"""
import argparse
import json
import os
import re
import statistics
from collections import defaultdict

from analyze import cliffs_delta, magnitude, mannwhitney_p

HIGH = [
    r"\bdelv(e|es|ed|ing)\b", r"\bintricac(y|ies)\b", r"\bintricate(ly)?\b",
    r"\bmeticulous(ly)?\b", r"\brealms?\b", r"\bpivotal\b",
    r"\bshowcas(e|es|ed|ing)\b", r"\bunderscor(e|es|ed|ing)\b", r"\bcommendable\b",
    r"\btapestry\b", r"\btestament\b", r"\bunveil(s|ed|ing)?\b", r"\bgarner(s|ed|ing)?\b",
    r"\bnuanced\b", r"\bmultifaceted\b", r"\bnoteworthy\b", r"\binvaluable\b",
    r"\bgroundbreaking\b", r"\bseamless(ly)?\b", r"\bit is worth noting\b",
    r"\bin the realm of\b", r"\ba testament to\b", r"\bever-evolving\b",
]
BROAD = [
    r"\bcrucial\b", r"\bcomprehensive(ly)?\b", r"\bnotably\b", r"\butili[sz](e|es|ed|ing)\b",
    r"\balign(s|ed|ing)?\b", r"\bleverag(e|es|ed|ing)\b", r"\brobust(ly|ness)?\b",
    r"\blandscape\b", r"\bfoster(s|ed|ing)?\b", r"\bharness(es|ed|ing)?\b",
    r"\bholistic\b", r"\btransformative\b", r"\belucidat(e|es|ed|ing)\b",
    r"\billuminat(e|es|ed|ing)\b", r"\bpotential\b", r"\bsignificantly\b",
    r"\benhanc(e|es|ed|ing)\b", r"\bvaluable insights?\b",
]
HIGH_RE = re.compile("|".join(HIGH), re.I)
BROAD_RE = re.compile("|".join(BROAD), re.I)


def score(abstract):
    words = max(len(abstract.split()), 1)
    h = len(HIGH_RE.findall(abstract))
    b = len(BROAD_RE.findall(abstract))
    return {"ai_high_hits": h, "ai_broad_hits": b,
            "ai_high_rate": round(1000 * h / words, 3),
            "ai_broad_rate": round(1000 * b / words, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out-dir", default="results")
    ap.add_argument("--post-from", type=int, default=2023)
    ap.add_argument("--pair", nargs=2, default=["T10", "B"])
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    hi, lo = args.pair

    recs = [json.loads(l) for l in open(args.inp, encoding="utf-8")]
    by_year = defaultdict(list)
    for r in recs:
        if r.get("abstract"):
            r.update(score(r["abstract"]))
            by_year[r["year"]].append(r)
    # rewrite features with the new columns
    with open(args.inp, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    def share(rs, key):
        return sum(1 for r in rs if r[key] > 0) / len(rs) if rs else 0.0

    md = os.path.join(args.out_dir, "ai_markers.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write("# LLM-assisted writing prevalence (excess style-vocabulary)\n\n")
        f.write("Population-level estimate only — do NOT use to label individual papers.\n\n")
        f.write("## By year\n\n| year | n | share ≥1 HIGH marker | HIGH per 1k words (mean) | share ≥1 BROAD | BROAD per 1k (mean) |\n|---|---|---|---|---|---|\n")
        pre, post = [], []
        for y in sorted(by_year):
            rs = by_year[y]
            (post if y >= args.post_from else pre).extend(rs)
            f.write(f"| {y} | {len(rs)} | {share(rs,'ai_high_hits'):.3f} "
                    f"| {statistics.mean(r['ai_high_rate'] for r in rs):.2f} "
                    f"| {share(rs,'ai_broad_hits'):.3f} "
                    f"| {statistics.mean(r['ai_broad_rate'] for r in rs):.2f} |\n")
        if pre and post:
            excess = share(post, "ai_high_hits") - share(pre, "ai_high_hits")
            pre_mean = statistics.mean(r["ai_high_rate"] for r in pre)
            ratio_txt = (f"{statistics.mean(r['ai_high_rate'] for r in post) / pre_mean:.2f}×"
                         if pre_mean > 0 else "n/a (pre baseline = 0)")
            f.write(f"\n**Excess (post ≥{args.post_from} vs pre):** share of abstracts with ≥1 HIGH marker "
                    f"{share(pre,'ai_high_hits'):.3f} → {share(post,'ai_high_hits'):.3f} "
                    f"(excess = **{excess:+.3f}**, i.e. a lower bound of ~{max(excess,0)*100:.1f}% "
                    f"LLM-assisted abstracts); HIGH-marker rate ratio post/pre = **{ratio_txt}**.\n")

        # tier comparison, post years only (composition-matched within year)
        f.write(f"\n## Tier comparison ({hi} vs {lo}), post years only\n\n")
        f.write(f"| feature | median {hi} | median {lo} | mean {hi} | mean {lo} | Cliff's δ | magnitude | p |\n|---|---|---|---|---|---|---|---|\n")
        for feat in ("ai_high_rate", "ai_broad_rate", "ai_high_hits"):
            x = [r[feat] for r in post if r.get("tier") == hi]
            y = [r[feat] for r in post if r.get("tier") == lo]
            if len(x) >= 8 and len(y) >= 8:
                d = cliffs_delta(x, y); p = mannwhitney_p(x, y)
                f.write(f"| {feat} | {statistics.median(x):.3g} | {statistics.median(y):.3g} "
                        f"| {statistics.mean(x):.3g} | {statistics.mean(y):.3g} | {d:.3f} | {magnitude(d)} "
                        f"| {p if p is None else round(p,5)} |\n")
        f.write(f"\nn(post) = {len(post)}; n({hi}) = {sum(1 for r in post if r.get('tier')==hi)}, "
                f"n({lo}) = {sum(1 for r in post if r.get('tier')==lo)}.\n")
        f.write("\n> Reading guide (report §7bis): the year table should show a step at the post-LLM "
                "boundary if LLM assistance is present; pre-2023 rates are the field's natural baseline. "
                "Extend years to 2024–2025 (tier labels excluded) for a cleaner post-LLM signal. "
                "Sources: Kobak et al. 2025 (Sci. Adv., doi:10.1126/sciadv.adt3813); "
                "Liang et al. 2024 (arXiv:2404.01268); Liang et al. 2023 (detector bias, arXiv:2304.02819).\n")
    print(f"→ {md}")


if __name__ == "__main__":
    main()
