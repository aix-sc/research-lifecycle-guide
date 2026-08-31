#!/usr/bin/env python3
from __future__ import annotations
"""author_venues.py — Step 6 of paper-structure-analyzer (v3).

Author-level publication-VENUE STRATEGY analysis, stratified by citation tier.
For the first (or last) author of each tiered paper, fetch their recent works
from OpenAlex and characterize the venue portfolio:

  au_n_works           works in the lookback window (default 10 years)
  au_n_venues          unique publication venues
  au_venue_diversity   unique venues / works (1.0 = never repeats a venue)
  au_top_venue_share   share of works in the author's modal venue ("loyalty")
  au_journal_share     journal works / (journal + conference) works
  au_venue_h_median    median h-index of the venues published in (via /sources)
  au_venue_h_max       max venue h-index ("flagship reach")
  au_preprint_share    share of works with an arXiv/preprint location

analyze-style tier comparison (Mann–Whitney + Cliff's δ) between the first
authors of HI-tier vs LO-tier papers answers RQ4: do highly cited papers'
authors show identifiable venue strategies (flagship + rapid-venue mix,
loyalty vs. diversity, preprint use)?

Usage:
  python author_venues.py --in data/features.jsonl --out-dir results/ \
      --email you@example.org [--role first|last] [--years-back 10] [--pair T10 B]

Caveats: author disambiguation is OpenAlex's; effects are correlational and
confounded by seniority — au_n_works is reported so career length can be seen
alongside every comparison (report §5bis).
"""
import argparse
import json
import urllib.error
import sys
import os
import statistics
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

from analyze import cliffs_delta, magnitude, mannwhitney_p

WORKS_API = "https://api.openalex.org/works"
SOURCES_API = "https://api.openalex.org/sources"
PACE = [0.4]

def _headers():
    """OpenAlex auth (Feb-2026 policy): free key = 10x daily budget. Never hardcode."""
    h = {"User-Agent": "paper-structure-analyzer/1.2 (https://github.com/aix-sc/research-lifecycle-guide)"}
    k = os.environ.get("OPENALEX_KEY")
    if k:
        h["Authorization"] = "Bearer " + k
    return h


def _credits_exhausted(e):
    rem = e.headers.get("X-RateLimit-Remaining") if e.headers else None
    return rem is not None and str(rem).strip().lstrip("-").isdigit() and int(rem) <= 0



