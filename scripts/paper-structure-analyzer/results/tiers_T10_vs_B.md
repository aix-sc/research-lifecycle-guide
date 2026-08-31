# Stratified comparison: T10 vs B

Cohort sizes: T1=30, T10=252, M=564, B=705

| feature | median T10 | median B | Cliff's δ | magnitude | p |
|---|---|---|---|---|---|
| price_index | 0.571 | 0.468 | 0.317 | small | 0.0 |
| n_refs | 45.5 | 37 | 0.309 | small | 0.0 |
| ref_cites_median | 208.0 | 146.0 | 0.3 | small | 0.0 |
| ref_year_median | 2016.0 | 2014.5 | 0.237 | small | 0.0 |
| n_authors | 5.0 | 4 | 0.192 | small | 0.0 |
| abs_words | 198.0 | 193 | 0.091 | negligible | 0.03817 |
| title_prep_density | 0.111 | 0.125 | -0.085 | negligible | 0.04048 |
| title_colon | 0.0 | 0 | 0.083 | negligible | 0.0063 |
| ref_span_years | 35 | 34.5 | 0.07 | negligible | 0.09979 |
| title_prep_count | 1.0 | 1 | -0.053 | negligible | 0.17421 |
| move_purpose | 1.0 | 1 | -0.041 | negligible | 0.19845 |
| move_method | 1.0 | 1 | -0.028 | negligible | 0.36415 |
| move_conclusion | 0.0 | 0 | 0.019 | negligible | 0.20332 |
| title_chars | 62.0 | 64 | -0.018 | negligible | 0.67305 |
| title_application | 0.0 | 0 | 0.016 | negligible | 0.15857 |
| has_quant_result | 0.0 | 0 | -0.016 | negligible | 0.55279 |
| title_question | 0.0 | 0 | 0.014 | negligible | 0.04562 |
| title_specific | 0.0 | 0 | 0.014 | negligible | 0.20861 |
| title_number | 0.0 | 0 | -0.013 | negligible | 0.12464 |
| title_for | 0.0 | 0 | 0.01 | negligible | 0.76266 |
| title_acronym | 0.0 | 0 | -0.004 | negligible | 0.86456 |
| move_result | 1.0 | 1 | 0.004 | negligible | 0.91916 |
| title_words | 8.0 | 8 | -0.001 | negligible | 0.9787 |
| title_country | 0.0 | 0 | -0.001 | negligible | 0.54993 |
| abs_flesch | 23.185 | 23.29 | -0.001 | negligible | 0.98144 |

> Interpret with docs/PaperAnatomy_HighCitation_Patterns_JA.md §6: correlational, small effects expected; override the guide's defaults with these venue-measured values.

## Generality hypothesis: title length by specificity, T10 vs B

| subgroup | median words T10 | median words B | Cliff's δ | n |
|---|---|---|---|---|
| all titles | 8.0 | 8.0 | -0.001 | 252/705 |
| generic (no country/application marker) | 8.0 | 8.0 | -0.009 | 243/690 |
| specific (country / applied-to / case-study) | 10.0 | 10.0 | -0.067 | 9/15 |

> If |δ| for title_words shrinks within the subgroups relative to 'all titles', specificity markers mediate the length–tier gap (supporting the generality hypothesis); if it persists, length carries information beyond specificity.
