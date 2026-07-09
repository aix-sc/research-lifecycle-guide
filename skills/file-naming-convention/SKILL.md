---
name: file-naming-convention
description: "成果物ファイル（DOCX / PPTX / XLSX 等）を生成・命名・改訂・提示するすべての場面で適用する統一ファイル名命名規則。日付プレフィックス YYYYMMDD_、バージョン番号 vX（初版 v1、改訂ごとに +1）、言語サフィックス JA / EN、複数ファイル同時更新時のバージョン統一、最新版の同時リンク表示を定義する。ユーザーが『ファイル名』『命名規則』『バージョン』『最新版』『v1 / v2』『JA 版・EN 版』に言及したとき、または DOCX / PPTX / XLSX を出力するときは、明示的な指示がなくても必ずこの規則に従って命名すること。Unified file-naming convention for every deliverable Claude creates, names, revises, or presents. Apply whenever the user mentions file names, naming conventions, versions, the latest version, or JA / EN versions, and whenever producing DOCX / PPTX / XLSX output, even without an explicit request."
---

# File Naming Convention / ファイル名命名規則

Claude が成果物ファイルを生成・命名・改訂・提示する際の統一規則。
Unified rules for naming deliverable files that Claude creates, revises, and presents.

## Naming format / 命名フォーマット

```
YYYYMMDD_<DescriptiveName>_vX_<LANG>.<ext>
```

例 / Example:

```
20260608_FileNamingConvention_Skill_v1_JA.docx
20260608_FileNamingConvention_Skill_v1_EN.docx
```

## Components / 構成要素

| 要素 / Element | 形式 / Format | 説明 / Description |
|---|---|---|
| 日付プレフィックス / Date prefix | `YYYYMMDD_` | 最新版を作成・更新した当日の日付を先頭に付与 / The date the latest version is produced, at the front (e.g. 2026-06-08 → `20260608_`) |
| 内容名 / Name | `DescriptiveName` | 内容が分かる簡潔な名前。英数字＋アンダースコア区切り、空白は避ける / Concise, descriptive; alphanumerics + underscores, no spaces |
| バージョン / Version | `_vX` | 初版は `_v1`、改訂ごとに +1（v1→v2→v3…）/ Start at `_v1`; increment on every revision |
| 言語サフィックス / Language | `_LANG` | 拡張子の直前に言語コード。日本語=`_JA`、英語=`_EN` / Language code just before the extension |
| 拡張子 / Extension | `.docx` `.pptx` `.xlsx` | 成果物の形式 / Matches the deliverable format |

## Rules / ルール

### 1. Date prefix / 日付プレフィックス
- 最新版を出力した「当日」の日付を `YYYYMMDD` 形式で先頭に置く。
- 改訂時は日付も当日の日付に更新する（日付とバージョンは連動）。
- Lead with today's date; refresh it on every revision so date and version move together.

### 2. Version number / バージョン番号
- 初版は必ず `v1` から開始する。
- すべての改訂でバージョンを 1 ずつインクリメントする（例: `v6` → `v7`）。連番で管理し、番号は飛ばさない。
- Always start at `v1`; increment by one on every revision; keep numbers sequential.

### 3. Language suffix / 言語サフィックス
- 言語コードをファイル名の最後（拡張子の前）に付与する: `_JA`、`_EN` など。
- 対訳セット（JA + EN）は同じ日付・同じバージョンを付け、言語サフィックスのみを変える。
- For a bilingual set, give both files the same date and version, varying only the language code.

### 4. Simultaneous updates — unified versioning / 複数ファイルの同時更新（バージョン統一）
- 複数ファイルを同時に更新する場合、セット内の全ファイルのバージョン番号を統一する。
- 内容の更新がないファイルがあっても、ファイル名の日付と `vX` のみを最新に揃える（内容は据え置きでよい）。
- 更新後は、セット全体を最新版として同時にリンク・表示する。
- When updating multiple files at once, unify the version across the whole set; even unchanged files get their date and `vX` bumped in the filename, and all latest files are linked and displayed together.

## Worked examples / 適用例

初版の作成 / Creating the first version:

```
20260608_SpiraProposal_v1_JA.docx
20260608_SpiraProposal_v1_EN.docx
```

セット内の一部のみ改訂（日付・バージョンは統一）/ Revising only part of a set (still unify date & version):

```
20260609_SpiraProposal_v2_JA.docx   # 内容を改訂 / content revised
20260609_SpiraProposal_v2_EN.docx   # 内容据え置き・名称のみ更新 / unchanged, filename only
```

## Checklist / チェックリスト

1. 先頭に当日の日付 `YYYYMMDD_` があるか / Starts with today's date `YYYYMMDD_`
2. 内容名が簡潔で空白を含まないか / Name is concise with no spaces
3. 末尾に `_vX` があり、改訂ごとにインクリメントされているか / Ends with `_vX`, incremented per revision
4. 言語サフィックス（`_JA` / `_EN` 等）が拡張子の直前にあるか / Language suffix sits just before the extension
5. セット内の全ファイルで日付・バージョンが統一されているか / Date and version unified across the set
6. 最新版のファイルをすべて同時にリンク・表示したか / All latest files linked and displayed together

## Notes / 補足

- このスキルファイル自体は、スキルとして機能させるためにフォルダ名 `file-naming-convention/` 内の `SKILL.md` を維持する。上記の日付・バージョン命名規則は、Claude が出力する DOCX / PPTX / XLSX などの成果物ファイルに適用するものであり、スキルの内部ファイル名（`SKILL.md`）には適用しない。
- This skill file must remain `file-naming-convention/SKILL.md` to function as a skill. The dated/versioned convention above applies to deliverable files (DOCX / PPTX / XLSX, etc.), not to the skill's internal `SKILL.md`.