def get(url, retries=8):
    consecutive_429 = 0
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=_headers())
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                if _credits_exhausted(e):
                    print("❌ OpenAlex 日次クレジット枯渇（UTC 0:00 リセット）。OPENALEX_KEY を設定するか明日再実行。"
                          "チェックポイントは保存済み。", file=sys.stderr)
                    raise SystemExit(3)
                consecutive_429 += 1
                ra = e.headers.get("Retry-After") if e.headers else None
                server_wait = int(ra) if (ra and str(ra).isdigit()) else 0
                wait = min(120, server_wait) if server_wait else min(120, 15 * consecutive_429)
                wait = max(wait, 10)
                PACE[0] = min(3.0, PACE[0] + 0.4)
            else:
                consecutive_429 = 0
                wait = min(60, 2 ** i)
            print(f"  retry {i+1}/{retries} in {wait}s (HTTP {e.code}, pace={PACE[0]:.1f}s)",
                  file=sys.stderr)
            time.sleep(wait)
        except Exception as e:  # noqa: BLE001 — transport errors
            wait = min(60, 2 ** i)
            print(f"  retry {i+1}/{retries} in {wait}s ({e})", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(url)


def author_works(author_id, y0, y1, email, max_works=200):
    aid = author_id.rsplit("/", 1)[-1]
    works, cursor = [], "*"
    while cursor and len(works) < max_works:
        params = {
            "filter": f"authorships.author.id:{aid},"
                      f"publication_year:{y0}-{y1},type:article",
            "per-page": 100, "cursor": cursor,
            "select": "id,publication_year,primary_location,locations,type",
        }
        if email:
            params["mailto"] = email
        page = get(WORKS_API + "?" + urllib.parse.urlencode(params))
        works.extend(page.get("results", []))
        cursor = page.get("meta", {}).get("next_cursor")
        time.sleep(0.15)
    return works


def source_stats(source_ids, email, cache):
    todo = [s for s in source_ids if s and s not in cache]
    for k in range(0, len(todo), 50):
        chunk = "|".join(s.rsplit("/", 1)[-1] for s in todo[k:k + 50])
        params = {"filter": f"openalex_id:{chunk}", "per-page": 50,
                  "select": "id,summary_stats,type"}
        if email:
            params["mailto"] = email
        page = get(SOURCES_API + "?" + urllib.parse.urlencode(params))
        for src in page.get("results", []):
            cache[src["id"]] = {
                "h": (src.get("summary_stats") or {}).get("h_index"),
                "type": src.get("type"),
            }
        time.sleep(0.15)
    return cache


def portfolio(works, src_cache):
    venues, hs, journal, conf, preprint = [], [], 0, 0, 0
    for w in works:
        loc = w.get("primary_location") or {}
        src = (loc.get("source") or {})
        sid = src.get("id")
        if sid:
            venues.append(sid)
            info = src_cache.get(sid, {})
            if info.get("h") is not None:
                hs.append(info["h"])
            if info.get("type") == "journal":
                journal += 1
            elif info.get("type") == "conference":
                conf += 1
        for l in (w.get("locations") or []):
            s2 = (l.get("source") or {})
            if (s2.get("type") == "repository") or \
               "arxiv" in (s2.get("display_name") or "").lower():
                preprint += 1
                break
    n = len(works)
    if n == 0 or not venues:
        return None
    modal = Counter(venues).most_common(1)[0][1]
    feats = {
        "au_n_works": n,
        "au_n_venues": len(set(venues)),
        "au_venue_diversity": round(len(set(venues)) / len(venues), 3),
        "au_top_venue_share": round(modal / len(venues), 3),
        "au_preprint_share": round(preprint / n, 3),
    }
    if journal + conf:
        feats["au_journal_share"] = round(journal / (journal + conf), 3)
    if hs:
        feats["au_venue_h_median"] = statistics.median(hs)
        feats["au_venue_h_max"] = max(hs)
    return feats


AU_FEATURES = ["au_n_works", "au_n_venues", "au_venue_diversity",
               "au_top_venue_share", "au_journal_share",
               "au_venue_h_median", "au_venue_h_max", "au_preprint_share"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out-dir", default="results")
    ap.add_argument("--email", default="")
    ap.add_argument("--role", choices=["first", "last"], default="first")
    ap.add_argument("--years-back", type=int, default=10)
    ap.add_argument("--pair", nargs=2, default=["T10", "B"])
    ap.add_argument("--max-authors-per-tier", type=int, default=150)
    args = ap.parse_args()
    hi, lo = args.pair
    os.makedirs(args.out_dir, exist_ok=True)
    key = f"{args.role}_author_id"

    tier_authors = defaultdict(dict)  # tier -> {author_id: paper_year}
    for line in open(args.inp, encoding="utf-8"):
        rec = json.loads(line)
        aid = rec.get(key)
        if aid and rec.get("tier") in (hi, lo):
            tier_authors[rec["tier"]].setdefault(aid, rec["year"])

    src_cache, by_tier, rows = {}, defaultdict(lambda: defaultdict(list)), []
    for tier in (hi, lo):
        items = list(tier_authors[tier].items())[: args.max_authors_per_tier]
        for i, (aid, py) in enumerate(items):
            works = author_works(aid, py - args.years_back, py, args.email)
            sids = [((w.get("primary_location") or {}).get("source") or {})
                    .get("id") for w in works]
            source_stats(sids, args.email, src_cache)
            feats = portfolio(works, src_cache)
            if not feats:
                continue
            feats.update({"author_id": aid, "tier": tier})
            rows.append(feats)
            for f in AU_FEATURES:
                if isinstance(feats.get(f), (int, float)):
                    by_tier[tier][f].append(feats[f])
            if (i + 1) % 20 == 0:
                print(f"{tier}: {i+1}/{len(items)} authors")

    with open(os.path.join(args.out_dir, f"authors_{args.role}.jsonl"), "w",
              encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    md = os.path.join(args.out_dir, f"venue_strategy_{hi}_vs_{lo}.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(f"# Venue strategy of {args.role} authors: {hi} vs {lo} papers\n\n")
        f.write(f"Lookback: {args.years_back}y before the tiered paper. "
                f"n = {len(by_tier[hi].get('au_n_works', []))} / "
                f"{len(by_tier[lo].get('au_n_works', []))} authors.\n\n")
        f.write(f"| feature | median {hi} | median {lo} | Cliff's δ | magnitude | p |\n")
        f.write("|---|---|---|---|---|---|\n")
        for feat in AU_FEATURES:
            x, y = by_tier[hi][feat], by_tier[lo][feat]
            if not x or not y:
                continue
            d = cliffs_delta(x, y)
            pv = mannwhitney_p(x, y)
            f.write(f"| {feat} | {statistics.median(x):.3g} "
                    f"| {statistics.median(y):.3g} | {d:.3f} | {magnitude(d)} "
                    f"| {pv if pv is None else round(pv, 5)} |\n")
        f.write("\n> RQ4 reading guide: interpret au_venue_diversity / "
                "au_top_venue_share as diversity-vs-loyalty, au_venue_h_max as "
                "flagship reach, au_preprint_share as rapid-dissemination use. "
                "ALWAYS read alongside au_n_works (seniority confound) — "
                "report §5bis.\n")
    print(f"→ {md}")


if __name__ == "__main__":
    main()
