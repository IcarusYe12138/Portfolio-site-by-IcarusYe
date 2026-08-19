# Portfolio Site Kit

A lean, token-conserving methodology that helps you — even with zero coding background — build a **trilingual** (EN / Simplified Chinese / Traditional Chinese) personal portfolio / works-showcase **static site** that works for both global and mainland-China audiences. Plain handwritten HTML/CSS/JS, zero frameworks, zero build step.

[简体中文版](README.zh-CN.md) · [繁體中文（港式粵語）](README.zh-HK.md)

---

## It's a methodology, not a template

You don't need to read a portfolio, or finish this README, before you take action — **start from "Quick start"** and move. The further you read, the more detours you avoid:

1. **Read nothing yet?** → Go straight to [Quick start](#quick-start) and start in 5 steps.
2. **Have an old site to rework, or existing content?** → Read [How the skill reads your website](#how-the-skill-reads-your-website). It reads in batches, it doesn't gulp down all your files at once.
3. **Want the decision criteria in one place?** → See [What you get (core principles)](#what-you-get-core-principles) and the [Reference docs map](#reference-docs-map).
4. **Prefer to browse?** → Use the [Contents](#contents).

The methodology is distilled from a real project ([icarusye.site](https://icarusye.site/)), but **you don't need to reference it** — it's a source, not a gate.

### Quick start

The fastest path, zero prerequisite reading:

1. **Give me the raw material**: paste 1–3 screenshots of sites/posters you like, or describe the feeling in one sentence. Skip if you have none; we fill it in later.
2. **List your works**: one entry per work (title + type + year + a link; one overseas and one mainland link is even better).
3. **State a goal**: e.g. "a clean single-page version first", "EN + ZH bilingual", "works must open in mainland China".
4. I'll run the intake checklist from [references/00-onboarding.md](references/00-onboarding.md) one question at a time — **I ask for what you haven't given; I never guess for you**.
5. Once you've locked the style direction, I write code — one thing per round.

> **Token-saving intake rule**: *ask first, then act; if information is missing, ask — don't answer on the user's behalf.* I ask one set of questions at a time and proceed only after you reply — no dumping a whole book on you at once.

---

## Contents

- [What it solves](#what-it-solves)
- [Is this for you?](#is-this-for-you)
- [What you get (core principles)](#what-you-get-core-principles)
- [How the skill reads your website](#how-the-skill-reads-your-website)
- [Reference docs map](#reference-docs-map)
- [Repository layout](#repository-layout)
- [Install](#install)
- [Recommended toolchain](#recommended-toolchain)
- [Recommended services](#recommended-services)
- [Design-phase resources](#design-phase-resources)
- [Companion skills](#companion-skills)
- [What this kit deliberately omits](#what-this-kit-deliberately-omits)
- [Licence](#licence) · [Link freshness](#link-freshness)

---

## What it solves

| Pain point | This kit's answer |
|---|---|
| No idea where to start — style and content both unclear | Intake questionnaire first to fix the style direction; style demo first, content files later |
| Overseas CDNs, fonts and cloud links break in mainland China | Full self-hosting discipline + dual-link strategy (overseas direct link + mainland mirror) |
| Video plays abroad but not in China | `<video>` direct link (`raw=1`) overseas; embeddable mainland-platform iframe (`?embed`) in China; switch per whole block by language |
| Unreachable article links | Local HTML archive: CSS, fonts and images all localised for CMS pages |
| Chinese webfont payloads run to several MB | Subset by the site's actual character set first, then split into unicode-range chunks |
| CSS/JS not updating after deploys | Cache-version discipline: every content change bumps `?v=YYYYMMDD` |
| Multilingual site drifts into divergent codebases | Single-DOM trilingual engine: inline dictionary + attribute-level i18n + `?lang=` URLs + browser detection |
| Iteration chaos, changes keep splitting | Three-layer docs: redesign master plan → per-round decision logs → living archive |
| Counts drift after adding/removing works | Content-ops checklist + counts computed from the DOM |

## Is this for you?

**Fits**: personal portfolio / works showcase / CV-type static site; with audio, video, image-text and iframe embeds; needs global + mainland reachability; public, no login, no backend.

**Doesn't fit / can skip**: heavy backend business systems (not static-first); single-language mainland-only with no large media (skip the dual-link chapters; the rest still applies).

## What you get (core principles)

1. **Static first.** Plain HTML/CSS/JS, direct upload, no build command.
2. **Dual-region reachability.** Fonts, audio and key images self-hosted; every overseas link carries a mainland alternative.
3. **Single-file limit awareness.** Large media lives in object storage; keep the page layer light.
4. **Cache-version discipline.** Any CSS/JS change bumps `?v=`, otherwise browsers keep stale copies.
5. **Content-first layout.** On case pages, iframes, videos and links precede long prose.
6. **One accent colour.** A single saturated colour signals action only, ≤ 5% of any view.
7. **Restrained motion.** Transitions ≤ 250ms, ease-out; everything honours `prefers-reduced-motion`.
8. **Touch/mouse split.** Hover effects gated behind `(hover:hover) and (pointer:fine)`.
9. **One DOM, three languages.** Inline dictionaries swap in place; `?lang=` URLs for direct linking; first-visit browser detection without persisting.
10. **Written iteration.** Every round locks decisions into a log before code changes; one round, one thing.

## How the skill reads your website

**Core: read in batches, advance layer by layer, never gulp down all your files at once.** This saves tokens and keeps the signal from drowning in noise.

Reading order (at each step, judge from the findings whether to continue; read the next layer only if needed):

1. **Entry layer**: index/home first (`index.html`, `works`, directory, `_headers` / `robots.txt` / `sitemap.xml`) — a minimal sample tells you "what site, what languages, rough structure".
2. **Style layer**: CSS variables / design tokens (colour, type, spacing) — tells you the style and whether it's systematic.
3. **Script layer**: interaction scripts (language switch, filters, players) — tells you the trilingual mechanism and component reuse.
4. **Media layer**: only when you hit a video/audio/external link do you consult the media docs and links — to verify cross-region reachability.
5. **Deep-read only the reference doc you actually need**, nothing irrelevant.

For file selection, use the [Reference docs map](#reference-docs-map): open the one matching your task — don't load the whole bundle.

## Reference docs map

`references/` is theme-split deep documentation. **Open the one matching your task**, don't read it all at once — saves tokens and reads better:

| Your situation | Open this |
|---|---|
| New site, must do first | [00-onboarding](references/00-onboarding.md) — intake questionnaire, content carriers, toolchain, privacy rules |
| Fix the style direction | [01-design-and-style](references/01-design-and-style.md) — find-your-style 3-step, Style Spec, copy discipline |
| Build the component skeleton | [02-components](references/02-components.md) — when/points/anti-patterns per component |
| Works must be viewable across regions | [03-media-compat](references/03-media-compat.md) — video/audio/image-text dual links |
| Deploy / buy a domain / caching | [04-deploy-and-domain](references/04-deploy-and-domain.md) — hosting, caching, domain, SEO, compliance |
| Clarify folders & the trilingual mechanism | [05-structure-i18n](references/05-structure-i18n.md) — folder structure + trilingual engine |
| Iterate and polish | [06-iteration](references/06-iteration.md) — three-layer docs + round cadence |
| Self-check before & after every big change | [07-pitfalls](references/07-pitfalls.md) — 23 real-world pitfalls |
| Accessibility / motion safety | [08-accessibility-motion](references/08-accessibility-motion.md) — WCAG 2.2, reduced-motion, photosensitivity |
| Optimise performance / fonts | [09-performance](references/09-performance.md) — font pipeline, lazy loading, resource hints |
| Add / remove works | [10-content-ops](references/10-content-ops.md) — add/remove sync checklist + count automation |
| Final pre-ship gate | [11-preship-checklist](references/11-preship-checklist.md) — one-page checklist |
| Copy a component / see it work | `templates/` (dependency-free skeletons) · `examples/minimal.html` (double-click to run) |

## Repository layout

```
portfolio-site-kit/
├── SKILL.md                Entry: triggers, core principles, batched workflow, file map
├── CHANGELOG.md            Versioned history of the kit itself
├── references/             Theme-split deep docs (open the one for your task, see map)
├── templates/              Copy-paste component skeletons (0 deps, self-documented)
│   ├── trilingual.html     Trilingual engine (text/alt/title/href/scramble/cursor)
│   ├── works-index.html    Works index (DOM counts + filters + HIGHLIGHT)
│   ├── case-page.html      Case detail page (cross-links + dual-link Links)
│   ├── 404.html            Generic fail page
│   ├── audio-player.html   Inline audio player
│   ├── bgm.html            Background-music singleton
│   ├── tile-field.html     Parameterised Metro tile field
│   ├── marquee.html        Infinite marquee
│   └── regional-links.html Dual-link / video / iframe
├── tools/                  Build & audit scripts (see tools/README.md)
└── examples/
    └── minimal.html        Four-component minimal assembly (double-click to run)
```

## Install

One-time setup (TRAE or any agent with skill support):

```bash
git clone https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe.git \
  ~/.trae-cn/skills/portfolio-site-kit
# or, with the vercel-labs skills CLI:
npx skills add https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe
```

(Or just copy the repository folder into your skills directory.) Afterwards, saying "build a portfolio / restyle it / add languages / fix mainland access" auto-invokes it. `tools/` and `examples/` ship with the repo.

## Recommended toolchain

- **Build with [TRAE](https://www.trae.cn/)** — local real-time preview across phone/tablet/desktop viewports; mainstream models available. The methodology is tool-agnostic; alternatives work fine.
- **Design prototypes with [Kimi K3](https://www.kimi.ai/blog/kimi-k3)** — strong aesthetics; feed it your reference screenshots for a personal style demo.
- Mnemonic: *Kimi for taste, TRAE for engineering.*

(Named picks are "author-verified, current as of 2026-08"; tools are time-sensitive choices — if a link dies, swap by capability, see [Link freshness](#link-freshness).)

## Recommended services

| Purpose | Service | Notes |
|---|---|---|
| Static hosting | [Cloudflare Pages](https://pages.cloudflare.com/) | Direct upload, zero build, 25 MiB per file |
| Object storage (mainland) | [Tencent COS](https://cloud.tencent.com/product/cos) · [Aliyun OSS](https://cn.aliyun.com/product/oss) | Large media external, stable mainland link |
| Object storage (global) | [Cloudflare R2](https://www.cloudflare.com/products/r2/) | Zero egress; same CF account |
| Reachability check | [ITDOG HTTP](https://www.itdog.cn/http/) | Multi-province mainland + overseas nodes |
| Digital card | [Popl](https://popl.co/) (global) / [muse link](https://muselink.cc/) (mainland) | Embeddable card iframe |
| Works inventory carrier | [Feishu](https://www.feishu.cn/) | Structured base, one row per work, link columns |
| Logo generators (web, style exploration) | [Arknights: Endfield](https://ark.ncreeper.top/) · [TuxuAI](https://www.tuxuai.com/share/inspiration?shareId=880) | Shared for reference, verify licence before commercial use |
| MCP (optional) | [github-mcp-server](https://github.com/github/github-mcp-server) · [mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) · [AnySearch](https://www.anysearch.com/home) | Drive GitHub/CF directly, or search the web in-conversation |
| Multimodal (optional) | [Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | Lets non-vision agents understand media; needs your own Qwen API key |

## Design-phase resources

Design-time questions: which icons, how to prototype, whether to install certain frontend skills. Quick answers below (ratings are the author's subjective assessment, not an obligation):

### Icon libraries
| Library | Style | Agent access | Coverage | Licence / notes |
|---|---|---|---|---|
| [simple-icons](https://github.com/simple-icons/simple-icons) ★ first choice | Monochrome minimal, 3300+ brands | CDN by slug | QQ/Weibo/Bilibili/Xiaohongshu + nearly all overseas | **CC0 / no attribution**, industry standard |
| [NViconsLib Silhouette](https://github.com/nullice/NViconsLib_Silhouette) | Pure silhouette, for mainland + global | GitHub Raw | WeChat/QQ Zone/Weibo + overseas | Supplement for CN-only platforms |
| [thesvg](https://github.com/glincker/thesvg) | Minimal brand SVG, 6000+ | `@thesvg/mcp-server` conversational | incl. Weibo, updating | Call by name, no hand-written URLs |
| [icons8-mcp](https://github.com/icons8/icons8-mcp) | 116 styles, 360k+ | Official MCP, natural-language | By-name hits, verify manually | Free gives PNG only; SVG needs a key |

### Design & prototyping
| Tool | What it does |
|---|---|
| [Google Stitch](https://stitch.withgoogle.com/) | Gemini AI UI: text/sketch/screenshot → multi-screen prototype + code; can extract a design system |
| [Design Skills Hub](https://designskills.xyz/skills) · (official site [vaporaviator.com/works/design-skills-hub](https://vaporaviator.com/works/design-skills-hub)) | Community design-skill registry: aesthetic + engineering skills; export a Figma file into a reusable skill |

Complementary: Stitch *generates* UI, Design Skills Hub *encodes design judgement*.

### Charting / data visualisation
| Skill | What it does |
|---|---|
| [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) ★ | Data → polished interactive HTML charts (metrics/timelines/distribution), no heavy charting library |

### Frontend-design skills (author's assessment)
| Skill | Verdict |
|---|---|
| **Design Tokens** (OKLCH) — [XINGANLIU/design-system-generator-skill](https://github.com/XINGANLIU/design-system-generator-skill) ★ | Recolour the whole site from one `hue`; fits static-first + one-accent |
| **identity-skill** (Sac-Y) — [Sac-Y/identity-skill](https://github.com/Sac-Y/identity-skill) | Optional: confirm a reference image first, then recreate 1:1; depends on an image model |
| **Motion Skill** (Framer Motion) — [schoepplake/framer-motion-skill](https://github.com/schoepplake/framer-motion-skill) | **Not recommended for this stack**: React-oriented, conflicts with static-first |

In short: install **Design Tokens** if you care about colour science; consider **Motion Skill** only for React (out of this kit's scope); keep the rest as comfort picks.

## Companion skills

This kit owns the portfolio **lifecycle** (structure, dual-region media, trilingual, content ops, deploy); horizontal taste and compliance come from companion skills. **During intake it asks whether to install** — it never installs unilaterally:

| Tier | Skill | Fills |
|---|---|---|
| ★ essential | [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) (Anthropic) | Aesthetic direction before code; anti AI-slop |
| ★ essential | [web-design-guidelines](https://github.com/vercel-labs/agent-skills) (Vercel) | 100+ WCAG 2.2 / UX audit rules |
| recommended | [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 240+ styles / 127 font pairings — divergence when no references exist |
| recommended | [impeccable](https://impeccable.style/) | brand-mode polish commands |

Discipline: ask first (the user may already have equivalents); keep the total skill budget ≤ 20–30; when a companion skill pushes a React component stack, this kit's static-first principle wins.

**Installation discipline (hard rule, applies to every MCP and skill): never install anything without explicit consent.** The agent recommends, gives the command and the reasoning — you execute it, or explicitly authorise the agent to. Every optional tool above is just that: optional, nothing breaks without it.

## What this kit deliberately omits

- No bundled framework, bundler or runtime — nothing to go stale.
- No design opinion beyond discipline — the visual identity comes from you, not the kit.
- No brand-specific links — every URL in the docs is a generic placeholder.

## Licence

[MIT](LICENSE) · Copyright (c) 2026 IcarusYe12138

The methodology and code skeletons are free to reuse; the portfolio they were distilled from remains the author's own work.

## Link freshness

External links (product pages, GitHub repos, community skills) were verified reachable at time of writing (2026-08) but may move or be taken down. If a link goes stale or a tool is discontinued, replace it by **capability**, not by exact brand — the methodology holds regardless. Please open a PR or issue if you find a dead link.