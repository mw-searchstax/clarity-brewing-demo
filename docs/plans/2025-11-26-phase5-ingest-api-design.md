# Phase 5: Ingest API Scripts Design

## Goals

1. Demo the SearchStax Ingest API feature with runnable Python scripts
2. Production-quality structure that could scale to real use
3. Add supplemental data not on the website (locations, inventory)

## Project Structure

```
scripts/
├── ingest_locations.py      # Taproom locations → geo search
├── ingest_inventory.py      # Stock counts per location
├── shared/
│   ├── __init__.py
│   ├── config.py            # Environment config + validation
│   ├── client.py            # SearchStax API client
│   ├── batch.py             # Size-based batching (1800KB target)
│   └── models.py            # Pydantic models for all document types
├── data/
│   ├── locations.csv        # 5 fictional taproom locations
│   └── inventory.csv        # Product stock by location
├── requirements.txt         # requests, pydantic, python-dotenv
└── README.md                # Usage instructions
```

## Environment Variables

Add to `.env` (read-write credentials, server-side only):

```env
SEARCHSTAX_INGEST_URL=https://searchcloud-19-us-east-1.searchstax.com/29847/sitesearchdemo-7005/update
SEARCHSTAX_INGEST_TOKEN=your-read-write-token-here
```

Get the read-write token from: SearchStax Dashboard → App Settings → All APIs → Search & Indexing

## Data Models

### Location (for geo search)

```python
class Location(BaseModel):
    id: str                    # "location:taproom-austin"
    name: str                  # "Clarity Brewing - Austin"
    address: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    lat: float                 # For geo search
    lng: float
    phone: str | None = None
    hours: str | None = None   # "Mon-Sat 11am-10pm, Sun 12pm-8pm"
```

### Inventory (stock per location)

```python
class InventoryItem(BaseModel):
    id: str                    # "inventory:taproom-austin:hop-forward-ipa"
    location_id: str           # Reference to location
    product_id: str            # Reference to product
    stock_count: int           # 0 = out of stock
    last_updated: datetime
```

### ID Patterns

- `location:taproom-austin` - stable, readable
- `inventory:taproom-austin:hop-forward-ipa` - composite key for product-location matrix

## API Client

### SearchStax Ingest API

- Endpoint: `/update?commit=true`
- Auth: `Authorization: Token [token]` header
- Format: JSON array of documents
- Limit: 2048KB max per request

Reference: https://www.searchstax.com/docs/searchstudio/searchstax-studio-ingest-api/

### Batching Strategy

- Target 1800KB per batch (buffer under 2048KB limit)
- Calculate JSON size as documents are added
- Flush when approaching limit or at end

### Retry Logic

- Exponential backoff: 1s, 2s, 4s, 8s (max 3 retries)
- Jitter: ±20% randomization to prevent thundering herd
- Retry on: 429 (rate limit), 5xx (server errors)
- Fail on: 4xx (client errors - bad data)

## Sample Data

### data/locations.csv

| slug | name | address | city | state | zip | lat | lng | phone | hours |
|------|------|---------|------|-------|-----|-----|-----|-------|-------|
| taproom-austin | Clarity Brewing - Austin | 123 Main St | Austin | TX | 78701 | 30.2672 | -97.7431 | 512-555-0100 | Mon-Sat 11am-10pm, Sun 12pm-8pm |
| taproom-denver | Clarity Brewing - Denver | 456 Market St | Denver | CO | 80202 | 39.7392 | -104.9903 | 303-555-0200 | Mon-Sun 11am-11pm |
| taproom-seattle | Clarity Brewing - Seattle | 789 Pike St | Seattle | WA | 98101 | 47.6062 | -122.3321 | 206-555-0300 | Mon-Sat 12pm-10pm |
| taproom-portland | Clarity Brewing - Portland | 321 Oak Ave | Portland | OR | 97204 | 45.5152 | -122.6784 | 503-555-0400 | Tue-Sun 11am-9pm |
| taproom-san-diego | Clarity Brewing - San Diego | 654 Harbor Dr | San Diego | CA | 92101 | 32.7157 | -117.1611 | 619-555-0500 | Mon-Sun 10am-10pm |

### data/inventory.csv

Cross-product of locations × products with stock counts:

| location_slug | product_slug | stock_count |
|---------------|--------------|-------------|
| taproom-austin | hop-forward-ipa | 24 |
| taproom-austin | golden-lager | 48 |
| taproom-austin | midnight-stout | 0 |
| ... | ... | ... |

The inventory script reads product slugs from `src/content/products/` to build the full matrix.

## Script Behavior

### Usage

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Ingest locations
python scripts/ingest_locations.py

# Ingest inventory
python scripts/ingest_inventory.py

# Dry run (validate + show what would be sent)
python scripts/ingest_locations.py --dry-run
```

### Output

```
Loading config from environment...
Reading data/locations.csv...
Found 5 locations
Validating documents...
Ingesting batch 1/1 (5 documents, 2.3KB)...
✓ Success: 5 documents ingested
```

### Error Handling

```
✗ Validation error: Location 'taproom-austin' missing required field 'lat'
✗ API error (429): Rate limited, retrying in 2.1s...
✗ API error (400): Bad request - {"error": "unknown field 'foo'"}
```

## Dependencies

```
# scripts/requirements.txt
requests>=2.31.0
pydantic>=2.5.0
python-dotenv>=1.0.0
```

## Search Feature Coverage

After Phase 5:

- **Geo search**: 5 taproom locations with lat/lng coordinates
- **Availability filtering**: Stock counts per product per location
- **Ingest API demo**: Complete example of pushing data via API
