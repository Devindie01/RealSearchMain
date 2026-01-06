
from app.storage.config import  WEAVIATE_URL , WEAVIATE_API_KEY

from weaviate import WeaviateClient

import weaviate
from weaviate.classes.init import Auth

def get_client():
    client = weaviate.connect_to_weaviate_cloud(
            cluster_url=WEAVIATE_URL,
            auth_credentials=weaviate.Auth.api_key(WEAVIATE_API_KEY),
         )
    return client
