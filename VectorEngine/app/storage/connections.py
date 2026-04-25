import weaviate
from weaviate.classes.init import Auth
from app.storage.config import WEAVIATE_URL, WEAVIATE_API_KEY

def get_client():
    """
    Initializes and returns a Weaviate client instance.
    """
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    )
    
    return client
