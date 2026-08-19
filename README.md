# Portfolio Site Kit

A field-tested skill for building trilingual (English / Simplified Chinese / Traditional Chinese) portfolio and works-showcase static sites that work for both global and mainland-China audiences.

The kit is distilled from the real-world experience of building [icarusye.site](https://icarusye.site/) — a production portfolio of hand-written HTML/CSS/JS on Cloudflare Pages, zero frameworks, zero build step, heavy on audio, video, embedded decks and long-form articles, all readable from both sides of the Great Firewall. That site is both a live example of this methodology and a reference to browse alongside the docs.

**This is not a template to clone. It is a methodology**: an intake questionnaire, design rules, component specifications, dual-region media strategy, deployment discipline, a three-layer documentation system, and a pitfall list of 23 real-world failures, each recorded as *symptom → root cause → how to avoid*.

[简体中文版](README.zh-CN.md)

---

## What it solves

| Problem | This kit's answer |
|---|---|
| Where to start — unclear style, unclear content | Intake questionnaire first: style references (code / screenshots / HTML / Figma), résumé and works inventory, link checklist; style demo first, content files later |
| Overseas CDNs, fonts and cloud links break in mainland China | Full self-hosting discipline + dual-link strategy (overseas direct link + mainland mirror) |
| Videos that play abroad but not in China | `<video>` direct links (`raw=1`) for global users, embeddable mainland-platform iframes (`?embed`) for Chinese users, switched as whole blocks per language |
| Unreachable article links | Local HTML archive pattern: CSS, fonts and images all localised for CMS pages; assets-only for JS-driven scrollytelling |
| Chinese webfont payloads of several megabytes | Subset first by the site's actual character set, then split into unicode-range chunks |
| Stale CSS/JS after deploys | Cache-busting discipline: every content change bumps `?v=YYYYMMDD` |
| Multilingual sites drifting into divergent codebases | Single-DOM trilingual engine: inline dictionary + full attribute-level i18n + `?lang=` URLs + browser detection |
| Iteration chaos | Three-layer documentation: redesign master plan → per-round decision logs → living archive at site root |
| Count drift after adding/removing works | Content-ops checklist: every sync point enumerated, counts computed from the DOM |

## Recommended toolchain

- **Build with [TRAE](https://www.trae.cn/)** — local real-time preview across phone / tablet / desktop viewports, which makes multi-device responsive work intuitive; mainstream models available. Other tools work fine too — the methodology is tool-agnostic.
- **Design prototypes with [Kimi K3](https://www.kimi.ai/blog/kimi-k3)** — the strongest aesthetics among models usable for web design; feed it your reference screenshots and get a personal style demo back. Demo first, then engineering.
- Mnemonic: *Kimi for taste, TRAE for engineering.*

## Recommended services

| Purpose | Service | Notes |
|---|---|---|
| Static hosting | [Cloudflare Pages](https://pages.cloudflare.com/) | Direct upload, zero build, 25 MiB per-file limit |
| Object storage (mainland) | [Tencent COS](https://cloud.tencent.com/product/cos) · [Aliyun OSS](https://cn.aliyun.com/product/oss) | For large media when mainland reach matters |
| Object storage (global) | [Cloudflare R2](https://www.cloudflare.com/products/r2/) | Zero egress fees; same account as Pages |
| Digital card (global) | [Popl](https://popl.co/) | Embeddable card iframe |
| Digital card (mainland) | [muse link](https://muselink.cc/) | Mainland-reachable card iframe |
| Works inventory carrier | [Feishu](https://www.feishu.cn/) | Structured base (one row per work, link columns) |
| MCP (optional) | [github-mcp-server](https://github.com/github/github-mcp-server) · [mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) | Let the agent drive GitHub / Cloudflare directly |

## Repository layout

```
├── SKILL.md                  Skill entry point: triggers, core principles, workflow, file map
├── CHANGELOG.md              Versioned history of the kit itself
├── references/
│   ├── 00-onboarding.md          Intake questionnaire, content carriers, toolchain, privacy rules
│   ├── 01-design-and-style.md    Design tokens + the "find your style" methodology + copy discipline
│   ├── 02-components.md          Component specs: topbar, cards, filters, players, case pages, preloader, contact, embedded cards, colophon
│   ├── 03-media-compat.md        Cross-region media compatibility (video / audio / web archives / four-layer regional diff)
│   ├── 04-deploy-and-domain.md   Hosting, caching discipline, domain-buying guide, privacy-friendly analytics, China reachability
│   ├── 05-structure-i18n.md      Folder structure + trilingual engine + homepage architecture
│   ├── 06-iteration.md           Three-layer documentation system (master plan / round logs / living archive)
│   ├── 07-pitfalls.md            23 pitfalls, each as symptom → root cause → avoidance
│   ├── 08-accessibility-motion.md  Accessibility patterns, reduced-motion strategy, photosensitivity guards
│   ├── 09-performance.md         Performance: font subsetting pipeline, lazy loading, IO patterns
│   ├── 10-content-ops.md         Content ops: works add/remove sync checklist + count automation
│   └── 11-preship-checklist.md   One-page pre-ship gate (hard limits + all checklists merged)
├── templates/                    Copy-paste component skeletons
│   ├── trilingual.html           Trilingual engine (full attribute set: text/alt/title/href/scramble/cursor)
│   ├── works-index.html          Works index page skeleton (DOM-computed counts + filters + HIGHLIGHT)
│   ├── case-page.html            Case detail page skeleton (cross-link list + dual-link Links section)
│   ├── 404.html                  Generic fail page (4XX-agnostic copy + language-aware return)
│   ├── audio-player.html         Inline audio player (play / seek / time / download, single instance)
│   ├── bgm.html                  Background-music singleton button
│   ├── tile-field.html           Parameterised Metro live-tile background field
│   ├── marquee.html              Infinite marquee (clone ×2 + wrap + drag + linked pause)
│   └── regional-links.html       Dual-link pattern (raw=1 / ?embed / data-href-* / lazy embed)
├── tools/                        Build & audit scripts (see tools/README.md)
│   ├── collect_chars.py          Collect CJK chars used by the site → charset file
│   ├── subset_fonts.py           Subset source fonts to the charset (TTF/OTF intermediates)
│   ├── split_cjk.js              cn-font-split → unicode-range woff2 chunks + cjk.css
│   ├── audit.sh                  Six-check consistency audit (counts / ?v= / badges / sitemap / size)
│   └── README.md                 Pipeline usage, dependencies, pitfalls, image cheat-sheet
└── examples/
    └── minimal.html              Living test page: four components assembled (double-click to run)
```

## Core principles

1. **Static first.** Plain HTML/CSS/JS, direct upload, no build command.
2. **Dual-region reachability.** Fonts, audio and key images self-hosted; every overseas service link carries a mainland alternative.
3. **Single-file limit awareness.** Large media lives in object storage (e.g. 25 MiB per-file limits on static hosts); the page layer stays light.
4. **Cache-version discipline.** Every CSS/JS content change bumps `?v=`, otherwise browsers keep immutable copies forever.
5. **Content-first layout.** On case pages, iframes, videos and links come before long prose.
6. **One accent colour.** A single saturated colour signals action only (links, focus, progress), never decoration, and covers ≤5% of any view.
7. **Restrained motion.** Transitions ≤250ms, ease-out; language switching swaps body text instantly; everything honours `prefers-reduced-motion`.
8. **Touch/mouse split.** Hover effects gated behind `(hover:hover) and (pointer:fine)`; touch devices see the full state by default.
9. **One DOM, three languages.** Per-page inline dictionaries switched in place; `?lang=` URLs for direct linking; first-visit browser detection without persisting.
10. **Written iteration.** Every round locks decisions in a log (user quote → root cause → plan → status) before code changes, then executes in one pass.

## Using the skill

### Install (TRAE or any agent with skill support)

```bash
git clone https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe.git \
  ~/.trae-cn/skills/portfolio-site-kit
```

(Or copy the repository folder into your skills directory.) The agent then invokes it when you ask to create, restructure or iterate a portfolio, works showcase, or media-rich static site. `tools/` and `examples/` ship with the kit — see `tools/README.md` for the font pipeline and consistency audit.

### As plain reference documentation

The `references/` folder reads as a standalone handbook (written in Chinese; this README is the English summary). Start with:

- `references/00-onboarding.md` before any project kickoff — the intake questionnaire and privacy rules;
- `references/03-media-compat.md` if you care about cross-region media;
- `references/07-pitfalls.md` before and after every major change, as a checklist;
- `references/09-performance.md` before shipping, for the font pipeline and lazy-loading matrix;
- `references/10-content-ops.md` whenever works are added or removed;
- `references/11-preship-checklist.md` as the one-page final gate before every release;
- `templates/` for the component skeletons, all dependency-free and self-documented;
- `examples/minimal.html` — open it directly in a browser to see four components assembled.

## Suggested workflow for a new site

1. **Intake interview** (`references/00-onboarding.md`): style references (code / screenshots / HTML / Figma), résumé and works inventory, overseas + mainland link checklist. Missing files? Style demo first, content later. Keep the works list in a structured carrier (Feishu / Markdown / spreadsheet).
2. **Define the style**: feed the reference screenshots to an image-capable agent (Kimi K3 recommended) and get a personalised style demo (colour, type, motif, layout). Lock it into a written Style Spec. Never copy an existing site.
3. **Fix the structure**: page list, homepage architecture, assets layout, language mechanism. Structural changes are the most expensive to make later.
4. **Lay components**: copy from `templates/` (case pages from `case-page.html`), skin with the Style Spec's tokens.
5. **Wire media**: dual links for video, self-hosted audio, local archives for articles. Do it all at once.
6. **Ship**: direct upload, `_headers`, robots, sitemap, og:image, domain.
7. **Iterate in written rounds** (master plan → round logs → living archive), checking the pitfall list after each pass.
8. **Grow content safely**: every works add/remove goes through the content-ops checklist.

## What this kit deliberately omits

- No bundled framework, bundler or runtime: nothing to go stale.
- No design opinion beyond discipline: the visual identity comes from the author, not the kit.
- No brand-specific links: every URL in the docs is a generic placeholder (`overseas.example`, `mainland.example`).

## License

[MIT](LICENSE) · Copyright (c) 2026 IcarusYe12138

The methodology and code skeletons are free to reuse; the portfolio they were distilled from remains the author's own work.
