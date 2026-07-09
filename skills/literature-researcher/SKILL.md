---
name: literature-researcher
description: 研究開始時の「虎の巻」作成を担う調査スキル（探索・発見の担当者）。テーマ・キーワード・問い（What / Why / How）から web 検索で分野を探索し、①トップ研究者リスト（5〜10名：名前・所属・代表論文・Google Scholar / ORCID URL）、②研究トピック地図（論点3〜5軸と自分の研究の位置づけ）、③世界線ステートメント素案（「これが解けたら世界はこう変わる」）、④初期虎の巻（「7割・2020年以降」構成の候補文献リスト＋各1行メモ）を作成する。「トップ研究者を調べて」「虎の巻を作って」「この分野の地図がほしい」「先行研究を探して」「関連分野をサーベイして」「survey the field」といった依頼、または research-starter の Phase 04 から呼び出されたときに必ず使う。実在が確認できない研究者・文献は ⚠️ とする。候補リストの検証・平易な要約・URL確認は literature-reviewer に引き継ぐ（researcher＝探す／reviewer＝検証して整える）。Explore a research field at project start: identify 5–10 top researchers, map the topic axes, draft the "world-line" statement, and assemble an initial reference shortlist (70% post-2020), handing the candidates to literature-reviewer for verification and plain-language summaries.
---

# literature-researcher — 分野の探索と「虎の巻」の作成

## 役割と分業

| スキル | 担当 | 一言 |
|---|---|---|
| **literature-researcher（本スキル）** | 探索・発見 | 「誰が・何が・どこにあるか」を見つけて虎の巻の骨組みを作る |
| **literature-reviewer** | 検証・整形 | 候補リストを実在確認し、平易な要約と本文URLで仕上げる |

research-starter（Phase 04）→ **researcher（探索）** → **reviewer（検証）** → paper-compiler / research-proposer（Literature Review への挿入）というパイプラインの最上流を担う。

## 入力

- テーマ・キーワード（例：「時系列データの粒度変換」）
- 問い・仮説（research_start DOCX の Q5〜Q7 ／ Phase 02 の What・Why・How から引き継ぎ）
- 分野・対象年代・件数の目安（未指定なら確認は1回にまとめる）

## 実行手順

1. **分野の探索**：web 検索でサーベイ論文・代表的研究・主要研究室・主要 venue を特定する。検索は「テーマ英訳 + survey / review」「テーマ + top researchers / lab」等で多角的に行う。
2. **トップ研究者リスト（5〜10名）**：名前・所属・代表論文・Google Scholar / ORCID の URL を表にする。**実在を web で確認**し、確認できない場合は ⚠️。「顔・名前・所属を把握し Scholar でフォローする」ことをユーザーに促す。
3. **研究トピック地図**：分野を論点3〜5軸に整理し、**ユーザーの研究が地図のどこに位置するか**を1行で述べる（2軸ポジショニングの素材になる）。
4. **世界線ステートメント素案**：「これが解けたら世界はこう変わる」を1〜3案、具体的に描く。
5. **初期虎の巻**：候補文献15〜30本を「**7割・2020年以降**＋オーソリティ（古典）数本＋データ原典」の構成で挙げ、各1行メモ（何の文献か）を付す。arXiv は preprint と明記。詳細な要約・URL検証は行わない（literature-reviewer の担当）。
6. **構成レポート**：2020年以降の比率、⚠️ 件数、reviewer への引き継ぎ候補を報告する。

## 出力

- **research-starter 経由**：research_start DOCX の **Phase 04 欄**（トップ研究者表・虎の巻チェック）へ記入・更新する（docx スキルの手順・validate.py 検証）。
- **単独起動**：Markdown またはチャットで、①研究者表 ②トピック地図 ③世界線 ④候補文献リスト＋構成レポート を出力する。

## ハンドオフ（重要）

- 完成した候補文献リストは **literature-reviewer に渡す**ことを常に提案する（検証・中学生でもわかる要約・本文URL・⚠️出典不明の判定はそちらで行う）。
- 論文執筆段階では、検証済みリストが paper-compiler / research-proposer 経由で Literature Review（関連研究）セクションに挿入される。

## 禁止事項

1. **でっち上げ禁止**：研究者・文献・研究室の実在を web で確認する。確認できないものは必ず ⚠️（もっともらしい名前・書誌を創作しない）。
2. ⚠️ には「何を確認すべきか」を添える（指摘だけは禁止）。
3. 候補リストの段階で URL・DOI を確定情報として提示しない（未検証であることを明示し、検証は reviewer へ）。
