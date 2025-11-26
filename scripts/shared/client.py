"""SearchStax Ingest API client with retry logic."""

import json
import random
import time
from dataclasses import dataclass
from typing import Any

import requests

from .config import Config


@dataclass
class IngestResult:
    """Result of an ingest operation."""

    success: bool
    documents_sent: int
    response_data: dict | None = None
    error_message: str | None = None


class SearchStaxClient:
    """Client for the SearchStax Ingest API."""

    def __init__(self, config: Config):
        self.url = config.ingest_url
        self.token = config.ingest_token
        self.max_retries = 3
        self.base_delay = 1.0  # seconds

    def _should_retry(self, status_code: int) -> bool:
        """Determine if we should retry based on status code."""
        return status_code == 429 or status_code >= 500

    def _get_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter."""
        delay = self.base_delay * (2 ** attempt)
        jitter = delay * 0.2 * random.uniform(-1, 1)
        return delay + jitter

    def ingest(
        self,
        documents: list[dict],
        commit: bool = True,
        dry_run: bool = False,
    ) -> IngestResult:
        """Send documents to the SearchStax Ingest API.

        Args:
            documents: List of Solr documents to ingest
            commit: Whether to commit immediately (default True)
            dry_run: If True, validate but don't send (default False)

        Returns:
            IngestResult with success status and details
        """
        if not documents:
            return IngestResult(success=True, documents_sent=0)

        if dry_run:
            return IngestResult(
                success=True,
                documents_sent=len(documents),
                response_data={"dry_run": True, "would_send": len(documents)},
            )

        url = f"{self.url}?commit={str(commit).lower()}"
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    data=json.dumps(documents),
                    timeout=30,
                )

                if response.status_code == 200:
                    return IngestResult(
                        success=True,
                        documents_sent=len(documents),
                        response_data=response.json() if response.text else None,
                    )

                if self._should_retry(response.status_code) and attempt < self.max_retries:
                    delay = self._get_delay(attempt)
                    print(f"  API error ({response.status_code}): Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    continue

                # Non-retryable error or max retries exceeded
                return IngestResult(
                    success=False,
                    documents_sent=0,
                    error_message=f"HTTP {response.status_code}: {response.text[:500]}",
                )

            except requests.RequestException as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    delay = self._get_delay(attempt)
                    print(f"  Request error: {e}. Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    continue

        return IngestResult(
            success=False,
            documents_sent=0,
            error_message=f"Max retries exceeded. Last error: {last_error}",
        )
