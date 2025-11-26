# Clarity Brewing Co - Site Search Demo

A demo website for testing SearchStax Site Search features. Built with Astro + React.

## Quick Start

```bash
npm install
npm run dev
# Open http://localhost:4321/en/
```

## Project Overview

This is a fictional non-alcoholic brewery website designed to exercise ~80% of Site Search features:

- **Multi-language support** (EN now, ES/DE/ZH_CN in Phase 6)
- **Multiple content types** for faceted search
- **Crawler + Ingest API** data sources
- **Search profiles** for different sections
- **Geo search** for store locator

## Current Status: Phase 4 Complete ✅

### What's Built

| Content Type | Count | Location |
|--------------|-------|----------|
| Products (beers) | 13 | `src/content/products/` |
| Articles | 13 | `src/content/articles/` |
| Events | 11 | `src/content/events/` |

### Pages

- `/en/` - Homepage with featured content
- `/en/products/` - Beer catalog with style filtering
- `/en/products/[slug]/` - Product detail pages
- `/en/articles/` - Articles with category filtering
- `/en/articles/[slug]/` - Article detail pages
- `/en/events/` - Event listings (upcoming/past)
- `/en/events/[slug]/` - Event detail pages
- `/en/search/` - SearchStax Site Search integration

### Search Integration (Phase 2) ✅

- **Deployed to**: [clarity-brewing-demo.pages.dev](https://clarity-brewing-demo.pages.dev/en/)
- **Search SDK**: `@searchstax-inc/searchstudio-ux-js` (vanilla JS)
- **Widgets**: Search input, results, facets, pagination, sorting

#### Environment Variables (Cloudflare Pages)

```env
PUBLIC_SEARCHSTAX_SEARCH_URL=https://your-app.searchstax.com/solr/collection/emselect
PUBLIC_SEARCHSTAX_SUGGEST_URL=https://your-app.searchstax.com/solr/collection/emsuggest
PUBLIC_SEARCHSTAX_TOKEN=your-read-only-token
PUBLIC_SEARCHSTAX_TRACK_KEY=your-tracking-key
```

#### Notes

- Using vanilla JS package instead of React wrapper due to React 19 compatibility issues
- CSS copied to `public/searchstax.css` (package doesn't export styles)
- Facets will populate once configured in SearchStax dashboard

---

## Phase 3: Search Page Polish ✅

- [x] Polish search page CSS styling (overrode SearchStax orange with site green)
- [x] Hide empty facets sidebar when no facets available

---

## Phase 4: Expand Content ✅

- [x] Add more products (8 new beers, total 13)
- [x] Add more articles (8 new articles, total 13)
- [x] Add more events (8 new events, total 11)

See `docs/plans/2025-11-26-phase4-content-expansion-design.md` for design details.

---

## Phase 5: Ingest API Scripts

Add Python scripts for supplemental data (locations not on website):

```
scripts/
├── ingest_locations.py   # Taproom locations (geo search)
├── ingest_inventory.py   # Product availability
└── shared/
    ├── config.py
    ├── batch_accumulator.py
    └── retry_handler.py
```

### Key Patterns

1. **Stable IDs**: `type:slug` pattern (e.g., `location:taproom-austin`)
2. **Size-based batching**: ~1800KB target per request (2048KB limit)
3. **Retry with backoff**: Exponential delay + jitter for 429/5xx
4. **Environment config**: `STAGING_` prefix for non-prod

---

## Phase 6: Multilingual

Add languages to `astro.config.mjs`:

```js
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'es', 'de', 'zh-cn'],
  routing: {
    prefixDefaultLocale: true,
  },
},
```

Create translated content in `src/content/*/` directories with language-specific files.

---

## Phase 7: SearchStax Configuration (Dashboard)

All dashboard configuration work:

- [ ] Configure facets in SearchStax dashboard
- [ ] Set up search profiles (products, articles, events)
- [ ] Configure Smart Answers
- [ ] Promotions and merchandising
- [ ] Related searches
- [ ] Custom synonyms and stopwords
- [ ] Analytics tracking

---

## Content Schema

### Products

```yaml
id: "product:slug"        # Stable ID for search
title: string
style: IPA | Lager | Stout | Pilsner | Wheat | Pale Ale | Porter | Amber
flavor_profile: string[]  # Multi-value facet
abv: number              # 0.0 - 0.5
calories: number
price: number
rating: number           # 1-5
available: boolean
description: string
```

### Articles

```yaml
id: "article:slug"
title: string
category: Brewing Process | Food & Pairing | Health & Wellness | News & Updates | Recipes
tags: string[]           # Multi-value facet
author: string
publish_date: date
reading_time: number     # minutes
description: string
```

### Events

```yaml
id: "event:slug"
title: string
event_type: Tasting | Tour | Festival | Workshop | Release Party
event_date: date
end_date: date?
location_id: string      # References location for geo search
location_name: string
capacity: number
price: number            # 0 = free
description: string
```

---

## Tech Stack

- **Framework**: Astro 5 with React islands
- **Styling**: CSS custom properties (no framework)
- **Content**: Astro Content Collections with Zod schemas
- **Search**: SearchStax Site Search (Phase 2+)
- **Hosting**: Cloudflare Pages (recommended)

## Commands

| Command | Action |
|---------|--------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server at localhost:4321 |
| `npm run build` | Build production site to ./dist/ |
| `npm run preview` | Preview production build |

## Deployment

### Cloudflare Pages

1. Connect your Git repo to Cloudflare Pages
2. Build command: `npm run build`
3. Output directory: `dist`

Or manually:

```bash
npm run build
# Upload dist/ to Cloudflare Pages
```

---

## License

Demo project for SearchStax Site Search testing.
