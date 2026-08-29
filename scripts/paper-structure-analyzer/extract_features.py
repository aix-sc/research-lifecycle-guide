#!/usr/bin/env python3
from __future__ import annotations
"""extract_features.py — Step 3 of paper-structure-analyzer.

Compute title and abstract structural features per paper (pure-Python, offline).

Title features
  title_words / title_chars   length
  title_colon                 two-part "Name: description" title (1/0)
  title_question              contains '?' (field-dependent sign — see report §2)
  title_acronym               contains an all-caps word of length 2–6 (1/0)
  title_number                contains a digit (1/0)

Abstract features
  abs_words                   length in words
  abs_flesch                  Flesch Reading Ease (lower = harder; highly cited
                              abstracts tend to score LOWER — see report §3)
  move_purpose / move_method / move_result / move_conclusion
                              cue-word heuristics for Hyland's rhetorical moves
  has_quant_result            digits/%/p-values present in result-cue sentences

Usage:
  python extract_features.py --in data/works_enriched.jsonl --out data/features.jsonl
"""
import argparse
import json
import re

VOWELS = "aeiouy"

PURPOSE = re.compile(r"\b(we (propose|present|introduce|develop|investigate|study|examine)|"
                     r"this (paper|study|article|work) (proposes|presents|introduces|"
                     r"investigates|examines|aims)|the (aim|goal|objective|purpose))\b", re.I)
METHOD = re.compile(r"\b(method|approach|algorithm|framework|model|dataset|experiment|"
                    r"we (use|train|evaluate|conduct|apply|implement))\b", re.I)
RESULT = re.compile(r"\b(results? (show|demonstrate|indicate|reveal)|we (find|found|show|"
                    r"observe)|outperform|improv(e|es|ed|ement)|achiev(e|es|ed)|"
                    r"accuracy|significant)\b", re.I)
CONCL = re.compile(r"\b(conclu(de|sion)|implication|suggest(s|ing)? that|"
                   r"these findings|our findings)\b", re.I)
QUANT = re.compile(r"(\d+(\.\d+)?\s*%|\bp\s*[<=]\s*0?\.\d+|\d+(\.\d+)?[x×]\b|\b\d{1,3}(\.\d+)?\b)")

# --- Title generality vs. specificity (v2) -----------------------------------
# Hypothesis under test (report §2bis): shorter titles at top venues may be a
# proxy for GENERALIZED contributions, while longer titles elsewhere carry
# application-scoping phrases ("for X", "applied to Y", "a case study of Z",
# country/region names). These features let analyze.py test whether specificity
# markers (a) differ by tier and (b) mediate the title-length–tier association.
APPLICATION = re.compile(r"\b(applied to|applications? (of|in|to)|applying|"
                         r"a case (study|of)|case study|toward[s]?)\b", re.I)
FOR_PHRASE = re.compile(r"\bfor\b", re.I)
PREPOSITIONS = re.compile(r"\b(of|for|in|on|with|from|via|using|under|towards?)\b", re.I)
COUNTRIES = re.compile(
    r"\b(Afghanistan|Argentina|Australia|Austria|Bangladesh|Belgium|Brazil|Canada|"
    r"Chile|China|Colombia|Croatia|Czech|Denmark|Egypt|Ethiopia|Finland|France|"
    r"Germany|Ghana|Greece|Hungary|India|Indonesia|Iran|Iraq|Ireland|Israel|Italy|"
    r"Japan|Jordan|Kenya|Korea|Malaysia|Mexico|Morocco|Nepal|Netherlands|Nigeria|"
    r"Norway|Pakistan|Peru|Philippines|Poland|Portugal|Romania|Russia|Saudi Arabia|"
    r"Singapore|Slovenia|South Africa|Spain|Sri Lanka|Sweden|Switzerland|Taiwan|"
    r"Tanzania|Thailand|Turkey|Uganda|Ukraine|United Kingdom|United States|the UK|"
    r"the USA?|U\.S\.A?\.|Vietnam|Zimbabwe)\b")


def syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    n, prev = 0, False
    for ch in w:
        isv = ch in VOWELS
        if isv and not prev:
            n += 1
        prev = isv
    if w.endswith("e") and n > 1:
        n -= 1
    return max(n, 1)


def flesch(text: str) -> float | None:
    words = re.findall(r"[A-Za-z]+", text)
    sents = max(len(re.findall(r"[.!?]+", text)), 1)
    if len(words) < 10:
        return None
    syl = sum(syllables(w) for w in words)
    return round(206.835 - 1.015 * len(words) / sents - 84.6 * syl / len(words), 2)


def title_features(t: str) -> dict:
    words = t.split()
    n_words = max(len(words), 1)
    n_prep = len(PREPOSITIONS.findall(t))
    specific = int(bool(COUNTRIES.search(t))) or int(bool(APPLICATION.search(t)))
    return {
        "title_words": len(words),
        "title_chars": len(t),
        "title_colon": int(":" in t),
        "title_question": int("?" in t),
        "title_acronym": int(bool(re.search(r"\b[A-Z]{2,6}\b", t))),
        "title_number": int(bool(re.search(r"\d", t))),
        # generality vs. specificity (v2)
        "title_for": int(bool(FOR_PHRASE.search(t))),
        "title_application": int(bool(APPLICATION.search(t))),
        "title_country": int(bool(COUNTRIES.search(t))),
        "title_prep_count": n_prep,
        "title_prep_density": round(n_prep / n_words, 3),
        "title_specific": int(bool(specific)),
    }


def abstract_features(a: str) -> dict:
    feats = {
        "abs_words": len(a.split()),
        "abs_flesch": flesch(a),
        "move_purpose": int(bool(PURPOSE.search(a))),
        "move_method": int(bool(METHOD.search(a))),
        "move_result": int(bool(RESULT.search(a))),
        "move_conclusion": int(bool(CONCL.search(a))),
    }
    has_quant = 0
    for sent in re.split(r"(?<=[.!?])\s+", a):
        if RESULT.search(sent) and QUANT.search(sent):
            has_quant = 1
            break
    feats["has_quant_result"] = has_quant
    return feats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    n = 0
    with open(args.out, "w", encoding="utf-8") as out:
        for line in open(args.inp, encoding="utf-8"):
            rec = json.loads(line)
            rec.update(title_features(rec.get("title") or ""))
            if rec.get("abstract"):
                rec.update(abstract_features(rec["abstract"]))
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    print(f"features for {n} records → {args.out}")


if __name__ == "__main__":
    main()
