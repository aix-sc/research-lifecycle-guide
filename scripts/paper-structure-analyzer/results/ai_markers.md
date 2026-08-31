# LLM-assisted writing prevalence (excess style-vocabulary)

Population-level estimate only — do NOT use to label individual papers.

## By year

| year | n | share ≥1 HIGH marker | HIGH per 1k words (mean) | share ≥1 BROAD | BROAD per 1k (mean) |
|---|---|---|---|---|---|
| 2018 | 411 | 0.041 | 0.25 | 0.477 | 3.67 |
| 2019 | 418 | 0.057 | 0.29 | 0.457 | 3.70 |
| 2020 | 419 | 0.017 | 0.11 | 0.465 | 3.50 |
| 2021 | 428 | 0.033 | 0.16 | 0.586 | 5.04 |
| 2022 | 446 | 0.036 | 0.19 | 0.547 | 4.79 |
| 2023 | 439 | 0.068 | 0.39 | 0.610 | 5.79 |

**Excess (post ≥2023 vs pre):** share of abstracts with ≥1 HIGH marker 0.037 → 0.068 (excess = **+0.032**, i.e. a lower bound of ~3.2% LLM-assisted abstracts); HIGH-marker rate ratio post/pre = **1.97×**.

## Tier comparison (T10 vs B), post years only

| feature | median T10 | median B | mean T10 | mean B | Cliff's δ | magnitude | p |
|---|---|---|---|---|---|---|---|
| ai_high_rate | 0 | 0 | 0.334 | 0.373 | -0.025 | negligible | 0.56974 |
| ai_broad_rate | 5.62 | 4.59 | 7.4 | 5.42 | 0.169 | small | 0.09328 |
| ai_high_hits | 0 | 0 | 0.0698 | 0.0727 | -0.025 | negligible | 0.58247 |

n(post) = 439; n(T10) = 43, n(B) = 110.

> Reading guide (report §7bis): the year table should show a step at the post-LLM boundary if LLM assistance is present; pre-2023 rates are the field's natural baseline. Extend years to 2024–2025 (tier labels excluded) for a cleaner post-LLM signal. Sources: Kobak et al. 2025 (Sci. Adv., doi:10.1126/sciadv.adt3813); Liang et al. 2024 (arXiv:2404.01268); Liang et al. 2023 (detector bias, arXiv:2304.02819).
