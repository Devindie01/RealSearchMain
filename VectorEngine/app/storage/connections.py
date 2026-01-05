import weaviate
import app.storage.config as config
from weaviate.auth import Auth


# def get_client() -> Client:
#     """
#     Returns a Weaviate client connected to the specified endpoint.
#     """
#     client = Client(
#         url=config.WEAVIATE_URL,
#         additional_headers=(
#             {"X-API-KEY": config.WEAVIATE_API_KEY} if config.WEAVIATE_API_KEY else {}
#         ),
#     )
#     return client


def get_client() -> weaviate.WeaviateClient:
    """
    Returns a Weaviate v4 client connected to the specified endpoint.
    """
    # If config.WEAVIATE_URL is something like "https://your-cluster.weaviate.network"
    # we use the connect_to_weaviate_cloud helper.

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=config.WEAVIATE_URL,
        auth_credentials=(
            Auth.api_key(config.WEAVIATE_API_KEY) if config.WEAVIATE_API_KEY else None
        ),
        # Optional: Add external API keys (like OpenAI) for on-the-fly vectorization
        # headers={"X-OpenAI-Api-Key": config.OPENAI_API_KEY}
    )
    return client
