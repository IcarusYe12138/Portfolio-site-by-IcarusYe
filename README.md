# Portfolio Site Kit

A field-tested skill for building trilingual (English / Simplified Chinese / Traditional Chinese) portfolio and works-showcase static sites that work for both global and mainland-China audiences.

The kit is distilled from the real-world experience of building [icarusye.site](https://icarusye.site/) — a production portfolio of hand-written HTML/CSS/JS on Cloudflare Pages, zero frameworks, zero build step, heavy on audio, video, embedded decks and long-form articles, all readable from both sides of the Great Firewall. That site is both a live example of this methodology and a reference to browse alongside the docs.

**This is not a template to clone. It is a methodology**: an intake questionnaire, design rules, component specifications, dual-region media strategy, deployment discipline, a three-layer documentation system, and a pitfall list of 23 real-world failures, each recorded as *symptom → root cause → how to avoid*.

[简体中文版](README.zh-CN.md) · [繁體中文（港式粵語）](README.zh-HK.md)

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
| Reachability check (multi-node ping/speed) | [ITDOG HTTP](https://www.itdog.cn/http/) · [探测网](https://www.tanceshu.net/) · [kk.yun / 快快测](https://www.kk.yun.com/) · [DNSPup](https://www.dnspup.com/) | Multi-province mainland + overseas nodes probe ping/TCP/HTTP/DNS/SSL on your live URL; use a second one when nodes wobble or as backup |
| Digital card (global) | [Popl](https://popl.co/) | Embeddable card iframe |
| Digital card (mainland) | [muse link](https://muselink.cc/) | Mainland-reachable card iframe |
| Works inventory carrier | [Feishu](https://www.feishu.cn/) | Structured base (one row per work, link columns) |
| Logo generators (web, style exploration) | [Arknights: Endfield-style](https://ark.ncreeper.top/) · [TuxuAI](https://www.tuxuai.com/share/inspiration?shareId=880) | Shared for reference only, no endorsement — verify licence before commercial use |
| MCP (optional) | [github-mcp-server](https://github.com/github/github-mcp-server) · [mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) · [AnySearch](https://www.anysearch.com/home) | Let the agent drive GitHub / Cloudflare directly, or search the open web from the conversation |
| Multimodal (optional) | [Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | Lets non-vision agents understand video / audio / images; requires your own Qwen API key |

## Repository layout

```
├── SKILL.md                  Skill entry point: triggers, core principles, workflow, file map
├── CHANGELOG.md              Versioned history of the kit itself
├── references/
│   ├── 00-onboarding.md          Intake questionnaire, content carriers, toolchain, privacy rules
│   ├── 01-design-and-style.md    Design tokens + the "find your style" methodology + copy discipline
│   ├── 02-components.md          Component specs: topbar, cards, filters, players, case pages, preloader, contact, embedded cards, colophon
│   ├── 03-media-compat.md        Cross-region media compatibility (video / audio / web archives / four-layer regional diff)
│   ├── 04-deploy-and-domain.md   Hosting, caching discipline, custom-domain binding walkthrough (routes + troubleshooting), domain-buying guide, SEO basics, privacy-friendly analytics & compliance, China reachability
│   ├── 05-structure-i18n.md      Folder structure + trilingual engine + homepage architecture
│   ├── 06-iteration.md           Three-layer documentation system (master plan / round logs / living archive)
│   ├── 07-pitfalls.md            23 pitfalls, each as symptom → root cause → avoidance
│   ├── 08-accessibility-motion.md  WCAG 2.2 baseline & test tools, accessibility patterns, reduced-motion strategy, photosensitivity guards
│   ├── 09-performance.md         Performance: font subsetting pipeline, lazy loading, IO patterns, resource hints & image formats
│   ├── 10-content-ops.md         Content ops: works add/remove sync checklist, count automation, periodic content audits
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
# or, with the vercel-labs skills CLI:
npx skills add https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe
```

(Or copy the repository folder into your skills directory.) The agent then invokes it when you ask to create, restructure or iterate a portfolio, works showcase, or media-rich static site. `tools/` and `examples/` ship with the kit — see `tools/README.md` for the font pipeline and consistency audit.

### Companion skills (asked during onboarding)

This kit owns the portfolio **lifecycle** (structure, dual-region media, trilingual, content ops, deploy); horizontal taste and compliance come from companion skills. During intake it asks whether to install:

| Tier | Skill | Fills |
|---|---|---|
| ★ essential | [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) (Anthropic) | Aesthetic direction before code; anti AI-slop |
| ★ essential | [web-design-guidelines](https://github.com/vercel-labs/agent-skills) (Vercel) | 100+ WCAG 2.2 / UX audit rules |
| recommended | [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 240+ styles / 127 font pairings — divergence when no references exist |
| recommended | [impeccable](https://impeccable.style/) | brand-mode polish commands (typeset / colorize / bolder / quieter) |

Rule of thumb: ask first (the user may already have equivalents), keep the total skill budget ≤ 20–30, and when a companion skill pushes a React component stack, this kit's static-first principle wins.

**Installation discipline (hard rule, applies to every MCP and skill): never install anything without the user's explicit consent.** The agent recommends, gives the command and the reasoning — the user executes it themselves, or explicitly authorises the agent to do so. Every optional tool above is just that: optional, and nothing in the workflow breaks without it.

## Resources for the design phase

These are separate from the companion skills above: they address *"which icon set?"* / *"how do I prototype a style?"* / *"which frontend skills are worth installing?"* questions. Full disclosure applies — the agent never installs anything on its own (see the discipline rule above). Ratings are the author's assessment, not an obligation.

### Icon libraries (when a user asks which icons to use)

| Library | Style | Agent access | Coverage | Licence / notes |
|---|---|---|---|---|
| [simple-icons](https://github.com/simple-icons/simple-icons) ★ **first choice** | Monochrome minimal line/silhouette, 3300+ brand icons | Direct CDN SVG by slug — no build, agent can `fetch` `https://cdn.jsdelivr.net/npm/simple-icons@15/icons/slug.svg` | QQ (renamed), Sina Weibo, Bilibili, Xiaohongshu + nearly all overseas platforms | **CC0 / no attribution**; industry fact-standard; paste the slug into a URL and you are done |
| [NViconsLib Silhouette](https://github.com/nullice/NViconsLib_Silhouette) | Pure-silhouette, **built for mainland CN + global** social sites, 189 icons | Raw GitHub SVG/PSD/EPS (`raw.githubusercontent.com`) | WeChat, moments, Sina/Tencent Weibo, QQ Zone, Bilibili, Tencent Video + Facebook/Twitter/Instagram | Best supplement when simple-icons/thesvg lack a CN-only platform |
| [thesvg](https://github.com/glincker/thesvg) | Minimal brand SVG, 6000+ icons, mono/color both | Native `@thesvg/mcp-server` for Claude/Cursor/Windsurf; also `npx @thesvg/cli add` | Sina Weibo + suite updates continuously | Best *conversational* option — agent calls a tool by name instead of hand-writing URLs |
| [icons8-mcp](https://github.com/icons8/icons8-mcp) | 116 styles incl. minimal line, 360k+ icons | Official MCP server (`https://mcp.icons8.com/mcp/`), natural-language search → SVG/PNG stream | By-name hits WeChat/Weibo/Douyin, needs manual verification | **Free quota only returns PNG; SVG needs an API key**; best for brand-colour fidelity and obscure CN apps |

Quick pick: **simple-icons** for "look up a slug, embed the SVG" (CC0, zero setup); **NViconsLib Silhouette** when a mainland-only platform is missing upstream; **thesvg / icons8** when you want conversational, tool-calling lookup.

### Design & prototyping tools

| Tool | What it does | When it helps |
|---|---|---|
| [Google Stitch](https://stitch.withgoogle.com/) | Gemini-driven AI UI generator: text / sketch / screenshot → multi-screen prototype + HTML/CSS/Tailwind or React code; can extract a design system from a pasted URL | Prototyping a style demo aimed at overseas design taste; free, Google account only |
| [Design Skills Hub](https://designskills.xyz/skills) · (official site [vaporaviator.com/works/design-skills-hub](https://vaporaviator.com/works/design-skills-hub)) | A community "skill registry" for design/agents — aesthetic skills (design systems, brand, critiquing) and engineering skills (code architecture, a11y, perf) | Borrowing an existing style taste (e.g. a Notion-like system) or exporting your own Figma file into a reusable skill |

The two are complementary: Stitch *generates* UI, Design Skills Hub *encodes design judgement* for an agent to follow.

### Charting / data-visualisation skills

| Skill | What it does |
|---|---|
| [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) ★ | Data-visualisation skill for AI agents — turns data into polished, interactive HTML charts for a portfolio page (metrics, timelines, distribution), no heavy charting library needed. Clone into your skills dir; ships a `SKILL.md` |

### Frontend-design skills worth considering (author's assessment)

Alongside the ★ companion skills already listed above, the following were evaluated:

| Skill | Verdict | Why |
|---|---|---|
| **Design Tokens** (OKLCH colour) — [XINGANLIU/design-system-generator-skill](https://github.com/XINGANLIU/design-system-generator-skill) (also community [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills#design-token)) | ★ recommended | Complements this kit's token discipline — switch one `hue` and the whole site recolours (OKLCH), with light/dark auto-adaptation; fits static-first and the single-accent principle |
| **identity-skill** (Sac-Y) — [Sac-Y/identity-skill](https://github.com/Sac-Y/identity-skill) | optional | Generates a reference image first, you confirm, then it recreates 1:1 with blocking checkpoints — pairs well with the "find your style" step, but depends on an image model |
| **Motion Skill** (Framer Motion) — community e.g. [schoepplake/framer-motion-skill](https://github.com/schoepplake/framer-motion-skill) | **not recommended for this stack** | Built for React/animation-heavy apps; conflicts with this kit's static-first + restrained-motion principles |
| Frontend Design / UI/UX Pro Max / Web Design Guidelines | already in the ★ companion table above | no action needed |

Bottom line: install **Design Tokens** if you care about colour science; skip **Motion Skill** unless you are building a React app (out of this kit's scope); keep the rest as comfort picks.

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

## Licence

[MIT](LICENSE) · Copyright (c) 2026 IcarusYe12138

The methodology and code skeletons are free to reuse; the portfolio they were distilled from remains the author's own work.
