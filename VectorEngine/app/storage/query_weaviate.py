
# main_ingest.py
import requests
import json
import csv
import pandas as pd
import openai
from app.storage.connections import get_client
from app.storage.operations import  insert_objects_with_vectors , search_real_search_collection ,  search_real_search_collection_with_filters
# If you also have update_property, can import it similarly
from sentence_transformers import SentenceTransformer
from weaviate.classes.query import Filter


if __name__ == "__main__":
    # Example: Search for something specific
    user_query = "An apartment with more than 3 bedrooms and 1 bathroom , with 2 floors and also have a sea view"
    data = search_real_search_collection(user_query, limit=3)
    print(f"\n\nRetrived data {data}")

    # Create the filter
    location_filter = Filter.by_property("nearestTown").equal("Wadduwa")
    data_2 =  search_real_search_collection_with_filters( query_text="beachfront property", filters=location_filter)
    print(f"\n\nRetrieved data with flters {data_2}")