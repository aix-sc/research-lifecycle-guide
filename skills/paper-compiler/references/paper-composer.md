# 論文フォーマット「箱テンプレート」（1〜5章フルセット／2章・3章はA/B切替）

**方針**：中身（具体的な研究内容）は書かず、「何を書く場所か」の注釈だけを置いた空の箱です。
**バージョン（2章・3章のみ切替）**：**A＝アーキテクチャ提案型**（概念→構成要素→主関数）、**B＝アルゴリズム型**（ステップ化されたパイプライン）。アブスト・1章・4章・5章・参考文献・文体申し送りは **A/B共通**。
**揺れの優先規則**：論文間でばらつく箇所は **P620（Time-axis Granularity Synthesizer）の書き方を優先**しています。
**章構成**：アブスト／1背景／2提案／3実現／4実験／5まとめ／参考文献 のフルセット。

---

## アブストラクト

**段落数の目安**：1段落（P620準拠で長め・高密度）。

```
【この段落に書くこと】

① 冒頭：分野を超えた一般命題で入る
   〈ここに、扱う現象の本質を一段高い抽象度で述べる一文〉
   ※技術詳細から入らない。

② 一般的な問題定義（定番スロット）
   〈対象領域に存在する課題・ギャップを、一般命題として抽象度高く述べる一文〉
   ※特定の内容（暗黙知の定量化など）には踏み込まず、問題の所在だけを一般論で置く。

③ 手法の固有名詞化と一文定義
   "we propose the 〈手法名を大文字始まりの固有名詞で〉"
   〈手法が何を実現するかを一文で〉

④ 手法の本質的特徴（複数のプロセスを列挙）
   "The essential feature ... is ... : 1) 〈…〉, 2) 〈…〉, ...（必要な数だけ）"

⑤ 貢献リスト（★P620優先でアブストにも置く）
   "Our contributions are summarized as follows: 1) 〈…〉, 2) 〈…〉"

⑥ 末尾：実験の一言予告
   "In our experiment, we ... to demonstrate the feasibility and
    effectiveness of our method in the field of 〈適用分野を列挙〉."
```

**Keywords**：セミコロン区切りで10〜15語程度。〈中核語（semantic computing, time-series 等）を固定し、その論文固有の分野語を足す〉。

---

## 1章　背景（Introduction）

**段落数の目安**：本文4〜6段落＋末尾に構成案内1段落。
**小見出し**：★P620優先で付ける（`1.1 Background` / `1.2 Organization of this Paper`）。

### 1.1 Background

```
【段落1｜重要性の宣言】
 〈扱う現象・活動がなぜ重要かを大きく述べる。一般論から入り、
   技術詳細には踏み込まない〉

【段落2｜背景研究への定型参照ブロック】
 〈自グループの基盤研究をまとめて引用する定型文を置く〉
 例形：our semantic computing methods [ ]
        are applied to 〈対象〉.
 ※引用番号のかたまりは常設。ここは箱なので中身の対象だけ差し替える。

【段落3〜4｜課題の掘り下げ（論理チェーン）】
 ① 対象となる現象の定義
    〈本研究が扱う現象が何かを定義する一文〉
 → ② ①を簡単には分析できない現状の記述
    〈①がそのままでは容易に分析できない、という現状を述べる〉
 → ③ ②の理由（なぜ簡単には分析できないのか）の記述
    〈②が生じる根本的な理由を述べる〉
 → ④ だから〈手法名＝本研究で提案する技術〉が必要
    〈③を踏まえ、本提案が必要である、と接続する〉
 → ⑤ 〈手法名〉を構築すれば③が解消され分析が実現できる
    〈提案技術を構築することで③で述べた困難が解決され、①の分析が実現できる旨〉
 〈この順で各文を置く〉

【段落5｜本提案の予告と全体像】
 "In this paper, we present/propose 〈手法名〉..."（この書き出しはそのまま）
 2文目以降：アブスト④（本質的特徴＝複数プロセス）と⑤（貢献）の内容を、
   ここで丁寧に文章として展開する。
 続けて概念図を参照し、全体像を見せる：
 "The overall picture ... is illustrated in Figure 1."

【段落6｜関連研究の中での位置づけ】
 ① 他者の関連研究：2つの軸で比較する
    〈評価軸を2つ立て、他研究は多くとも一方の軸しか実現できないのに対し、
      本研究は両方の軸を同時に実現できる、という差分を述べる〉
 ② 自分の先行研究：それぞれの特徴を示す
    〈本提案の土台になった自分の先行研究を名指しし、各研究の特徴を述べる〉
```

### 1.2 Organization of this Paper

```
【構成案内（1段落）】
 節の道案内で章を閉じる：
 "Section 2 details the proposed model, Section 3 describes the
  implementation, Section 4 shows the experiments, and Section 5
  concludes the paper."
 ※本テンプレートは実現を独立章にするので、提案(2)と実現(3)を
   分けて案内する。
```

