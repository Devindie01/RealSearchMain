from weaviate import Client
from app.storage.config import config

def get_client() -> Client:
    """
    Returns a Weaviate client connected to the specified endpoint.
    """
    client = Client(
        url=config.WEAVIATE_URL,
        additional_headers={"X-API-KEY": config.WEAVIATE_API_KEY} if config.WEAVIATE_API_KEY else {}
    )
    return client
