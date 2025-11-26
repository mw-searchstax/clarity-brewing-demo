import { defineCollection, z } from 'astro:content';

/**
 * Content Collections for Clarity Brewing Co
 *
 * These schemas define the frontmatter structure for each content type.
 * The fields are designed to support Site Search features:
 * - Faceting (style, category, event_type)
 * - Sorting (price, rating, publish_date, event_date)
 * - Multi-value facets (flavor_profile, tags)
 */

const products = defineCollection({
  type: 'content',
  schema: z.object({
    // Stable ID for Ingest API compatibility
    id: z.string(),
    title: z.string(),

    // Product details
    style: z.enum(['IPA', 'Lager', 'Stout', 'Pilsner', 'Wheat', 'Pale Ale', 'Porter', 'Amber']),
    flavor_profile: z.array(z.string()),  // Multi-value facet
    abv: z.number().min(0).max(0.5),       // 0.0% - 0.5% for NA beer
    calories: z.number().positive(),
    price: z.number().positive(),
    rating: z.number().min(1).max(5),

    // Availability
    available: z.boolean().default(true),

    // Media
    image: z.string().optional(),

    // SEO
    description: z.string(),
  }),
});

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    id: z.string(),
    title: z.string(),

    // Categorization
    category: z.enum([
      'Brewing Process',
      'Food & Pairing',
      'Health & Wellness',
      'News & Updates',
      'Recipes',
    ]),
    tags: z.array(z.string()),  // Multi-value facet

    // Metadata
    author: z.string(),
    publish_date: z.date(),
    reading_time: z.number().positive(),  // minutes

    // Media
    image: z.string().optional(),

    // SEO
    description: z.string(),
  }),
});

const events = defineCollection({
  type: 'content',
  schema: z.object({
    id: z.string(),
    title: z.string(),

    // Event details
    event_type: z.enum(['Tasting', 'Tour', 'Festival', 'Workshop', 'Release Party']),
    event_date: z.date(),
    end_date: z.date().optional(),

    // Location (references a location ID for geo search)
    location_id: z.string(),
    location_name: z.string(),  // Denormalized for display

    // Capacity and pricing
    capacity: z.number().positive(),
    price: z.number().min(0),  // 0 = free event

    // Media
    image: z.string().optional(),

    // SEO
    description: z.string(),
  }),
});

export const collections = {
  products,
  articles,
  events,
};
