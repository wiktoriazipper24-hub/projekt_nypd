
import pytest
from collections import Counter
from analyzer.similarity import calculate_cosine_similarity


@pytest.mark.parametrize("counter1, counter2, expected", [
    (Counter({'tadeusz': 10, 'zamek': 5}), Counter({'tadeusz': 10, 'zamek': 5}), 100.0),
    (Counter({'tadeusz': 10}), Counter({'wokulski': 10}), 0.0),
    (Counter(), Counter(), 0.0),
])
def test_cosine_similarity(counter1, counter2, expected):
    assert calculate_cosine_similarity(counter1, counter2, n=1000) == expected


def test_empty_counters():
    # test edge case when both dictionaries are empty
    assert calculate_cosine_similarity(Counter(), Counter(), n=1000) == 0.0

def test_partially_similar_texts():
    counter1 = Counter({'tadeusz': 10, 'zamek': 5, 'maryla': 3})
    counter2 = Counter({'tadeusz': 8, 'zamek': 2, 'inny': 5})
    result = calculate_cosine_similarity(counter1, counter2, n=1000)
    assert 0 < result < 100

def test_zero_norm_similarity():
    from collections import Counter
    counter1 = Counter()  # pusty - norm = 0
    counter2 = Counter({'kot': 5})
    result = calculate_cosine_similarity(counter1, counter2, n=10)
    assert result == 0.0