---

## 2章　提案方式（章題＝手法のフルネーム）

> **【バージョン切替】** この章と3章はA/Bで分岐する。論文が **アーキテクチャ提案型ならA**、**アルゴリズム（手続き）型ならB** を使う。アブスト・1章・4章・5章・参考文献・文体申し送りはA/B共通。
> **章題の付け方（A/B共通）**：`2. 〈手法のフルネーム〉`。アブスト・1章と一字一句同じ固有名詞を再掲。

### ▼ バージョンA：アーキテクチャ提案

**段落数の目安**：章冒頭に導入1段落＋小節（2.1／2.2…）。

```
【章冒頭｜導入段落】
 "In this paper, we propose a model to realize 〈手法名〉.
  In the following section, we present the details of the new
  conceptual model and system architecture."
 〈1章の課題（①現象の定義／②分析できない現状／③その理由）を、
   ほぼ同じ言い回しで一度反復してから入る〉
```

### 2.1 〈上位概念名〉（コンセプトの提示）

```
【この節に書くこと】
 〈手法の基礎となる上位概念を定義する。まだ実装の数式には入らない〉
 ・概念が何を実現するアーキテクチャかを1〜2文で宣言
 ・全体像のOverview図を1枚参照（"as shown in Figure 2."）
```

### 2.2 〈手法アーキテクチャ名〉（全体像と構成要素の宣言）

```
【この節に書くこと：★この著者の核となる型「N要素/M関数への分解」】
 手法を構成要素に分解して列挙する。
 ・手法を特徴づけるプロセス（適応の種類）を列挙する：
   "The essential feature ... is ... following the types of processes:
    1) 〈プロセス1〉, 2) 〈プロセス2〉, ...（必要な数だけ）"
   ※プロセスの分け方（軸）と種類数は手法に応じて決める。
     （P620の「縦方向/横方向の適応」はその一例にすぎない）
 ・その各プロセスに対応する Primitive Function を箇条書きで宣言
    - PF1: 〈名称〉（〈役割の一言〉）
    - PF2: 〈名称〉（〈役割の一言〉）
    - PF3: 〈名称〉（〈役割の一言〉）
    - PF4: 〈名称〉（〈役割の一言〉）
 ・構成要素の関係を示す図を参照（"As shown in Figure 3, ...")

【主関数の宣言（提案レベル）】
 個別要素を統合する写像を1つ提示：
   F_〈name〉: (入力) → (出力)
 記号の意味を "X = 〈…〉" で列挙。
 合成写像（∘）としての組み立て方針を一文で述べる
 （詳細な各関数の定義は次章＝3章 実現方式に回す）。
```

**この章の論理展開（固定・A）**：`上位概念を提示 → 全体像を語る → 構成要素をN個に分解して列挙 → 主関数で統合方針を示す（定義の詳細は3章へ送る）`

### ▼ バージョンB：アルゴリズム（ステップ化）

**段落数の目安**：章冒頭に導入1段落＋2.1 Overview（ステップ列）。

```
【章冒頭｜導入段落】
 "In this section, we define 〈手法名〉. First, we explain the overview
  of our method to process the 〈N〉 elements. Then we define the elements,
  and we also define input data, reference data, and output data."
 〈直前に1章の課題①②③（現象の定義／分析できない現状／その理由）を
   一度反復してから入る。ここはAと共通〉

【2.1 Overview（手法の全体像＝ステップ列）】
 "We realize our method by the following 〈K〉 steps to obtain 〈結果〉.
  Overview ... is shown in Figure 2."
 Step 1： 〈入力データ（文脈適用前の生データ）〉
 Step 2（核）： N個の要素の組み合わせで 〈定義したい対象〉 を定義する
    1) 〈要素1〉, 2) 〈要素2〉, ..., N) 〈要素N〉
 Step 3： Step2で定義した要素に従って 〈中間結果〉 を抽出/計算
 Step 4： 文脈に従って 〈最終結果〉 を出力
 ※ステップ数Kと各要素の中身は手法に応じて決める。
 ※「N個の要素の組み合わせで対象を定義する」がこの型の核。
 ※各要素・入出力データ構造・関数の詳細定義は3章 実現方式（B）へ送る。
```

**この章の論理展開（固定・B）**：`Overview（ステップ列）を提示 → Step2で「N要素の組み合わせ」を核として宣言 → 各要素・入出力データ・関数の定義はStepに対応させて3章へ送る`

---

## 3章　実現方式（Implementation / 各要素の定義）

