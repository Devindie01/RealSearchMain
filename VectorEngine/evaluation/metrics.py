import math

# precision
def precision_at_k(retrieved, relevant, k=10):
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)

    hits = sum(1 for doc in retrieved_k if doc in relevant_set)
    return hits / k

# recall
def recall_at_k(retrieved, relevant, k=10):
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)

    if len(relevant_set) == 0:
        return 0

    hits = sum(1 for doc in retrieved_k if doc in relevant_set)
    return hits / len(relevant_set)

# f1 score
def f1_at_k(retrieved, relevant, k=10):
    p = precision_at_k(retrieved, relevant, k)
    r = recall_at_k(retrieved, relevant, k)

    if p + r == 0:
        return 0
    return 2 * (p * r) / (p + r)

def reciprocal_rank(retrieved, relevant):
    relevant_set = set(relevant)

    for i, doc in enumerate(retrieved, start=1):
        if doc in relevant_set:
            return 1 / i
    return 0


def mean_reciprocal_rank(queries):
    return sum(reciprocal_rank(q["retrieved"], q["relevant"]) for q in queries) / len(queries)

def average_precision(retrieved, relevant):
    relevant_set = set(relevant)

    hits = 0
    sum_precision = 0

    for i, doc in enumerate(retrieved, start=1):
        if doc in relevant_set:
            hits += 1
            sum_precision += hits / i

    if hits == 0:
        return 0

    return sum_precision / len(relevant_set)


def mean_average_precision(queries):
    return sum(average_precision(q["retrieved"], q["relevant"]) for q in queries) / len(queries)

def average_precision(retrieved, relevant):
    relevant_set = set(relevant)

    hits = 0
    sum_precision = 0

    for i, doc in enumerate(retrieved, start=1):
        if doc in relevant_set:
            hits += 1
            sum_precision += hits / i

    if hits == 0:
        return 0

    return sum_precision / len(relevant_set)


def mean_average_precision(queries):
    return sum(average_precision(q["retrieved"], q["relevant"]) for q in queries) / len(queries)


def dcg_at_k(retrieved, relevant, k=10):
    relevant_set = set(relevant)
    dcg = 0

    for i, doc in enumerate(retrieved[:k], start=1):
        rel = 1 if doc in relevant_set else 0
        dcg += rel / math.log2(i + 1)

    return dcg


def idcg_at_k(relevant, k=10):
    ideal_rels = [1] * min(len(relevant), k)
    idcg = 0

    for i, rel in enumerate(ideal_rels, start=1):
        idcg += rel / math.log2(i + 1)

    return idcg


def ndcg_at_k(retrieved, relevant, k=10):
    dcg = dcg_at_k(retrieved, relevant, k)
    idcg = idcg_at_k(relevant, k)

    if idcg == 0:
        return 0

    return dcg / idcg