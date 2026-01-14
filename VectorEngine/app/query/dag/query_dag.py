from aggregation.weighted_sum import WeightedSumAggregator

class QueryDAG:
    def __init__(self):
        self.nodes = []

    def add_node(self, node, weight: float):
        if weight > 0:
            self.nodes.append((node, weight))

    def run(self, context):
        vectors = []
        weights = []

        for node, weight in self.nodes:
            vectors.append(node.execute(context))
            weights.append(weight)

        aggregator = WeightedSumAggregator()
        return aggregator.aggregate(vectors, weights)
