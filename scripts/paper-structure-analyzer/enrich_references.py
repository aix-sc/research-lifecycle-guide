#!/usr/bin/env python3
from __future__ import annotations
"""enrich_references.py — Step 2 of paper-structure-analyzer.

Resolve every referenced work's publication year and citation count via the
OpenAlex batch filter endpoint, then attach per-paper reference-list features:

  n_refs             number of resolvable references
  price_index        share of references published <= 5 years before the paper
  recency_share_5y   alias of price_index (kept for readability in reports)
  ref_year_median    median reference publication year
  ref_cites_median   median cited_by_count of the references (reference impact)
  ref_span_years     max - min reference year (temporal span; expected ~no effect)

Usage:
  python enrich_references.py --in data/works.jsonl --out data/works_enriched.jsonl \
      --email you@example.org
"""
import argparse
import json
import statistics
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.openalex.org/works"
BATCH = 50  # OpenAlex allows up to ~50 IDs per filter


def get(url: str, retries: int = 5) -> dict:
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            time.sleep(2 ** i)
            print(f"  retry {i+1} ({e})", file=sys.stderr)
    raise RuntimeError(url)


def resolve(ids, email, cache):
    todo = [i for i in ids if i not in cache]
    for k in range(0, len(todo), BATCH):
        chunk = todo[k : k + BATCH]
        short = "|".join(i.rsplit("/", 1)[-1] for i in chunk)
        params = {
            "filter": f"openalex_id:{short}",
            "per-page": BATCH,
            "select": "id,publication_year,cited_by_count",
        }
        if email:
            params["mailto"] = email
        page = get(API + "?" + urllib.parse.urlencode(params))
        for w in page.get("results", []):
            cache[w["id"]] = (w.get("publication_year"), w.get("cited_by_count", 0))
        time.sleep(0.2)
    return cache


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--email", default="")
    args = ap.parse_args()

    cache: dict[str, tuple] = {}
    records = [json.loads(l) for l in open(args.inp, encoding="utf-8")]

    with open(args.out, "w", encoding="utf-8") as f:
        for i, rec in enumerate(records):
            refs = rec.get("referenced_works") or []
            resolve(refs, args.email, cache)
            years = [cache[r][0] for r in refs if r in cache and cache[r][0]]
            cites = [cache[r][1] for r in refs if r in cache]
            py = rec["year"]
            if years:
                recent = sum(1 for y in years if py - y <= 5)
                rec["n_refs"] = len(years)
                rec["price_index"] = round(recent / len(years), 4)
                rec["recency_share_5y"] = rec["price_index"]
                rec["ref_year_median"] = statistics.median(years)
                rec["ref_span_years"] = max(years) - min(years)
            else:
                rec["n_refs"] = 0
            if cites:
                rec["ref_cites_median"] = statistics.median(cites)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if (i + 1) % 50 == 0:
                print(f"{i+1}/{len(records)} enriched")
    print(f"done → {args.out}")


if __name__ == "__main__":
    main()
