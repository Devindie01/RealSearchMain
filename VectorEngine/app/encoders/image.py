from sentence_transformers import SentenceTransformer
import numpy as np
from PIL import Image
from typing import Union

class ImageEncoder:
    """
    Encodes a single image (PIL.Image or image path) into a vector embedding.
    """
    def __init__(self, model_name: str = "clip-ViT-B-32"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, image: Union[str, Image.Image]) -> np.ndarray:
        """
        Accepts an image path or PIL.Image, returns a vector embedding.
        """
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        elif not isinstance(image, Image.Image):
            raise ValueError("Image must be a PIL.Image or path string")
        return np.array(self.model.encode(image))
