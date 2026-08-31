# Paper Anatomy — Structural Patterns of Highly Cited Papers (Evidence Synthesis)

**Research Lifecycle Guide supplement | v4 (2026-08-31)**
Skill delta: `paper-compiler/references/paper-anatomist.md` · Pipeline: `scripts/paper-structure-analyzer/`
Full version: [PaperAnatomy_HighCitation_Patterns_JA.md](PaperAnatomy_HighCitation_Patterns_JA.md) (Japanese)

## 0. Scope & caveat

What distinguishes highly cited papers from the rest at top venues, across title, abstract structure, section structure/labels, and reference lists? Two components: (a) a synthesis of large-scale bibliometric meta-research; (b) a reproducible OpenAlex-based pipeline to re-measure every claim on your own field. **Overriding caveat:** almost all associations are correlational with small effect sizes (r < ±0.2 in a 262-study meta-analysis); content, not form, drives citations. Do not game the form.

## 1. Stratification design

Citation distributions are skewed; use percentile tiers **within venue × publication-year cohorts**: T1 (top 1%), T10 (top 10% excl. T1), M (40–60%), B (bottom 25%). Minimum 3-year citation window; exclude the most recent 2 years.

## 2. Titles

Shorter titles dominate among highly cited papers at top venues (Letchford et al. 2015, τ≈−0.07; Bramoullé & Ductor 2018 with team controls) — but the sign flips at non-elite journals, where longer/more informative titles do better (Sienkiewicz & Altmann 2016). Colon-separated two-part titles help (Jacques & Sebire 2010; Buter & van Raan 2011). Question titles: negative in classic studies, **positive in CS** (+16%, Fiala et al. 2021) — field-dependent. Concrete method words (randomized, meta-analysis) over descriptive/region-bound words. **Guidance:** ≤10–14 words at top venues; `MethodName: what it enables`; check venue's recent accepted titles before question forms.

**Generality hypothesis (v2).** A candidate mechanism for the length flip: top-tier papers state generalized contributions tersely, while lower-tier titles grow through application-scoping phrases ("for X", "applied to Y", "a case study of Z", country names). Partially supported: country names in titles are a dramatic predictor of poor citation in medicine (over a third of poorly cited Lancet titles vs none of the well cited), geographic mentions reduce citations in OA journals (Paiva 2012), and Thelwall reads country-named titles' citation penalty as a specificity effect — though management journals show no such contextual effect (Nair & Gibbert 2016). No large-scale stratified test of the "for/applied-to" phrasing itself exists; the v2 pipeline adds six specificity features and a mediation check (does the tier gap in title length shrink within generic/specific subgroups?).

## 3. Abstracts

Hyland's 5 moves (Introduction–Purpose–Method–Product–Conclusion) mirror IMRaD; the Results/Product move is near-universal (~100%) in empirical fields — a missing quantitative result is the biggest red flag. Longer, move-complete abstracts tend to do better; use 85–100% of the venue's word limit. Counter-intuitively, *more readable abstracts are cited less* across large samples (Gazni 2011; Sienkiewicz & Altmann 2016; Ante 2022) — read as lexical density of expertise, not a license to obfuscate. The Uraki 7-sentence grammar fully covers the 5 moves: keep syntax plain, keep terminology dense and precise.

## 4. Section structure & labels

Label standardization is field-dependent: ≥92% IMRaD in cardiology vs. no standard structure in computational linguistics (79% Introduction, 59% Conclusion, 16% Discussion). CS/AI de-facto skeleton: Introduction → Related Work → *MethodName* → Experiments → Limitations → Conclusion, with the method's proper name as a heading. Reviews outcite research articles — control for document type.

## 5. Reference lists — is "70% within 5 years" right?

Reference count correlates positively with citations across many large studies. Highly cited papers cite longer, **more recent**, and more impactful reference lists (50,878-paper ecology study); the share of classics is harmless. Price index (share of references ≤5 years old) typically runs 0.27–0.52 by field, so **0.70 exceeds most field averages — read it as a prescriptive target for fast fields, not a descriptive fact**: papers with Price index ≥0.72 show the fastest citation take-off (10% of total citations in 1.66y vs 1.95y). Keep the current literature-reviewer rule: ~70% recent + a few authorities + data originals; targets Price ≥0.6 (ideal 0.7) for AI/CS, venue-measured +0.1 elsewhere.

## 5bis. Author venue strategy (v3)

Beyond single-paper form, v3 adds the AUTHOR's venue portfolio as a stratified object of analysis. Prior work covers venue-selection criteria and journal diversity of early-career researchers; general-audience journals carry a readership advantage (mirroring the generality hypothesis); and authors publishing mainly in low-impact venues concentrate in dense, inward-looking citation cliques — venue choice shapes citation ecology, not just exposure. Journal-level metrics must not proxy single-paper quality, so venue h-index is used only as a portfolio descriptor. New `author_venues.py` compares first authors of T10 vs B papers on venue diversity vs loyalty, journal/conference mix, median & max venue h-index (flagship reach), and preprint share — testing whether a "flagship journal × rapid venue × preprint" division is identifiable among highly cited papers' authors (RQ4/E6). Main confound: career length (`au_n_works` always reported alongside).

