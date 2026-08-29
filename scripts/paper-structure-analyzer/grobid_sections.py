#!/usr/bin/env python3
"""grobid_sections.py — optional Step 5 of paper-structure-analyzer.

Extract section-heading labels from full-text PDFs via a local GROBID server
(https://github.com/kermitt2/grobid, `docker run -p 8070:8070 lfoppiano/grobid`),
then tabulate label distributions per citation tier (IMRaD-conformity, presence
of Related Work / Limitations, method-proper-name headings).

Usage:
  python grobid_sections.py --pdf-dir pdfs/ --works data/features.jsonl \
      --out data/sections.jsonl [--grobid http://localhost:8070]

PDF files must be named <openalex_id>.pdf (e.g. W2741809807.pdf). Only papers
with legally obtainable full texts (OA copies) should be placed in --pdf-dir.
"""
import argparse
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

TEI = "{http://www.tei-c.org/ns/1.0}"
STANDARD = {
    "introduction": "intro", "related work": "related", "background": "related",
    "method": "methods", "methods": "methods", "methodology": "methods",
    "experiment": "experiments", "experiments": "experiments", "evaluation":
    "experiments", "results": "results", "discussion": "discussion",
    "limitation": "limitations", "limitations": "limitations",
    "conclusion": "conclusion", "conclusions": "conclusion",
}


def grobid_tei(pdf_path: str, server: str) -> str:
    import mimetypes, uuid
    boundary = uuid.uuid4().hex
    with open(pdf_path, "rb") as f:
        pdf = f.read()
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"input\"; "
            f"filename=\"{os.path.basename(pdf_path)}\"\r\n"
            f"Content-Type: application/pdf\r\n\r\n").encode() + pdf + \
           f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        server.rstrip("/") + "/api/processFulltextDocument", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8", "replace")


def section_labels(tei_xml: str) -> list[str]:
    root = ET.fromstring(tei_xml)
    heads = []
    for div in root.iter(f"{TEI}div"):
        h = div.find(f"{TEI}head")
        if h is not None and h.text:
            heads.append(h.text.strip())
    return heads


def normalize(label: str) -> str:
    key = re.sub(r"^[\d.\s]+", "", label).strip().lower()
    for k, v in STANDARD.items():
        if key.startswith(k):
            return v
    return "other"  # typically a method proper-name heading


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", required=True)
    ap.add_argument("--works", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--grobid", default="http://localhost:8070")
    args = ap.parse_args()

    tiers = {json.loads(l)["id"].rsplit("/", 1)[-1]: json.loads(l)["tier"]
             for l in open(args.works, encoding="utf-8")}
    with open(args.out, "w", encoding="utf-8") as out:
        for fn in sorted(os.listdir(args.pdf_dir)):
            if not fn.endswith(".pdf"):
                continue
            wid = fn[:-4]
            try:
                heads = section_labels(grobid_tei(os.path.join(args.pdf_dir, fn),
                                                  args.grobid))
            except Exception as e:  # noqa: BLE001
                print(f"skip {fn}: {e}")
                continue
            norm = [normalize(h) for h in heads]
            out.write(json.dumps({
                "id": wid, "tier": tiers.get(wid, "-"), "headings": heads,
                "normalized": norm,
                "imrad_conform": int({"intro", "methods", "results",
                                      "discussion"} <= set(norm)),
                "has_related": int("related" in norm),
                "has_limitations": int("limitations" in norm),
                "n_proper_name_headings": norm.count("other"),
            }, ensure_ascii=False) + "\n")
    print(f"→ {args.out}")


if __name__ == "__main__":
    main()
