# Portfolio Site Kit

A field-tested skill for building trilingual (English / Simplified Chinese / Traditional Chinese) portfolio and works-showcase static sites that work for both global and mainland-China audiences.

Distilled from a real, production portfolio: hand-written HTML/CSS/JS on Cloudflare Pages, zero frameworks, zero build step, heavy use of audio, video, embedded decks and long-form articles, all readable from both sides of the Great Firewall.

**This is not a template to clone. It is a methodology**: design rules, component specifications, dual-region media strategy, deployment discipline, an iteration cadence, and a pitfall list of 23 real-world failures, each recorded as *symptom → root cause → how to avoid*.

[简体中文版](README.zh-CN.md)

---

## What it solves

| Problem | This kit's answer |
|---|---|
| Overseas CDNs, fonts and cloud links break in mainland China | Full self-hosting discipline + dual-link strategy (overseas direct link + mainland mirror) |
| Videos that play abroad but not in China | `<video>` direct links (`raw=1`) for global users, embeddable mainland-platform iframes (`?embed`) for Chinese users, switched as whole blocks per language |
| Unreachable article links | Local HTML archive pattern: CSS, fonts and images all localised for CMS pages; assets-only for JS-driven scrollytelling |
| Chinese webfont payloads of several megabytes | Subset first by the site's actual character set, then split into unicode-range chunks |
| Stale CSS/JS after deploys | Cache-busting discipline: every content change bumps `?v=YYYYMMDD` |
| Multilingual sites drifting into divergent codebases | Single-DOM trilingual engine: inline dictionary + `data-i18n` + `?lang=` URLs + browser detection |
| Iteration chaos | Written iteration rounds: every change locked in a decision log before any code moves |

## Repository layout

```
├── SKILL.md                  Skill entry point: triggers, core principles, workflow, hard limits
├── references/
│   ├── 01-design-and-style.md    Design tokens + the "find your style" methodology
│   ├── 02-components.md          Component specs: topbar, cards, filters, players, tile fields, marquees
│   ├── 03-media-compat.md        Cross-region media compatibility (video / audio / web archives)
│   ├── 04-deploy-and-domain.md   Hosting, caching discipline, domain strategy, China reachability
│   ├── 05-structure-i18n.md      Folder structure + the trilingual mechanism
│   ├── 06-iteration.md           Iteration cadence and decision-log format
│   └── 07-pitfalls.md            23 pitfalls, each as symptom → root cause → avoidance
└── templates/                    Copy-paste component skeletons
    ├── trilingual.html           Trilingual engine (dictionary + setLang + width-locked scramble)
    ├── audio-player.html         Inline audio player (play / seek / time / download, single instance)
    ├── bgm.html                  Background-music singleton button
    ├── tile-field.html           Parameterised Metro live-tile background field
    ├── marquee.html              Infinite marquee (clone ×2 + wrap + drag + linked pause)
    └── regional-links.html       Dual-link pattern (raw=1 / ?embed / data-href-* / lazy embed)
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

### In TRAE (or any agent with skill support)

Copy this repository's contents into your skills directory, e.g.:

```
~/.trae-cn/skills/portfolio-site-kit/
├── SKILL.md
├── references/
└── templates/
```

The agent then invokes it when you ask to create, restructure or iterate a portfolio, works showcase, or media-rich static site.

### As plain reference documentation

The `references/` folder reads as a standalone handbook. Start with:

- `references/03-media-compat.md` if you care about cross-region media;
- `references/07-pitfalls.md` before and after every major change, as a checklist;
- `templates/` for the component skeletons, all dependency-free and self-documented.

## Suggested workflow for a new site

1. **Define the style**: collect reference screenshots the author loves, feed them to any image-capable agent, and get a personalised style demo (colour, type, motif, layout). Never copy an existing site.
2. **Fix the structure**: page list, assets layout, language mechanism. Structural changes are the most expensive to make later.
3. **Lay components**: copy from `templates/`, skin with the demo's tokens.
4. **Wire media**: dual links for video, self-hosted audio, local archives for articles. Do it all at once.
5. **Ship**: direct upload, `_headers`, robots, sitemap, og:image.
6. **Iterate in written rounds**, checking the pitfall list after each pass.

## What this kit deliberately omits

- No bundled framework, bundler or runtime: nothing to go stale.
- No design opinion beyond discipline: the visual identity comes from the author, not the kit.
- No brand-specific links: every URL in the docs is a generic placeholder (`overseas.example`, `mainland.example`).

## License

[MIT](LICENSE) · Copyright (c) 2026 IcarusYe12138

The methodology and code skeletons are free to reuse; the portfolio they were distilled from remains the author's own work.
