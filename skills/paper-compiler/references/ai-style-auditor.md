# ai-style-auditor — 文体鑑識官（AI っぽさの検査と除去）

paper-compiler の **write（英語生成時の禁則）** と **audit（AI 文体ゲート：18項目監査と別枠の⚠️リスト）**、および research-proposer の英語テキスト（EN 版・英文アブスト）review から参照する。

**目的と立場**：LLM 支援執筆そのものは禁止しない。ただし ChatGPT 以降に急増した特定のスタイル語・定型句・構造パターンは、査読者・編集者に「AI の痕跡」として認識されつつあり、内容より先に文体で減点される。**痕跡を残さず、自分の言葉に直す**ことが規範。個別の文書・人物を「AI 執筆」と断定する用途には使わない（個別判定器は非ネイティブ英語話者を誤検知する偏りが既知）。

**エビデンス**：Kobak et al. 2025（*Sci. Adv.*、PubMed 1,500 万抄録：2024 年に LLM スタイル語が急増、≥10% が LLM 支援）／Liang et al. 2024（AI 会議論文で最大 17.5%）／Liang et al. 2023（検出器の非ネイティブ偏り）／**E1 実測（2026-08-31）**：TKDE・PVLDB・DMKD の 2023 年抄録で HIGH 語の出現が基準比 1.97 倍（3.7%→6.8%）。機械検査の実装：`scripts/paper-structure-analyzer/ai_markers.py`（公開リポジトリ）。

## 1. HIGH 語彙（検出したら原則置換。E1/Kobak の regex と同一セット）

| AI っぽい語 | 置換の指針 |
|---|---|
| delve (into) | examine / analyze / investigate |
| intricate / intricacies | complex / details（何が複雑かを名指しする） |
| meticulous(ly) | careful(ly) / rigorous(ly)、または手続きを具体的に書く |
| pivotal | key / central（または削って主張を直接書く） |
| realm / in the realm of | field / area / in |
| showcase | show / demonstrate / present |
| underscore | highlight / emphasize（または「重要だ」と言わず理由を書く） |
| commendable / noteworthy / invaluable | 評価語を削り、事実と数値で示す |
| multifaceted / nuanced / holistic | 面・ニュアンス・範囲を**列挙して**置き換える |
| groundbreaking / transformative / game-changing | 使用禁止。結果に語らせる |
| seamless(ly) | 統合の仕組みを具体語で |
| tapestry / testament / beacon / a testament to | 比喩ごと削除 |
| garner | obtain / receive |
| unveil | present / introduce |
| ever-evolving / rapidly evolving landscape | 何がどう変わったかを名指す |
| harness / leverage | use |
| foster | support / enable |
| elucidate / illuminate | explain / clarify |
| boast | have / provide |

## 2. 定型句（見つけたら削除または書き換え）

- "It is worth noting that …" → 文頭ごと削除して主文だけ残す
- "plays a pivotal/crucial role in …" → 役割の中身を動詞で書く
- "In today's fast-paced / ever-changing world …" → 削除（導入の水増し）
- "This underscores the importance of …" → 重要性を言わず、帰結を書く
- "In conclusion, … paves the way for …" → 結論は貢献の再掲＋数値＋限界
- "not only X but also Y" の頻用 → 1 原稿 1 回まで
- "a wide range of / a variety of" → 数を書くか具体例 2–3 個
- "comprehensive overview / framework" → 何を網羅するか列挙

## 3. 書き方の構造パターン（目視チェック）

| # | パターン | 対処 |
|---|---|---|
| P1 | **三点並列の乱発**（"X, Y, and Z" のリズムが毎文続く） | 列挙は本当に 3 つある時だけ。文型を変える |
| P2 | **段落頭の接続詞ローテーション**（Moreover / Furthermore / Additionally / Notably） | 接続詞を削っても通じるなら削る。論理接続は内容で示す |
| P3 | **数値なしの強調**（significantly enhance / greatly improve） | 必ず数値・効果量に置換（岡先生の「数字に意味を与える」原則） |
| P4 | **過剰ヘッジ×過剰主張の同居**（could potentially revolutionize） | 主張の強さをフェーズ（P1〜P4）に合わせて一段階に統一 |
| P5 | **均質な文長・段落長**（リズムがない） | 短文を混ぜる。1 段落 1 主張に割り直す |
| P6 | **新情報ゼロの総括文**（In summary, this comprehensive approach …） | 削除。結論には数値と限界を |
| P7 | **em-dash・セミコロンの過用**（英文） | 文を切る |
| P8 | **太字・Title Case 見出しの乱発** | 見出しは Heading スタイル規則に従う（強調は原則使わない） |

## 4. 検査手順（audit の「AI 文体ゲート」）

1. **機械スキャン**：§1 の HIGH 語を正規表現で全文走査し、出現箇所を行番号つきで列挙する。
2. **判定**：本文 1,000 語あたり HIGH 出現 **≥2 で ⚠️**（要修正リスト化）。§2 定型句が併発する場合は **HIGH ⚠️（最優先修正）**。0〜1 は ✅（自然な使用は許容——例：数学用語としての manifold 的な正当使用は除外判断してよい）。
3. **提案**：各出現箇所に**置換後の文の下書き**を必ず添える（❌/⚠️ に充足質問・下書きを添える本則に従う）。
4. **構造チェック**：§3 の P1〜P8 を目視で確認し、該当パターンに例文つきで指摘する。
5. **報告**：監査表の 18 項目の後に「AI 文体ゲート」小表（HIGH 件数／1k 語率／定型句件数／P1〜P8 該当）を付す。
6. **してはいけないこと**：著者の AI 利用を断定・詮索しない。日本語文書は参考チェックのみ（「〜を掘り下げる」「極めて重要な役割を果たす」「多面的な」「まさに〜の証左」等の直訳癖）。

## 5. write モードでの禁則（生成時）

- §1 の語・§2 の句を**生成しない**（paper-composer のレシピに優先する禁則語彙として扱う）。
- 強調は数値で行い、評価形容詞を使わない。結論段落に新しい飾り文を足さない。
- 7 文法（浦木）の「平易な統語・正確な語彙」と同じ方向であり、矛盾しない。
