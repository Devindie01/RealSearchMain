from typing import List, Optional, Union
import numpy as np
from PIL import Image
from app.encoders.image import ImageEncoder

class ImageSpace:
    """
    Space for handling a property’s list of images.
    Converts each image to a vector using ImageEncoder and combines them.
    """
    def __init__(
        self,
        images: Optional[List[Union[str, Image.Image]]] = None,
        model_name: str = "clip-ViT-B-32",
        weight: float = 1.0,
    ):
        self.images = images or []
        self.weight = weight
        self.encoder = ImageEncoder(model_name)

    def encode(self, property_obj) -> np.ndarray:
        """
        Encodes all images of a property and returns a combined vector.
        property_obj must have an attribute 'images' which is a list of paths or PIL.Images.
        """
        images = getattr(property_obj, "images", [])
        if not images:
            # return a zero vector of reasonable size if no images
            # (assumes model embedding size of 512 for CLIP, can be adjusted)
            return np.zeros(512) * self.weight

        vectors = [self.encoder.encode(img) for img in images]
        combined = np.mean(vectors, axis=0)  # mean pooling
        return combined * self.weight
