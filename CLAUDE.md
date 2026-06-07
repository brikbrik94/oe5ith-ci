# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

`oe5ith-ci` is the shared CI/design system and CSS library for all OE5ITH websites. It defines tokens, components, layouts, page types, and rules for consistent visual identity across all portals. No build step — files are CSS, HTML, and shell/Python scripts used directly.

## Architecture

### Core principle

`css/common.css` is the single source of truth for all design tokens (colors, spacing, radii, shadows, z-index, transitions). Every other CSS file depends on it and must be loaded after it.

### CSS loading order

1. `css/common.css` — tokens, reset, base layout (always first, always required)
2. `css/typography.css`, `css/badges.css`, `css/buttons.css`, `css/cards.css`
3. `css/topbar.css`, `css/sidebar.css`
4. `css/page.css`, `css/code-viewer.css`, `css/calendar.css`
5. `css/forms.css`, `css/coords.css`, `css/utils.css`, `css/modal.css`, `css/toast.css`
6. `css/service-dashboard.css`

Or use `css/index.css` to import all production components at once.

**`css/demo.css` is only for `components/` reference pages — never in production.**

### Key files

| File | Role |
|---|---|
| `css/common.css` | Token definitions — edit here to change any token globally |
| `css/index.css` | Master import for all production CSS |
| `docs/tokens.md` | Token reference documentation |
| `docs/for-coding-agents.md` | Binding rules for automated changes |
| `docs/page-types.md` | Which page layout to use |
| `docs/sidebar-types.md` | Which sidebar variant to use |
| `docs/usage.md` | CSS inclusion rules and examples |
| `components/` | Live-testable HTML reference pages for each component |

### Map pages (special case)

Map pages using Leaflet or MapLibre follow different layout rules: `css/page.css` is usually omitted, the map fills the main area directly, and MapLibre/Leaflet overrides live in `css/modal.css`. Never apply standard page layouts to map pages.

### CLI utilities

`scripts/cli/utils.sh` and `scripts/cli/utils.py` provide logging functions with CI token color mapping for shell and Python scripts. Source or import before using `log_header`, `log_step`, `log_info`, `log_success`, `log_warn`, `log_error`, `log_auth`, `log_debug`, `log_sep`.

## Mandatory rules for all changes

1. **Never hardcode values** — use CSS tokens for all colors, backgrounds, borders, radii, shadows, z-index, and transitions.
2. **No custom component classes** — reuse existing CI classes; only create new ones if no existing pattern fits.
3. **Check existing patterns first** — before any UI change, consult `docs/page-types.md`, `docs/sidebar-types.md`, and `components/` for a matching pattern.
4. **New patterns require documentation first** — add spec in `docs/`, reference HTML in `components/`, then CSS in `css/`.
5. **New tokens** belong in `css/common.css` (definition) and `docs/tokens.md` (documentation). Only add tokens for values used multiple times or with clear semantic meaning.
6. **Never change paths** (CSS, asset, font, API, domain) without an explicit request.
7. **No structural changes without reason** — renaming files, reorganizing folders, splitting or merging CSS files requires explicit instruction.
8. **Register new components** — every new component/feature needs an entry in `docs/registry.json`; run `python3 scripts/cli/check_consistency.py` and ensure it passes. See `docs/for-coding-agents.md`.

## Versioning and changelog

Semantic versioning via Git tags (`vMAJOR.MINOR.PATCH`). Filenames never include version numbers.

- MAJOR: breaking changes (removed/renamed classes or tokens, incompatible HTML structure changes)
- MINOR: backwards-compatible additions (new component, new token, new docs)
- PATCH: bug fixes, typo corrections, doc updates

Update `CHANGELOG.md` with categories `Added`, `Changed`, `Fixed`, `Removed`, `Breaking` before tagging a release. Tag with:

```bash
git tag -a v1.x.x -m "Release v1.x.x"
git push origin v1.x.x
```

## Pre-change checklist

- [ ] `css/common.css` remains source of truth
- [ ] No hardcoded colors or z-index values
- [ ] No production page uses `css/demo.css`
- [ ] Existing components reused where applicable
- [ ] New components documented
- [ ] New tokens added to `css/common.css` and `docs/tokens.md`
- [ ] No paths or deploy structures changed unintentionally
- [ ] Map pages treated as special case
