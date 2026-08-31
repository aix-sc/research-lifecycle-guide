#!/usr/bin/env python3
from __future__ import annotations
"""enrich_references.py — Step 2 of paper-structure-analyzer (v2: resumable).

Resolve referenced works' publication years and citation counts via the
OpenAlex batch filter endpoint, then attach per-paper reference-list features
(n_refs, price_index, ref_year_median, ref_cites_median, ref_span_years).

v2 hardening:
  * RESUMABLE — appends to --out, validates/truncates a possibly partial last
    line, and skips already-enriched records, so a crash never loses work.
  * Reference cache persisted to <out>.cache.json every 25 records.
  * 429-aware retries — honors Retry-After, waits up to 60s, 8 attempts.
  * Adaptive pacing — base 0.4s between calls, +0.2s after each 429 (cap 1.5s).

Usage (safe to re-run; it resumes automatically):
  python enrich_references.py --in data/works.jsonl --out data/works_enriched.jsonl \
      --email you@example.org
"""
import argparse
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.openalex.org/works"
BATCH = 50
PACE = [0.4]  # seconds between API calls; adapts upward on 429

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
        time.sleep(PACE[0])
    return cache


def valid_lines(path):
    """Return the list of JSON-parsable lines (drops a partial trailing line)."""
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        try:
            json.loads(line)
            out.append(line)
        except json.JSONDecodeError:
            print(f"  dropping partial line at position {len(out)} in {path}",
                  file=sys.stderr)
            break
    return out


def save_cache(path, cache):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({k: list(v) for k, v in cache.items()}, f)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--email", default="")
    args = ap.parse_args()
    records = [json.loads(l) for l in open(args.inp, encoding="utf-8")]

    done_lines = valid_lines(args.out)
    if done_lines:
        with open(args.out, "w", encoding="utf-8") as f:  # rewrite w/o partial tail
            f.write("\n".join(done_lines) + "\n")
        print(f"resume: {len(done_lines)}/{len(records)} already enriched — skipping")
    done = len(done_lines)

    cache_path = args.out + ".cache.json"
    cache = {}
    if os.path.exists(cache_path):
        try:
            cache = {k: tuple(v) for k, v in
                     json.load(open(cache_path, encoding="utf-8")).items()}
            print(f"resume: reference cache loaded ({len(cache)} works)")
        except Exception:  # noqa: BLE001 — corrupt cache is disposable
            cache = {}

    with open(args.out, "a", encoding="utf-8") as f:
        for i, rec in enumerate(records):
            if i < done:
                continue
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
            f.flush()
            if (i + 1) % 25 == 0:
                save_cache(cache_path, cache)
            if (i + 1) % 50 == 0:
                print(f"{i+1}/{len(records)} enriched (pace={PACE[0]:.1f}s)")
    save_cache(cache_path, cache)
    print(f"done → {args.out}")


if __name__ == "__main__":
    main()
