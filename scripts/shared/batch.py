"""Size-based batching for SearchStax Ingest API."""

import json
from typing import Iterator


class BatchAccumulator:
    """Accumulate documents into size-limited batches.

    The SearchStax Ingest API has a 2048KB limit per request.
    We target 1800KB to leave buffer for JSON formatting overhead.
    """

    def __init__(self, target_size_kb: int = 1800):
        self.target_size = target_size_kb * 1024
        self.current_batch: list[dict] = []
        self.current_size = 0

    def _doc_size(self, doc: dict) -> int:
        """Calculate JSON size of a document."""
        return len(json.dumps(doc))

    def add(self, document: dict) -> list[dict] | None:
        """Add a document to the current batch.

        Returns the batch if adding this document would exceed the target size.
        The document is added to the next batch.
        """
        doc_size = self._doc_size(document)

        # If this single doc is too large, we have a problem
        if doc_size > self.target_size:
            raise ValueError(
                f"Document too large: {doc_size} bytes > {self.target_size} bytes. "
                f"Document ID: {document.get('id', 'unknown')}"
            )

        # Check if adding this doc would exceed target
        if self.current_size + doc_size > self.target_size and self.current_batch:
            batch = self.current_batch
            self.current_batch = [document]
            self.current_size = doc_size
            return batch

        self.current_batch.append(document)
        self.current_size += doc_size
        return None

    def flush(self) -> list[dict]:
        """Return any remaining documents in the current batch."""
        batch = self.current_batch
        self.current_batch = []
        self.current_size = 0
        return batch


def batched(documents: list[dict], target_size_kb: int = 1800) -> Iterator[list[dict]]:
    """Yield batches of documents that fit within the size limit."""
    accumulator = BatchAccumulator(target_size_kb)

    for doc in documents:
        batch = accumulator.add(doc)
        if batch:
            yield batch

    # Don't forget the last batch
    final = accumulator.flush()
    if final:
        yield final
