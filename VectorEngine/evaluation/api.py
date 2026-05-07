"""
api.py  —  Property Search Backend
Place this file in the same directory as evaluator.py
Run with: uvicorn api:app --reload --port 8000

Expects a CSV named 'property_data.csv' in the same directory with columns:
  Property_id, Title, Property type, Contract Type, Price_LKR,
  Price_in_other_currency, Other_currency, Price_LKR_per_unit, Unit_type,
  Other_curr_val_per_unit, Other_currency_per_unit, Bedrooms, Bathrooms,
  Land Size, Land_size_unit, Floor_area_sqft, Location, Latitude, Longitude,
  Nearest Town, Amenities, Description, Links to Image, Map Link, Full Description
"""

import sys
import os
import csv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from tests.pipeline import run_pipeline_test
from app.storage.connections import get_client

# ── Load env ──────────────────────────────────────────────────────────────────
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", "app", ".env")
load_dotenv(dotenv_path=env_path)

# ── Load CSV into memory at startup ───────────────────────────────────────────
CSV_PATH = os.path.join(current_dir, "property_data.csv")

def load_property_csv(path: str) -> dict:
    """Load CSV and index rows by Property_id (string) for O(1) lookup."""
    index = {}
    if not os.path.exists(path):
        print(f"⚠️  WARNING: {path} not found — property detail lookups will return empty cards.")
        return index
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = str(row.get("Property_id", "")).strip()
            if pid:
                index[pid] = row
    print(f"✅ Loaded {len(index)} properties from CSV")
    return index

PROPERTY_INDEX: dict = load_property_csv(CSV_PATH)


# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(title="Property Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request schema ─────────────────────────────────────────────────────────────
class SearchRequest(BaseModel):
    query: str
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[float] = None


# ── Build enriched query string ────────────────────────────────────────────────
def build_query(req: SearchRequest) -> str:
    parts = [req.query.strip()]
    if req.price_min is not None and req.price_max is not None:
        parts.append(f"The price should be between {req.price_min:,.0f} and {req.price_max:,.0f} LKR.")
    elif req.price_min is not None:
        parts.append(f"The price should be at least {req.price_min:,.0f} LKR.")
    elif req.price_max is not None:
        parts.append(f"The price should be at most {req.price_max:,.0f} LKR.")
    if req.bedrooms is not None:
        parts.append(f"It should have {req.bedrooms} bedroom(s).")
    if req.bathrooms is not None:
        parts.append(f"It should have {req.bathrooms} bathroom(s).")
    if req.area is not None:
        parts.append(f"The floor area should be around {req.area:,.0f} square feet.")
    return " ".join(parts)


# ── Map a CSV row to a clean dict for the frontend ────────────────────────────
def row_to_property(pid: str, row: dict) -> dict:
    def val(key):
        return (row.get(key) or "").strip()

    def num(key):
        v = val(key).replace(",", "")
        try:
            return float(v) if "." in v else int(v)
        except (ValueError, TypeError):
            return None

    # Combined price string: LKR + other currency if present
    price_lkr = num("Price_LKR")
    other_curr_val = val("Price_in_other_currency")
    other_curr_sym = val("Other_currency")
    price_display = None
    if price_lkr is not None:
        price_display = f"LKR {price_lkr:,.0f}"
        if other_curr_val and other_curr_sym:
            price_display += f"  ·  {other_curr_sym} {other_curr_val}"

    # Land size with unit
    land = val("Land Size")
    land_unit = val("Land_size_unit")
    land_display = f"{land} {land_unit}".strip() if land else None

    return {
        "property_id":     pid,
        "title":           val("Title") or f"Property {pid}",
        "property_type":   val("Property type"),
        "contract_type":   val("Contract Type"),
        "price":           price_lkr,
        "price_display":   price_display,
        "bedrooms":        num("Bedrooms"),
        "bathrooms":       num("Bathrooms"),
        "floor_area_sqft": num("Floor_area_sqft"),
        "land_size":       land_display,
        "location":        val("Location"),
        "nearest_town":    val("Nearest Town"),
        "latitude":        num("Latitude"),
        "longitude":       num("Longitude"),
        "amenities":       val("Amenities"),
        "description":     val("Full Description") or val("Description"),
        "image_url":       val("Links to Image"),
        "map_link":        val("Map Link"),
    }


# ── Resolve IDs against CSV ────────────────────────────────────────────────────
def fetch_properties_from_csv(property_ids: list) -> list:
    results = []
    for pid in property_ids:
        key = str(pid).strip()
        row = PROPERTY_INDEX.get(key)
        if row:
            results.append(row_to_property(key, row))
        else:
            print(f"  ⚠️  Property ID {key} not found in CSV")
            results.append({
                "property_id": key, "title": f"Property {key}",
                "property_type": "", "contract_type": "",
                "price": None, "price_display": None,
                "bedrooms": None, "bathrooms": None,
                "floor_area_sqft": None, "land_size": None,
                "location": "", "nearest_town": "",
                "latitude": None, "longitude": None,
                "amenities": "", "description": "",
                "image_url": "", "map_link": "",
            })
    return results

# ── Search endpoint ────────────────────────────────────────────────────────────
@app.post("/search")
def search(req: SearchRequest):
    enriched_query = build_query(req)
    print(f"\n🔎 Enriched query: {enriched_query}")

    try:
        with get_client() as client:
            # retrieved_ids = run_pipeline_test(enriched_query,req.price_min, req.price_max, req.bedrooms, req.bathrooms, req.area, client)
            retrieved_ids = run_pipeline_test(
                user_query=req.query,
                price_min=req.price_min,
                price_max=req.price_max,
                bedrooms=req.bedrooms,
                bathrooms=req.bathrooms,
                area=req.area,
                client=client,
            )
        if isinstance(retrieved_ids, dict):
            retrieved_ids = retrieved_ids.get("ids", [])
        if not retrieved_ids:
            return {"query": enriched_query, "count": 0, "results": []}

        print(f"  → Retrieved IDs: {retrieved_ids}")
        properties = fetch_properties_from_csv(retrieved_ids)

        return {
            "query": enriched_query,
            "count": len(properties),
            "results": properties,
        }

    except Exception as e:
        print(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Serve the frontend ─────────────────────────────────────────────────────────
@app.get("/")
def serve_frontend():
    html_path = os.path.join(current_dir, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    raise HTTPException(status_code=404, detail="index.html not found")


@app.get("/health")
def health():
    return {"status": "ok", "properties_loaded": len(PROPERTY_INDEX)}
