
from app.storage.config import  WEAVIATE_URL , WEAVIATE_API_KEY

from weaviate import WeaviateClient

import weaviate
from weaviate.classes.init import Auth

def get_client():
    client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=weaviate_api_key,
         )
    return client
