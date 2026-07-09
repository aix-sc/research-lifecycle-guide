# Research Lifecycle Guide — 研究ライフサイクル・スキル群

**はじめの一歩から論文投稿まで、研究の全工程を AI スキルで伴走する** ── Claude Skills・学習ガイド・v0テンプレートの統合リポジトリ。

Research lifecycle skills for Claude (and other LLMs): from a researcher's first steps (ORCID, research questions, branding) through proposal writing, paper drafting (IMRAD / Kiyoki-lineage "hako" template), literature research/verification, to an 18-item pre-submission audit. Japanese-first; English materials to follow in the same repository.

研究ライフサイクル：**01 はじめの一歩 → 02 研究開始 → 03 執筆型の決定 → 04 論文執筆 → 05 投稿前監査**

📖 **フルガイド（全内容・学習統合版）**：[docs/ResearchLifecycleGuide_JA.md](docs/ResearchLifecycleGuide_JA.md)（PPTX版：[docs/](docs/)）

---

## リポジトリ構成

```
research-lifecycle-guide/
├── README.md                          ← このファイル（概要・導入手順）
├── docs/
│   ├── ResearchLifecycleGuide_JA.md   ← 統合ガイド全文（Markdown）
│   └── 20260709_Research_Lifecycle_Guide_v6_JA.pptx  ← スライド版
├── skills/                            ← スキルのソース（Markdown・読める形）
│   ├── paper-compiler/                （write / review / audit の3モード）
│   │   ├── SKILL.md
│   │   ├── references/                （-er形式：blueprint-designer / composer /
│   │   │                                composition-checker / auditor / evaluation-planner）
│   │   └── assets/paper_template_v0.docx
│   ├── research-starter/              （はじめの一歩・6フェーズの伴走）
│   ├── research-proposer/             （研究プロポーザルの対話コンパイル）
│   ├── literature-researcher/         （虎の巻の探索：研究者・地図・世界線・候補文献）
│   ├── literature-reviewer/           （文献の検証・平易な要約・URL確認）
│   └── file-naming-convention/        （全成果物の命名規則）
├── dist/                              ← claude.ai にそのままアップロードできる .skill（ZIP）
│   ├── paper-compiler.skill
│   ├── research-starter.skill
│   ├── research-proposer.skill
│   ├── literature-researcher.skill
│   ├── literature-reviewer.skill
│   └── file-naming-convention.skill
└── templates/                         ← v0テンプレート（Markdown版）
    ├── paper_template_v0_JA.md
    ├── research_start_template_v0_JA.md
    └── proposal_template_v0_JA.md
```

## スキル一覧（5＋1）

| Skill | 役割 | 主な起動フレーズ |
|---|---|---|
| **paper-compiler** | 論文執筆の統合：write（素材→ドラフト生成）／ review（❌/⚠️＋充足質問の収束ループ）／ audit（投稿前18項目監査） | 「論文にして」「reviewmodeで」「投稿前チェック」 |
| **research-starter** | はじめの一歩の伴走（ORCID〜執筆力の6フェーズを状態機械で管理） | 「研究を始めたい」「研究スタート」 |
| **research-proposer** | 研究プロジェクト計画書の対話コンパイル（固定目次・キックオフ可能版まで収束） | 「研究プロポーザル」「研究計画をまとめて」 |
| **literature-researcher** | 虎の巻の**探索**：トップ研究者5〜10名・トピック地図・世界線・候補文献（7割・2020年以降） | 「トップ研究者を調べて」「虎の巻を作って」 |
| **literature-reviewer** | 文献の**検証**：実在確認・中学生でもわかる要約・本文URL検証（⚠️＝出典不明・要確認） | 「参考文献リストを作って」「引用のURLを確認して」 |
| file-naming-convention | 全成果物の命名規則（`YYYYMMDD_名称_vX_LANG.拡張子`） | DOCX/PPTX/XLSX 出力時に自動適用 |

パイプライン：**starter → proposer → compiler v2**（v0リレー）。文献は **researcher（探索）→ reviewer（検証）** が全工程を支援し、paper_template の②Literature Review ／ プロポーザル末尾に改ページで挿入されます。

---

## インストール

### A. Claude（claude.ai ブラウザ／モバイル）

