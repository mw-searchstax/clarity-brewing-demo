# Phase 4: Content Expansion Design

## Goals

1. Maximize search feature testing - ensure facets, filtering, and sorting have meaningful data
2. Test content length extremes - very short to very long content for search result rendering

## Products (Add 8, Total: 13)

| Beer | Style | Content Length | Edge Case |
|------|-------|----------------|-----------|
| Classic Pilsner | Pilsner | Medium | New style |
| Dark Roast Porter | Porter | Long | New style, complex flavors |
| Session Pale | Pale Ale | Very short (~50 words) | Minimal description |
| Oktoberfest Marzen | Amber | Medium | Seasonal, `available: false` |
| Breakfast Stout | Stout | Long | Premium price ($18.99) |
| Citrus Radler | Wheat | Short | Lower ABV (0.3%), budget price |
| Double Dry-Hopped IPA | IPA | Extra long | Most detailed product |
| Belgian Tripel | Pale Ale | Medium | Higher ABV (0.5%), complex |

**New flavor profiles:** coffee, chocolate, malty, crisp, spicy

**Rating spread:** Include 3.8 (lower) and 4.7+ (high) for sort testing

## Articles (Add 8, Total: 13)

| Article | Category | Content Length | Edge Case |
|---------|----------|----------------|-----------|
| Quick Serving Tips | Food & Pairing | Very short (~150 words) | Minimal content |
| Complete Guide to Beer Styles | Brewing Process | Extra long (2500+ words) | Longest article |
| NA Beer Myths Debunked | Health & Wellness | Medium | Listicle format |
| Summer Recipe: Beer Can Chicken | Recipes | Medium | Recipe steps |
| New Taproom Opening: Seattle | News & Updates | Short | Announcement |
| Hop Varieties Explained | Brewing Process | Long | Reference content |
| Holiday Gift Guide | News & Updates | Medium | Seasonal |
| Interview with Our Brewmaster | News & Updates | Long | Q&A format |

**New tags:** seasonal, beginner, advanced, interview, announcement, reference

**New authors:** Add 2-3 beyond "Brewmaster Sarah Chen"

**Reading times:** 2 minutes (quick tips) to 15 minutes (complete guide)

## Events (Add 8, Total: 11)

| Event | Type | Edge Case |
|-------|------|-----------|
| Weekly Brewery Tour | Tour | New type, recurring |
| Stout Tasting Night | Tasting | New type, evening |
| Seattle Grand Opening | Release Party | Far future (6 months) |
| Summer Beer Festival | Festival | Multi-day (3 days), capacity 500 |
| Brewing 101 Workshop | Workshop | Free (`price: 0`) |
| Hop Harvest Tour | Tour | Past event |
| New Year's Eve Party | Festival | Premium ($100), capacity 50 |
| Porter & Chocolate Pairing | Tasting | Intimate, food-focused |

**Locations:** Austin, Denver, Seattle (new)

**Capacity range:** 25 to 500

**Price range:** $0 to $100

**Date spread:** Past, current, 6+ months future

## Search Feature Coverage

After expansion:

- All 8 product styles populated
- All 5 article categories populated
- All 5 event types populated
- Multi-value facets (flavor_profile, tags) well exercised
- Numeric ranges (price, rating, capacity) with good spread

## Content Length Extremes

- **Shortest:** "Quick Serving Tips" (~150 words), "Session Pale" (~50 words)
- **Longest:** "Complete Guide to Beer Styles" (~2500 words), "Double Dry-Hopped IPA" (detailed)
