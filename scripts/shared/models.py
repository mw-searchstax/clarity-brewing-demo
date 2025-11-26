"""Pydantic models for SearchStax documents."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Location(BaseModel):
    """Taproom location for geo search."""

    id: str = Field(description="Stable ID: location:{slug}")
    name: str = Field(description="Display name")
    address: str
    city: str
    state: str
    zip_code: str = Field(alias="zip")
    country: str = "USA"
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    phone: Optional[str] = None
    hours: Optional[str] = None

    # SearchStax document type for faceting
    doc_type: str = "location"

    @field_validator("id", mode="before")
    @classmethod
    def ensure_location_prefix(cls, v: str) -> str:
        if not v.startswith("location:"):
            return f"location:{v}"
        return v

    def to_solr_doc(self) -> dict:
        """Convert to Solr document format."""
        doc = {
            "id": self.id,
            "name_t": self.name,
            "address_t": self.address,
            "city_t": self.city,
            "state_s": self.state,
            "zip_code_s": self.zip_code,
            "country_s": self.country,
            "lat_d": self.lat,
            "lng_d": self.lng,
            "doc_type_s": self.doc_type,
            # Geo point for spatial search
            "location_p": f"{self.lat},{self.lng}",
        }
        if self.phone:
            doc["phone_s"] = self.phone
        if self.hours:
            doc["hours_t"] = self.hours
        return doc


class InventoryItem(BaseModel):
    """Product stock at a location."""

    id: str = Field(description="Stable ID: inventory:{location_slug}:{product_slug}")
    location_id: str = Field(description="Reference: location:{slug}")
    product_id: str = Field(description="Reference: product:{slug}")
    stock_count: int = Field(ge=0)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    # SearchStax document type for faceting
    doc_type: str = "inventory"

    def to_solr_doc(self) -> dict:
        """Convert to Solr document format."""
        return {
            "id": self.id,
            "location_id_s": self.location_id,
            "product_id_s": self.product_id,
            "stock_count_i": self.stock_count,
            "in_stock_b": self.stock_count > 0,
            "last_updated_dt": self.last_updated.isoformat() + "Z",
            "doc_type_s": self.doc_type,
        }