1. `dist/` の `.skill` ファイルをダウンロード
2. claude.ai → **Settings → Customize → Skills → Add** からアップロード（1ファイルずつ・6本）
3. ⚠️ 旧スキル（`research-project-plan`・`paper-review-imrad`・`paper-review-imrad-en`）が登録されている場合は、**先に削除**してください（起動フレーズが競合します）

### B. Claude Code（ターミナル／VS Code）

```bash
git clone https://github.com/<YOUR_ACCOUNT>/research-lifecycle-guide.git
mkdir -p ~/.claude/skills
cp -r research-lifecycle-guide/skills/* ~/.claude/skills/
```

`skills/` 配下のフォルダをそのまま `~/.claude/skills/` に置くだけで有効になります。
※ claude.ai（ブラウザ）と Claude Code の Skill は**同期しません**。使う環境ごとに登録してください。

### C. その他の LLM（ChatGPT / Gemini など）

`.skill` は単なる ZIP、中身はプレーンな Markdown です。`skills/<name>/SKILL.md` がそのまま「役割定義プロンプト」として機能します。

- **ChatGPT（GPTs）**：GPT Builder の **Instructions** に `SKILL.md` の本文を貼り付け、`references/` の各 md と `templates/` の md を **Knowledge** としてアップロード
- **Gemini（Gems）**：Gem の指示文に `SKILL.md` を貼り付け、references を参考ファイルとして添付
- **汎用**：システムプロンプトに `SKILL.md`、必要に応じて references を続けて投入

**制限事項**：DOCX の生成・コメント・変更履歴・黄色網掛けなどの手順は Claude の実行環境（docx スキル等）を前提としています。他LLMでは「Markdown で同じ構成を出力する」運用に読み替えてください（スロット行列・❌/⚠️＋充足質問・18項目監査などの中核ロジックはそのまま動きます）。

---

## クイックスタート（Claude）

1. **研究を始める**：「研究を始めたい」→ research-starter が Phase 01（ORCID）から伴走
2. **計画書を作る**：「研究プロポーザルを作って」→ research-proposer が固定目次で Proposal DOCX を生成
3. **論文を書く**：`templates/paper_template_v0_JA.md`（または DOCX）の1ページ目を記入し、メモ・議事録と一緒に添付 →「論文にして」
4. **投稿前チェック**：完成稿を添付 →「投稿前チェック」→ 18項目監査（❌3件以上なら review ループへ）

---

## 日本語版と英語版の運用方針

**同一リポジトリで管理します**（推奨・本リポジトリの方針）。

- 理由：本プロジェクトの命名規則では **JA / EN は常に同一バージョン**で管理するため、リポジトリを分けると版同期のコストと事故（片方だけ更新）が発生します。1リポジトリなら1コミットで両言語を揃えられます。
- ファイル規則：言語別ファイルは `_JA` / `_EN` サフィックスで並置（例：`ResearchLifecycleGuide_JA.md` / `ResearchLifecycleGuide_EN.md`、`paper_template_v0_JA.md` / `_EN.md`）。README はトップを英語＋日本語併記（国際公開の慣行）。
- **Skill は言語別に分けません**：各 SKILL.md の description はバイリンガルで、出力言語は入力（論文・会話）の言語に追従します。旧 paper-review-imrad の JA/EN 分割で起きた起動競合を避けるためでもあります。
- 将来 Firebase ウェブアプリを追加する場合も同一リポジトリ内の `app/` ディレクトリで管理し、UI の i18n はアプリ側（Vue i18n）で行います。

## Roadmap

- [ ] 英語版ドキュメント・テンプレート（`_EN`）の追加
- [ ] **Firebase ウェブアプリ**：アイディア・興味を入力すると research lifecycle 一式（starter → proposer → compiler）を実行するアプリ（`app/` に追加予定。AIx 標準スタック：Vue / Vuetify / Firebase）
- [ ] スキルの評価（skill-creator による検出率・偽❌率ベンチマーク）

## Acknowledgment

- 岡 宗一 教授（武蔵野大学 データサイエンス学部）── 貴重なフィードバックとアドバイス
- 浦木メソッド（アブストラクト7文法・箱テンプレートA/B・流し込みエディタ）

## License

TBD（公開前に決定してください。ドキュメント＝CC BY 4.0、スキル定義＝MIT などの組み合わせを推奨）

---

Musashino University, Faculty of Data Science ／ Yusuke Takahashi (Co-founder, AIx, Inc.)