**位置づけ**：★本テンプレート独自の分離章。2章後半にあった「各要素のデータ構造・数式・集約関数・具体例」をここに集約する。
**段落数の目安**：導入1段落＋「各要素＝1小節」の反復。
**A/B分岐**：3.1〜3.x の各要素定義（同型ブロック）は **A/B共通**。章の **閉じ方だけ** A/Bで分かれる（A＝統合データ構造で閉じる／B＝入出力データ構造＋関数で閉じる）。

```
【章冒頭｜導入段落（A/B共通）】
 "In this section, we present the implementation details of the
  〈primitive functions / elements〉 and data structures defined in the
  previous section."
 〈2章で列挙した要素を、ここで1つずつ実装レベルまで定義すると宣言。
   Aは Primitive Function、Bは Step2 の N要素を指す〉

【設計方針の一文（★この著者の癖）】
 各プロセスを分離する設計の意図を述べる：
 "One of the essential points of process design is to separate ...."
```

### 3.1 〈要素1〉の定義（例：PF1 の実装）

```
【同型ブロック（要素ごとに繰り返す定義フォーマット）】
 (a) 要素名＋略語を太字/小見出しで提示
     "Primitive function and data structure of PF1: 〈名称〉"
 (b) 役割を1〜2文で言語化
 (c) データ構造を数式で定義（右端に通し番号 (1)(2)... を付す）
     PF1: (入力) → (出力)
 (d) 記号説明を "X indicates ..." の列で縦に並べる
 (e) 付随する補助関数（集約関数など）を同じ形式で定義
 (f) "Example:" で具体例を1つ添える
 (g) 処理の詳細図を参照（"The process details ... is shown in Figure N."）
```

### 3.2 〈要素2〉の定義　…　### 3.x 〈要素n〉の定義

```
【上と同じ同型ブロックを要素の数だけ反復】
 ・数式には必ず通し番号を継続。
 ・記号説明は "◯ indicates △" 構文で統一。
 ・例示は second/minute/hour、phrase/sentence/section など
   「階層的な時間・言語・音楽」から取ると全体の語り口と揃う。
 ・オプション分岐がある要素は "option-1) ... option-2) ..." で明示。
```

### 3.x+1 章の閉じ方（★ここだけA/Bで分岐）

#### ▼ バージョンA：統合データ構造で閉じる

```
【この節に書くこと】
 各要素を束ねる階層構造／合成データ構造を1つ定義して章を閉じる：
 "Hierarchy_s = (〈…〉, 〈…〉, ...)"
 〈記号説明とExampleを添える〉
```

#### ▼ バージョンB：入出力データ構造＋関数で閉じる

```
【B-1｜入出力データ構造の定義】
 各要素の定義に続けて、手法の入力・（参照/中間）・出力データ構造を定義する：
 ・入力データ 〈記号：例 IRD / ITD〉：〈役割の一言〉。数式で定義（通し番号継続）。
 ・参照/中間データ 〈記号：例 CRD〉（ある場合のみ）：同形式で定義。
 ・出力データ 〈記号：例 OPD〉：〈役割の一言〉。同形式で定義。
 各記号は "◯ indicates △" で説明。成立条件がある場合は明示
 （"... might be possible when ..." の形）。

【B-2｜手法を統合する関数の定義】
 個別要素と入出力を束ねる写像を定義して章を閉じる：
 ・処理前半の関数（例：対象/参照データを決定する関数）
   f_〈name1〉: (要素群, 入力) → (中間データ, 〈…〉)   …(通し番号)
 ・処理後半の関数（例：最終結果を生成する関数）
   f_〈name2〉: (入力, 中間データ, 〈…〉) → (出力)      …(通し番号)
 〈2章-BのStepと関数を対応させる：Step2→要素群、Step3→前半関数、Step4→後半関数〉
```

---

## 4章　実験（Experiment(al) Study）

**章題**：★P620優先で `4. Implementation and experimental study` 系。
**段落数・構造**：Experiment 1 / Experiment 2（必要なら3）を並列。各実験が同型反復。

```
【章の入り｜評価目的の宣言（★P620の癖）】
 "We designed our implementation method to evaluate the feasibility
  of our system based on the following objective: whether the expected
  answers can be obtained."
 〈精度・誤差ではなく feasibility を評価軸に置くと最初に宣言〉
```

### Experiment 1:

