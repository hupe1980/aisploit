import pytest

from aisploit.utils import cosine_distance, euclidean_distance


# Test cases for cosine_distance function
@pytest.mark.parametrize(
    "emb1, emb2, expected_distance",
    [
        ([1.0, 0.0], [0.0, 1.0], 1.0),  # Orthogonal vectors
        ([1.0, 2.0], [2.0, 4.0], 0.0),  # Parallel vectors with same direction
        ([1.0, 2.0], [-1.0, -2.0], 2.0),  # Parallel vectors with opposite direction
        ([1.0, 0.0], [1.0, 0.0], 0.0),  # Identical vectors
    ],
)
def test_cosine_distance(emb1, emb2, expected_distance):
    assert cosine_distance(emb1, emb2) == pytest.approx(expected_distance, abs=1e-6)


# Test cases for euclidean_distance function
@pytest.mark.parametrize(
    "emb1, emb2, expected_distance",
    [
        ([1.0, 0.0], [0.0, 1.0], 1.4142135623730951),  # Orthogonal vectors
        (
            [1.0, 2.0],
            [2.0, 4.0],
            2.23606797749979,
        ),  # Parallel vectors with same direction
        (
            [1.0, 2.0],
            [-1.0, -2.0],
            4.47213595499958,
        ),  # Parallel vectors with opposite direction
        ([1.0, 0.0], [1.0, 0.0], 0.0),  # Identical vectors
    ],
)
def test_euclidean_distance(emb1, emb2, expected_distance):
    assert euclidean_distance(emb1, emb2) == pytest.approx(expected_distance, abs=1e-6)
