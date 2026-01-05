import numpy as np
from dag.node import Node

class TextEmbeddingNode(Node):
    def execute(self, context):
        # Replace with SentenceTransformer
        vec = np.random.rand(384)
        return vec / np.linalg.norm(vec)
