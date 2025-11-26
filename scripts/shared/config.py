"""Environment configuration for SearchStax Ingest API."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    """SearchStax Ingest API configuration."""

    ingest_url: str
    ingest_token: str

    def __post_init__(self):
        if not self.ingest_url:
            raise ValueError("SEARCHSTAX_INGEST_URL is required")
        if not self.ingest_token:
            raise ValueError("SEARCHSTAX_INGEST_TOKEN is required")
        if not self.ingest_url.endswith("/update"):
            raise ValueError("SEARCHSTAX_INGEST_URL must end with /update")


def load_config() -> Config:
    """Load configuration from environment variables.

    Reads from .env file in project root, then environment variables.
    """
    # Load .env from project root (parent of scripts/)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    load_dotenv(os.path.join(project_root, ".env"))

    return Config(
        ingest_url=os.getenv("SEARCHSTAX_INGEST_URL", ""),
        ingest_token=os.getenv("SEARCHSTAX_INGEST_TOKEN", ""),
    )
