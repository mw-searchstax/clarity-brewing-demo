#!/usr/bin/env python3
"""Ingest taproom locations to SearchStax for geo search."""

import argparse
import csv
import sys
from pathlib import Path

from pydantic import ValidationError

from shared.batch import batched
from shared.client import SearchStaxClient
from shared.config import load_config
from shared.models import Location


def load_locations(csv_path: Path) -> list[Location]:
    """Load and validate locations from CSV."""
    locations = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert lat/lng to float
            row["lat"] = float(row["lat"])
            row["lng"] = float(row["lng"])
            # Use slug as id
            row["id"] = row.pop("slug")

            location = Location.model_validate(row)
            locations.append(location)

    return locations


def main():
    parser = argparse.ArgumentParser(description="Ingest locations to SearchStax")
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
    csv_path = script_dir / "data" / "locations.csv"

    print(f"Reading {csv_path}...")
    try:
        locations = load_locations(csv_path)
    except FileNotFoundError:
        print(f"✗ File not found: {csv_path}")
        sys.exit(1)
    except ValidationError as e:
        print(f"✗ Validation error: {e}")
        sys.exit(1)

    print(f"Found {len(locations)} locations")
    print("Validating documents...")

    # Convert to Solr documents
    documents = [loc.to_solr_doc() for loc in locations]

    if args.dry_run:
        print("\n[DRY RUN] Would send:")
        for doc in documents:
            print(f"  - {doc['id']}: {doc['name_t']}")
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
