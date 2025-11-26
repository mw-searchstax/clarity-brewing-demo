#!/usr/bin/env python3
"""Ingest product inventory by location to SearchStax."""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

from pydantic import ValidationError

from shared.batch import batched
from shared.client import SearchStaxClient
from shared.config import load_config
from shared.models import InventoryItem


def load_inventory(csv_path: Path) -> list[InventoryItem]:
    """Load and validate inventory from CSV."""
    items = []
    now = datetime.utcnow()

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            location_slug = row["location_slug"]
            product_slug = row["product_slug"]

            item = InventoryItem(
                id=f"inventory:{location_slug}:{product_slug}",
                location_id=f"location:{location_slug}",
                product_id=f"product:{product_slug}",
                stock_count=int(row["stock_count"]),
                last_updated=now,
            )
            items.append(item)

    return items


def main():
    parser = argparse.ArgumentParser(description="Ingest inventory to SearchStax")
    parser.add_argument("--dry-run", action="store_true", help="Validate without sending")
    args = parser.parse_args()

    print("Loading config from environment...")
    try:
        config = load_config()
    except ValueError as e:
        print(f"✗ Config error: {e}")
        sys.exit(1)

    # Find data file relative to script location
    script_dir = Path(__file__).parent
    csv_path = script_dir / "data" / "inventory.csv"

    print(f"Reading {csv_path}...")
    try:
        items = load_inventory(csv_path)
    except FileNotFoundError:
        print(f"✗ File not found: {csv_path}")
        sys.exit(1)
    except ValidationError as e:
        print(f"✗ Validation error: {e}")
        sys.exit(1)

    print(f"Found {len(items)} inventory records")
    print("Validating documents...")

    # Convert to Solr documents
    documents = [item.to_solr_doc() for item in items]

    # Summary stats
    in_stock = sum(1 for item in items if item.stock_count > 0)
    out_of_stock = len(items) - in_stock
    print(f"  In stock: {in_stock}, Out of stock: {out_of_stock}")

    if args.dry_run:
        print("\n[DRY RUN] Sample documents:")
        for doc in documents[:5]:
            print(f"  - {doc['id']}: {doc['stock_count_i']} units")
        print(f"  ... and {len(documents) - 5} more")
        print(f"\n✓ Dry run complete: {len(documents)} documents validated")
        return

    # Ingest in batches
    client = SearchStaxClient(config)
    total_sent = 0

    for i, batch in enumerate(batched(documents), 1):
        batch_size_kb = sum(len(str(d)) for d in batch) / 1024
        print(f"Ingesting batch {i} ({len(batch)} documents, {batch_size_kb:.1f}KB)...")

        result = client.ingest(batch)

        if result.success:
            total_sent += result.documents_sent
        else:
            print(f"✗ API error: {result.error_message}")
            sys.exit(1)

    print(f"✓ Success: {total_sent} documents ingested")


if __name__ == "__main__":
    main()
