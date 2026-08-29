#!/usr/bin/env python3
"""fetch_openalex.py — Step 1 of paper-structure-analyzer.

Fetch article metadata for a set of venues from OpenAlex (no API key needed)
and assign citation-percentile tiers WITHIN each venue x publication-year cohort.

Tiers (see docs/PaperAnatomy_HighCitation_Patterns_JA.md §1):
  T1  = top 1% by cited_by_count within venue-year
  T10 = top 10% (excluding T1)
  M   = 40th–60th percentile
  B   = bottom 25%
  (others get tier "-": kept in the file, excluded from comparisons)

Usage:
  python fetch_openalex.py --venues S4306420609 S137773608 \
      --years 2018-2023 --per-year 400 --email you@example.org \
      --out data/works.jsonl

Venue IDs are OpenAlex source IDs (S...). Find them at
https://api.openalex.org/sources?search=<journal name>.
Pass --email to enter OpenAlex's polite pool (faster, required courtesy).
Recent 2 years are excluded automatically (unstable citation windows).
"""
import argparse
import json
import sys
import time
import datetime
import urllib.parse
import urllib.request

API = "https://api.openalex.org/works"


def get(url: str, retries: int = 5) -> dict:
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 — retry on any transport error
            wait = 2 ** i
            print(f"  retry {i+1}/{retries} after {wait}s ({e})", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed after {retries} retries: {url}")


def fetch_cohort(venue: str, year: int, per_year: int, email: str):
    """Fetch up to per_year articles for one venue-year, sorted by citations desc."""
    works, cursor = [], "*"
    while cursor and len(works) < per_year:
        params = {
            "filter": (
                f"primary_location.source.id:{venue},"
                f"publication_year:{year},type:article"
            ),
            "sort": "cited_by_count:desc",
            "per-page": min(200, per_year - len(works)),
            "cursor": cursor,
            "select": (
                "id,doi,title,publication_year,cited_by_count,type,"
                "authorships,abstract_inverted_index,referenced_works,"
                "biblio,primary_location"
            ),
        }
        if email:
            params["mailto"] = email
        page = get(API + "?" + urllib.parse.urlencode(params))
        works.extend(page.get("results", []))
        cursor = page.get("meta", {}).get("next_cursor")
        time.sleep(0.2)
    return works


def tier_of(rank: int, n: int) -> str:
    """rank: 0-based position in citation-descending order within the cohort."""
    pct = (rank + 0.5) / n  # 0 = most cited
    if pct <= 0.01:
        return "T1"
    if pct <= 0.10:
        return "T10"
    if 0.40 <= pct <= 0.60:
        return "M"
    if pct >= 0.75:
        return "B"
    return "-"


def abstract_text(inv: dict | None) -> str:
    """Rebuild plain-text abstract from OpenAlex inverted index."""
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--venues", nargs="+", required=True, help="OpenAlex source IDs (S...)")
    ap.add_argument("--years", required=True, help="e.g. 2018-2023")
    ap.add_argument("--per-year", type=int, default=400)
    ap.add_argument("--email", default="", help="polite-pool email")
    ap.add_argument("--out", default="data/works.jsonl")
    args = ap.parse_args()

    y0, y1 = (int(x) for x in args.years.split("-"))
    this_year = datetime.date.today().year
    years = [y for y in range(y0, y1 + 1) if y <= this_year - 2]
    if not years:
        sys.exit("all requested years fall inside the excluded 2-year window")

    import os
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    n_out = 0
    with open(args.out, "w", encoding="utf-8") as f:
        for venue in args.venues:
            for year in years:
                cohort = fetch_cohort(venue, year, args.per_year, args.email)
                n = len(cohort)
                print(f"{venue} {year}: {n} works")
                for rank, w in enumerate(cohort):
                    auths = w.get("authorships") or []
                    rec = {
                        "id": w["id"],
                        "doi": w.get("doi"),
                        "venue": venue,
                        "venue_name": (w.get("primary_location") or {})
                        .get("source", {})
                        .get("display_name"),
                        "year": year,
                        "tier": tier_of(rank, n),
                        "cited_by_count": w.get("cited_by_count", 0),
                        "title": w.get("title") or "",
                        "abstract": abstract_text(w.get("abstract_inverted_index")),
                        "n_authors": len(auths),
                        "first_author_id": (auths[0].get("author", {}) or {}).get("id")
                        if auths else None,
                        "last_author_id": (auths[-1].get("author", {}) or {}).get("id")
                        if auths else None,
                        "referenced_works": w.get("referenced_works") or [],
                        "first_page": (w.get("biblio") or {}).get("first_page"),
                        "last_page": (w.get("biblio") or {}).get("last_page"),
                    }
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    n_out += 1
    print(f"wrote {n_out} records → {args.out}")


if __name__ == "__main__":
    main()