```
【実験ブロックの内部フォーマット（実験ごとに反復）】

(1) 見出し："Experiment 1:"（番号付き）

(2) 目的の一文（定型）
    "The purpose of this experiment is to verify that, by utilizing
     the 〈switching〉 function (which is a key point of this proposal),
     it is possible to 〈…〉."

(3) 事例選定の理由＋専門家の暗黙知を1つ明文化
    〈なぜこのデータ/事例か。切替で結果差が出ることを確認できる理由〉
    〈例：ある曜日は検査所が閉まる／人口密度が切替速度に効く 等の
       field-specific な暗黙知を1つ言語化して差し込む〉

(4) 入力データと文脈設定を提示（★P620優先で「設定Table」中心）
    Table N：各 Primitive Function / 各要素に実際の値を割り当てた設定表
    〈要素の並び順を実験間で固定して比較可能にする〉

(5) 結果を図表で提示
    〈本文で "shown in Figure N / Table N" と先に予告 → 図表を置く〉
    ※図キャプションは長め・自立型（色/線種/読み方まで書き込む）

(6) 結果の言語的解釈
    〈同じ入力から、文脈を切り替えると異なる結果が出たことに着地〉
```

### Experiment 2:（必要なら Experiment 3:）

```
【Experiment 1 と同型のブロックを反復】
 ・(2)目的一文の "switching is a key point" リフレインを維持。
 ・(4)設定Tableの要素並びは Experiment 1 と揃える。
```

### Discussion for Experiments 1 and 2:

```
【★P620優先：実験横断の考察を独立見出しで置く】
 "By comparing ..." で実験横断の含意を述べ、以下の観点を箇条書き：
  ・feasibility（実現可能性）
  ・quantitative comparison between different contexts
  ・effectiveness for discussion（比較・議論の土台になる）
  ・applicability（他分野への適用可能性）
 ※この4点が「考察の定型スロット」。
```

---

## 5章　まとめ（Conclusion）

**段落数の目安**：2〜3段落＋Future work。
**構造の癖**：導入と高い対称性。新情報を入れず「約束の回収」に徹する。

```
【段落1｜提案の再宣言】
 "We have been advocating / We have presented 〈手法名〉..."
 〈アブストの定義文をほぼ流用して手法名を再掲〉

【段落2｜本質的特徴と貢献の再掲】
 "The essential feature ... is ...: 1) 〈…〉, 2) 〈…〉, ..."
 "Our contributions are summarized as follows: 1) 〈…〉, 2) 〈…〉"
 〈アブスト・1章と対応させて再列挙。新情報なし〉

【段落3｜実験の総括一文】
 "In our experiment, we performed an analysis by applying 〈分野〉 data
  to demonstrate the feasibility and effectiveness of our method."

【Future work（必ず置く）】
 "In our future work, we will 〈…〉, and we will extend our method and
  system to realize mutual understanding and knowledge sharing on
  global human-health issues in the world-wide scope."
 ※この "global human-health ... world-wide scope" 系の着地は定番オチ。
```

```
【謝辞（任意）】
 〈P620は謝辞なし。置く場合のみ Acknowledgement 見出しを追加〉
```

---

## 参考文献（References）

```
【構造の癖】
 ・前半 [1]〜[12] 付近：自己引用の常設リスト
   （5D World Map / Kansei / semantic computing 系）。ほぼ固定。
 ・後半 [13以降]：その論文固有の外部データ源・ツール
   （music21, ECDC, UK Government data 等）を足す。
【スタイル】番号 [n] 方式。著者名フル → タイトル → 誌名/会議 → 巻 → 頁 → 年。
```

---

## 文体・語尾・一人称の申し送り（箱を埋めるときの遵守事項）

```
・一人称は一貫して we / our（our method / our approach / our system /
  our contribution）。
・中心概念は大文字始まりの固有名詞にして "" で括り、各章で同じ表記を反復。
  用語を揺らさない。
・signature 動詞：propose / present / define / realize / express /
  switch(switching) / adapt / apply。特に realize と switch を効かせる。
・中心主張「文脈/スコープを switch すると同じ入力から違う結果が出る」を、
  アブスト・各実験・結論で意図的にリフレイン。
・数式の後は "X indicates ..." を縦に並べて記号説明。
・例示は「階層的な時間・言語・音楽」（second/min/hour,
  phrase/sentence/section）から取る。
・"Kansei" は英語論文でもローマ字のまま術語として使用。
・図表は本文で先に予告→提示。キャプションは長め・自立型。
・導入と結論は同一文を再利用できるほど対称に。
・綴り/三単現/冠詞は最終チェックで整える
  （過去に substruction=subtraction 等のゆれあり）。
```

---

## この分離構成での要注意点（P620優先ゆえの補足）

- 本テンプレートは、あなたが本来2章に融合させていた「実現方式」を **3章として独立**させています。したがって **2章は概念・全体像・要素宣言・主関数まで**にとどめ、**各要素の数式・集約関数・具体例・処理詳細図は3章に送る**、という切り分けを守ると破綻しません。
- 2章末の主関数と3章の各要素定義で **同じ記号系**を使うこと（2章で宣言→3章で実装、の対応を崩さない）。
- 1.2の構成案内も、提案(2)と実現(3)を **別章として案内**する文面にしてください（元の4章構成の案内文をそのまま流用すると章番号がずれます）。