## E1. Pilot measurements (2026-08-31) — venue-measured override

**Data:** OpenAlex, TKDE / PVLDB / DMKD, 2018–2023, top-200 by citations per venue-year (DMKD: all 53–91) = 2,814 papers; tiers within venue-year: T1=30, **T10=252, M=564, B=705**. Mann–Whitney + Cliff's δ. **go/no-go: GO** (5 features with |δ|≥0.147).

- **Only reference-list features separate tiers:** Price index 0.571 vs 0.468 (δ=0.317), reference count 45.5 vs 37 (0.309), median citations of cited works 208 vs 146 (0.300), median reference year 2016 vs 2014.5 (0.237). The ecology-study pattern replicates fully in DS/DB; "70% within 5 years" is reached only in the upper half of T10 — the ≥0.6 / ideal 0.7 prescription holds.
- **Titles and abstracts are inert within a venue:** median title length 8 words in both tiers; colon/question/specificity markers, abstract length, readability (Flesch 23.2 vs 23.3) and move cues all negligible. Specific titles are nearly absent at top venues (243/252 and 690/705 generic), so the generality hypothesis operates *between* venue tiers, not within one. Venue norms homogenize abstracts.
- **Author venue strategy (RQ4) is null:** first authors of T10 vs B papers are indistinguishable on works, venue diversity, loyalty, venue h-index reach and preprint share.
- Author count 5 vs 4 (δ=0.19) — team-size confound, to be controlled in E2.
- **Takeaway:** once a paper is in a top venue, what it cites decides whether it gets cited; title and abstract are the entry ticket, not bonus points.

## 7bis. LLM-assisted writing (excess vocabulary, v4)

Following Kobak et al. (2025, *Sci. Adv.*) — population-level only, no per-paper labeling (individual detectors are unreliable and biased against non-native writers, Liang et al. 2023). Share of abstracts with ≥1 HIGH style marker (delve, intricate, pivotal, showcase, underscore, …): 3.7% baseline (2018–2022) → **6.8% in 2023 (+3.2 pt, 1.97×)**, a lower bound of ~3% LLM-assisted abstracts, consistent with the small 2023 step and 2024 surge seen in PubMed. The BROAD set (crucial, comprehensive, robust, …) already rose from 2021 and is unusable as evidence. No tier difference (δ=−0.025). Implementation: `ai_markers.py`; E2 adds 2024–2025.

## 6. What stratification newly reveals

(i) Form explains least at T1 (content/topicality dominate) — the coachable transition is B/M → T10. (ii) Some features flip sign between within-journal and between-journal comparisons — always stratify within venue-year. (iii) Readability paradox: no causal evidence for obfuscation; norm fixed as "dense terminology, plain syntax". (iv) Standard confounds: author count, internationality, OA, topicality — record author count & document type minimally. (v) Maintain the field-flip list and override guidance with venue measurements via the pipeline.

## 7–8. Pipeline & skill delta

See `scripts/paper-structure-analyzer/README.md` (fetch → enrich references → extract features → stratified analysis with Mann–Whitney + Cliff's δ; optional GROBID section labels). Skill delta in this version: new `paper-compiler/references/paper-anatomist.md` (T/A/S/R check items + field-flip list), registered in `paper-compiler/SKILL.md`.

## Key sources (verified URLs)

Letchford et al. 2015 (https://ncbi.nlm.nih.gov/pmc/articles/PMC4555861) · Sienkiewicz & Altmann 2016 (https://arxiv.org/pdf/1611.01935) · Bramoullé & Ductor 2018 (https://www.sciencedirect.com/science/article/abs/pii/S0167268118300143) · Kousha & Thelwall 2024 ARIST (https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24810) · Jacques & Sebire 2010 (https://pmc.ncbi.nlm.nih.gov/articles/PMC2984326/) · Reference-list features, Scientometrics 2020 (https://link.springer.com/article/10.1007/s11192-020-03759-0) · Knowledge recency & take-off (https://arxiv.org/pdf/1906.04206) · Top-1% analysis (https://arxiv.org/pdf/1804.10436) · Paper length meta-analysis 2019 (https://link.springer.com/article/10.1007/s11192-019-03015-0) · Ante 2022 (https://www.sciencedirect.com/science/article/pii/S1751157722000049) · Moves in abstracts, PLOS ONE 2018 (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0205417) · Multidisciplinary headings, J. Informetrics (https://www.sciencedirect.com/science/article/abs/pii/S1751157718304942)

## Update history

| v | Date | Change |
|---|---|---|
| v1 | 2026-07-23 | First release: evidence synthesis + stratified protocol + pipeline design + skill delta |
| v2 | 2026-07-23 | Added the title-generality hypothesis (§2bis-equivalent), six specificity features and a mediation check in the pipeline, two new sources |
| v3 | 2026-07-23 | Added author venue-strategy analysis (§5bis): author_venues.py compares first-author venue portfolios across tiers; fetch now records first/last author IDs |
| v4 | 2026-08-31 | Added E1 pilot measurements (2,814 papers, GO) overriding the guide's defaults, and §7bis LLM-assisted writing analysis (ai_markers.py) |
