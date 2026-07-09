# Research Lifecycle Guide

**AI skills that accompany the entire research lifecycle — from a researcher's first steps to paper submission.**

A curated set of Claude Skills, a learning guide, and v0 templates. Japanese-first today; documents and templates are provided in both languages (skill bodies are being unified to English — Japanese trigger phrases are always kept).

🇯🇵 日本語版 README は **[README_JA.md](README_JA.md)** ／ フルガイド（日本語）は **[docs/ResearchLifecycleGuide_JA.md](docs/ResearchLifecycleGuide_JA.md)**

**The lifecycle:** `01 First Steps → 02 Project Start → 03 Choose the Format → 04 Write the Paper → 05 Pre-submission Audit`

📖 Full guide: [docs/ResearchLifecycleGuide_JA.md](docs/ResearchLifecycleGuide_JA.md) (JA Markdown) ・ Slide decks: [docs/](docs/) (`v7_JA.pptx` / `v7_EN.pptx`)

## The Skills (5 + 1)

| Skill | Role | Trigger examples |
|---|---|---|
| **paper-compiler** | One skill for paper writing: `write` (material → full draft), `review` (gap-flag / fulfillment-question convergence loop), `audit` (18-item pre-submission gate incl. the closed-world check) | "turn this into a paper", "what's missing?", "pre-submission check" |
| **research-starter** | Coaches a researcher's first steps: ORCID → question & hypothesis → branding → references → venues → writing skills, as a 6-phase state machine | "I want to start doing research" |
| **research-proposer** | Compiles a kickoff proposal in dialogue against a fixed outline, converging to a "kickoff-ready" DOCX | "research proposal", "draft the project plan" |
| **literature-researcher** | *Survey agent*: top 5–10 researchers, topic map, "world-line" statement, candidate reference list (70% post-2020) | "map the top researchers", "build my playbook" |
| **literature-reviewer** | *Verify agent*: confirms each source exists, writes plain-language summaries (junior-high level), verifies full-text URLs; unverifiable → flagged "source unknown — verify" | "build a reference list", "check these citation URLs" |
| file-naming-convention | Uniform naming for every deliverable (`YYYYMMDD_name_vX_LANG.ext`) | applied automatically |

**Pipeline:** `starter → proposer → compiler v2` (the v0 relay), with `researcher (survey) → reviewer (verify)` supporting references at every stage. The reviewer inserts a page-broken *Literature Review* section into `paper_template` (between the question sheet and the review history) and at the end of proposals (after the FAQ).

## Repository layout

```
skills/      Skill sources (readable Markdown: SKILL.md + references/ + assets/)
dist/        Ready-to-upload .skill packages (ZIP) for claude.ai
docs/        The full guide (Markdown, JA) + slide decks (PPTX, JA & EN)
templates/   v0 templates in Markdown (paper / research-start / proposal, JA & EN)
```

## Installation

### Claude (claude.ai — browser / mobile)

1. Download the `.skill` files from [`dist/`](dist/)
2. claude.ai → **Settings → Customize → Skills → Add** (upload each file)
3. ⚠️ If the legacy skills `research-project-plan`, `paper-review-imrad`, or `paper-review-imrad-en` are registered, **delete them first** — their triggers collide with the new set.

### Claude Code (terminal / VS Code)

```bash
git clone https://github.com/aix-sc/research-lifecycle-guide.git
mkdir -p ~/.claude/skills
cp -r research-lifecycle-guide/skills/* ~/.claude/skills/
```

Note: skills do **not** sync between claude.ai (browser) and Claude Code — register them in each environment you use.

### Other LLMs (ChatGPT, Gemini, ...)

A `.skill` file is just a ZIP of plain Markdown. `skills/<name>/SKILL.md` works directly as a role/system prompt.

- **ChatGPT (GPTs):** paste `SKILL.md` into the GPT's *Instructions*; upload the `references/` and `templates/` Markdown files as *Knowledge*.
- **Gemini (Gems):** paste `SKILL.md` into the Gem instructions; attach references as files.
- **Generic:** put `SKILL.md` in the system prompt, followed by references as needed.

**Limitations:** steps involving DOCX generation, Word comments/tracked changes and yellow highlighting assume Claude's execution environment. On other LLMs, read these as "produce the same structure in Markdown" — the core logic (slot matrices, gap flags + fulfillment questions, the 18-item audit) works unchanged.

## Quick start (Claude)

1. **Start research:** say *"I want to start doing research"* → research-starter walks you from Phase 01 (ORCID).
2. **Write the plan:** *"draft a research proposal"* → research-proposer generates the Proposal DOCX.
3. **Write the paper:** fill page 1 of `templates/paper_template_v0` and attach it with your notes → *"turn this into a paper"*.
4. **Before submitting:** attach the finished draft → *"pre-submission check"* → the 18-item audit.

## Language policy (JA / EN)

Both languages live in **this single repository** — our naming convention keeps JA/EN at identical version numbers, and one commit updates both. Language-specific files use `_JA` / `_EN` suffixes. **Skills are not split by language**: descriptions are bilingual and output language follows your input (splitting caused trigger collisions in the past). Skill bodies are being unified to English while keeping Japanese trigger phrases.

## Roadmap

- [x] English slide deck (`docs/*_v7_EN.pptx`) and English templates (`templates/*_EN.md`)
- [ ] English guide in Markdown (`docs/ResearchLifecycleGuide_EN.md`)
- [ ] English skill bodies (keeping Japanese triggers in descriptions)
- [ ] **Firebase web app** (`app/`): enter an idea or interest and it runs the whole research lifecycle (starter → proposer → compiler). AIx standard stack: Vue / Vuetify / Firebase.
- [ ] Skill evaluation via skill-creator (defect detection rate / false-flag rate benchmarks)

## License

Dual-licensed: **skills/ and dist/ = [MIT](LICENSE)** ・ **docs/ and templates/ = [CC BY 4.0](LICENSE-DOCS)** (attribution required).

## Acknowledgments

- Prof. Souichi Oka (Musashino University, Faculty of Data Science) — invaluable feedback and advice
- The Uraki method (7-sentence abstract, hako template A/B, fill-in editor)

---

Musashino University, Faculty of Data Science ・ Yusuke Takahashi (Co-founder, AIx, Inc.)
