# Ingest API Scripts

Python scripts for ingesting supplemental data to SearchStax Site Search.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Add read-write credentials to `.env` (in project root):

```env
SEARCHSTAX_INGEST_URL=https://searchcloud-19-us-east-1.searchstax.com/29847/sitesearchdemo-7005/update
SEARCHSTAX_INGEST_TOKEN=your-read-write-token-here
```

Get the token from: SearchStax Dashboard → App Settings → All APIs → Search & Indexing

## Scripts

### ingest_locations.py

Ingests taproom locations for geo search.

```bash
# Dry run (validate only)
python ingest_locations.py --dry-run

# Ingest to SearchStax
python ingest_locations.py
```

### ingest_inventory.py

Ingests product stock counts by location.

```bash
# Dry run (validate only)
python ingest_inventory.py --dry-run

# Ingest to SearchStax
python ingest_inventory.py
```

## Data Files

- `data/locations.csv` - 5 taproom locations with addresses and coordinates
- `data/inventory.csv` - 65 inventory records (5 locations × 13 products)

## Document IDs

Scripts use stable, readable IDs:

- Locations: `location:taproom-austin`
- Inventory: `inventory:taproom-austin:hop-forward-ipa`

## Troubleshooting

**Config error: SEARCHSTAX_INGEST_URL is required**
- Ensure `.env` file exists in project root with the required variables

**API error (401): Unauthorized**
- Check that SEARCHSTAX_INGEST_TOKEN is a valid read-write token

**API error (429): Rate limited**
- Script will automatically retry with exponential backoff
