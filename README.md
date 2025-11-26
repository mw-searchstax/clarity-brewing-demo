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

- **Multi-language support** (EN now, ES/DE/ZH_CN in Phase 4)
- **Multiple content types** for faceted search
- **Crawler + Ingest API** data sources
- **Search profiles** for different sections
- **Geo search** for store locator

## Current Status: Phase 1 Complete ✅

### What's Built

| Content Type | Count | Location |
|--------------|-------|----------|
| Products (beers) | 5 | `src/content/products/` |
| Articles | 5 | `src/content/articles/` |
| Events | 3 | `src/content/events/` |

### Pages

- `/en/` - Homepage with featured content
- `/en/products/` - Beer catalog with style filtering
- `/en/products/[slug]/` - Product detail pages
- `/en/articles/` - Articles with category filtering
- `/en/articles/[slug]/` - Article detail pages
- `/en/events/` - Event listings (upcoming/past)
- `/en/events/[slug]/` - Event detail pages
- `/en/search/` - Placeholder for SearchStax integration

---

## Phase 2: Search Integration

### Prerequisites

1. Create a Site Search App at [searchstax.com](https://www.searchstax.com)
2. Deploy this site to Cloudflare Pages (or similar)
3. Configure the crawler to index the deployed site

### Implementation Steps

#### 1. Install SearchStax UI Kit

```bash
npm install @searchstax-inc/searchstudio-ux-react
```

#### 2. Get API Credentials

From Site Search dashboard:
- **Search URL**: `https://{app-id}.searchstax.com/solr/{collection}/emselect`
- **Suggest URL**: `https://{app-id}.searchstax.com/solr/{collection}/emsuggest`
- **Read-Only Token**: From App Settings > All APIs > Search & Indexing
- **Tracking API Key**: From App Settings > All APIs > Analytics

#### 3. Create Search Component

Create `src/components/SearchInterface.tsx`:

```tsx
import {
  SearchstaxWrapper,
  SearchstaxInputWidget,
  SearchstaxResultWidget,
  SearchstaxFacetsWidget,
  SearchstaxPaginationWidget,
  SearchstaxSortingWidget,
} from '@searchstax-inc/searchstudio-ux-react';
import '@searchstax-inc/searchstudio-ux-react/dist/styles/mainTheme.css';

const config = {
  searchURL: import.meta.env.PUBLIC_SEARCHSTAX_SEARCH_URL,
  suggesterURL: import.meta.env.PUBLIC_SEARCHSTAX_SUGGEST_URL,
  searchAuth: import.meta.env.PUBLIC_SEARCHSTAX_TOKEN,
  trackApiKey: import.meta.env.PUBLIC_SEARCHSTAX_TRACK_KEY,
  authType: 'token',
  language: 'en',
};

export default function SearchInterface() {
  return (
    <SearchstaxWrapper config={config}>
      <SearchstaxInputWidget />
      <div className="search-layout">
        <aside className="search-sidebar">
          <SearchstaxFacetsWidget />
        </aside>
        <main className="search-results">
          <SearchstaxSortingWidget />
          <SearchstaxResultWidget />
          <SearchstaxPaginationWidget />
        </main>
      </div>
    </SearchstaxWrapper>
  );
}
```

#### 4. Create Environment File

Create `.env`:

```env
PUBLIC_SEARCHSTAX_SEARCH_URL=https://your-app.searchstax.com/solr/collection/emselect
PUBLIC_SEARCHSTAX_SUGGEST_URL=https://your-app.searchstax.com/solr/collection/emsuggest
PUBLIC_SEARCHSTAX_TOKEN=your-read-only-token
PUBLIC_SEARCHSTAX_TRACK_KEY=your-tracking-key
```

#### 5. Update Search Page

Update `src/pages/en/search.astro` to use the React component:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import SearchInterface from '../../components/SearchInterface.tsx';
---

<BaseLayout title="Search">
  <h1>Search</h1>
  <SearchInterface client:load />
</BaseLayout>
```

#### 6. Configure Search Profiles

In Site Search dashboard, create profiles:

| Profile | Data Filter | Purpose |
|---------|-------------|---------|
| Default | (none) | Global search |
| Products | `content_type:product` | Beer catalog |
| Articles | `content_type:article` | Knowledge base |
| Events | `content_type:event` | Event finder |

---

## Phase 3: Ingest API

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

## Phase 4: Multilingual

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

## Phase 5: Advanced Features

- Smart Answers configuration
- Promotions and merchandising
- Related searches
- Custom synonyms and stopwords
- Analytics tracking

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
