from typing import List

import numpy as np


def euclidean_distance(emb1: List[float], emb2: List[float]) -> float:
    """
    Calculate the Euclidean distance between two embeddings.

    Parameters:
    emb1 (List[float]): The first embedding.
    emb2 (List[float]): The second embedding.

    Returns:
    float: The Euclidean distance between the embeddings.
    """
    # Convert lists to numpy arrays
    emb1_array = np.array(emb1)
    emb2_array = np.array(emb2)

    # Calculate the Euclidean distance
    distance = np.linalg.norm(emb1_array - emb2_array)
    return float(distance)


def cosine_distance(emb1: List[float], emb2: List[float]) -> float:
    """
    Calculate the cosine distance between two embeddings.

    Parameters:
    emb1 (List[float]): The first embedding.
    emb2 (List[float]): The second embedding.

    Returns:
    float: The cosine distance between the embeddings.
    """
    # Convert lists to numpy arrays
    emb1_array = np.array(emb1)
    emb2_array = np.array(emb2)

    # Calculate the cosine distance
    distance = 1 - np.dot(emb1_array, emb2_array) / (np.linalg.norm(emb1_array) * np.linalg.norm(emb2_array))
    return distance
