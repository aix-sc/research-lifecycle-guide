# paper-structure-analyzer

トップ venue の論文を **被引用パーセンタイル層（T1 / T10 / M / B、venue×年コホート内判定）** に分け、タイトル・アブストラクト・章構造・参考文献リストの構造特徴を層間比較する再現パイプライン。設計根拠と結果の読み方は [docs/PaperAnatomy_HighCitation_Patterns_JA.md](../../docs/PaperAnatomy_HighCitation_Patterns_JA.md)（EN: [`_EN`](../../docs/PaperAnatomy_HighCitation_Patterns_EN.md)）を参照。

A reproducible pipeline that stratifies papers from top venues into citation-percentile tiers (assigned **within venue × publication-year cohorts**) and compares structural features of titles, abstracts, section labels, and reference lists across tiers.

## Requirements

- Python 3.10+（標準ライブラリのみ / stdlib only — no pip installs needed）
- ネットワーク（OpenAlex API, キー不要 / no API key）
- （任意 / optional）GROBID server for Step 5: `docker run -p 8070:8070 lfoppiano/grobid`

## Pipeline

```bash
# 1. venue の OpenAlex source ID を調べる（例: ブラウザで）
#    https://api.openalex.org/sources?search=VLDB

# 2. 取得＋層ラベル付与（直近2年は自動除外）
python fetch_openalex.py --venues S4306420609 S137773608 \
    --years 2018-2023 --per-year 400 --email you@example.org --out data/works.jsonl

# 3. 参照リスト解決 → Price指数・参照先インパクト
python enrich_references.py --in data/works.jsonl --out data/works_enriched.jsonl \
    --email you@example.org

# 4. タイトル・アブスト特徴抽出（オフライン）
python extract_features.py --in data/works_enriched.jsonl --out data/features.jsonl

# 5. 層間比較（既定: T10 vs B。--pair T1 M なども可）
python analyze.py --in data/features.jsonl --out-dir results/
#    → results/tiers_T10_vs_B.csv / .md

# 6. 著者のvenue戦略（T10 vs B の筆頭著者ポートフォリオ比較）
python author_venues.py --in data/features.jsonl --out-dir results/ \
    --email you@example.org
#    → results/venue_strategy_T10_vs_B.md

# 7.（任意）OA本文PDFがある場合のみ: 章見出しラベル分布
python grobid_sections.py --pdf-dir pdfs/ --works data/features.jsonl \
    --out data/sections.jsonl
```

## Design decisions（要旨）

| 決定 | 根拠（レポート§） |
|---|---|
| 層は venue×年コホート内パーセンタイル | 引用分布の歪み・分野規範差（§1）；journal 内外で符号が反転する特徴があるため（§6-2） |
| 直近2年を除外 | 3年未満の引用窓は層判定が不安定（§1） |
| Mann–Whitney U ＋ Cliff's δ、p値単独解釈の禁止 | 歪んだ分布・小効果量が既知（§0, §6-1） |
| 著者数・document type を必ず記録 | 交絡の常連（§6-4） |
| Price 指数＝5年以内参照比率 | de Solla Price (1970) の標準定義（§5） |

## Outputs

- `results/tiers_<HI>_vs_<LO>.csv` — 全特徴の層別中央値・Cliff's δ・大きさ・p
- `results/tiers_<HI>_vs_<LO>.md` — レポート形式（ガイドの既定値を venue 実測で上書きするための表）
- `data/sections.jsonl` — IMRaD 適合・Related Work / Limitations 有無・固有名見出し数

## Ethics / terms

- OpenAlex メタデータは CC0。`--email` で polite pool を必ず使う（レート配慮）。
- 本文 PDF は **合法的に取得できる OA コピーのみ** を `pdfs/` に置く。
- 結果は相関であり、執筆指導の既定値更新に使う。難読化などのゲーミングには使わない（レポート§6-3）。

## Update history

| v | Date | Change |
|---|---|---|
| v1 | 2026-07-23 | 初版（fetch / enrich / extract / analyze / grobid の5ステップ） |
| v2 | 2026-07-23 | タイトル一般性・特定性特徴6種（for／application／country／前置詞密度 等）と、層×特定性の媒介チェックを analyze.py のレポートに追加 |
| v3 | 2026-07-23 | author_venues.py（著者venue戦略：多様性/ロイヤルティ・journal比・venue h-index・preprint率の層間比較）を追加。fetch_openalex.py が first/last author ID を記録 |
