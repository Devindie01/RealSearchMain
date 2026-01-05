import numpy as np
from dag.node import Node

class RecencyEmbeddingNode(Node):
    def execute(self, context):
        weight = context.intent.recency_weight
        vec = np.ones(384) * weight
        return vec / np.linalg.norm(vec)
